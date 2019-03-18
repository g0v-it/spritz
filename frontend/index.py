#!/usr/bin/env python3
import os
from flask import Flask, render_template,request,redirect,url_for
from flask_login import LoginManager, login_required, current_user,login_user,logout_user
import config 
import user
import votation
import candidate
import backend
import option
import vote
import voter
import datetime
import auth 

MSG_INFO = 0
MSG_OK   = 1
MSG_KO   = 2

app = Flask(__name__)
app.secret_key = os.urandom(24) 
login_manager = LoginManager()
login_manager.init_app(app)

def votation_timing(v):
    # timing of votation
    now = datetime.datetime.utcnow()
    #now_string = "{}-{}-{} {}:{}".format(now.year, now.month,now.day,now.hour,now.minute)
    votation_timing = 0
    if now < v.begin_date:
        votation_timing = -1 
    if now > v.end_date:
        votation_timing = +1 
    return votation_timing


@login_manager.user_loader
def load_user(user_name):
    u = user.User(user_name)
    if u.is_valid():
        return u
    return None

@app.route("/")
@login_required
def index():
    return render_template('index_template.html', pagetitle="Menu principale")

@app.route("/login", methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':    
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        u = user.User(user_name)
        if u.try_to_authenticate(pass_word):
            login_user(u)
            message = ("Login effettuato",MSG_OK)
        else:
            message = ("Login errato",MSG_KO)
    return render_template(auth.LOGIN_TEMPLATE, pagetitle="Login",message=message, CLIENT_ID=auth.CLIENT_ID)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout_template.html', pagetitle="Logout")

@app.route("/votation_propose", methods=['GET', 'POST'])
@login_required
def votation_propose():
    v = votation.get_blank_dto()
    message = ("Inserire i dati",MSG_INFO)
    if request.method == 'POST':    
        #v.votation_id = request.form['votation_id']
        v.votation_description = request.form['votation_description']
        v.begin_date = request.form['begin_date'] + " " + request.form['begin_time']
        v.end_date = request.form['end_date'] + " " + request.form['end_time']
        v.votation_type = request.form['votation_type']
        v.promoter_user = current_user.u
        if v.votation_type == votation.TYPE_DRAW:
            v.votation_status = votation.STATUS_WAIT_FOR_CAND_AND_GUAR
        else:
            v.votation_status = votation.STATUS_VOTING
        result, msg = votation.validate_dto(v)
        if result:
            if votation.insert_votation_dto(v):
                message = ("Votazione salvata",MSG_OK)
                # options saving
                option.save_options_from_text(v.votation_id,request.form['votation_options'])
            else:
                message = ("Errore, votazione non salvata",MSG_KO )                   
    return render_template('votation_propose_template.html', pagetitle="Crea una votazione", \
    votation_obj=v, message=message)

@app.route("/votation_list")
@login_required
def votation_list():
    votations_array = votation.load_votations()
    return render_template('votation_list_template.html', pagetitle="Lista delle votazioni", \
    votations_array=votations_array,states=votation.states,type_description=votation.TYPE_DESCRIPTION)

@app.route("/be_a_candidate/<int:votation_id>")
@login_required
def be_a_candidate(votation_id):
    v = votation.load_votation_by_id(votation_id)
    return render_template('be_a_candidate_template.html', pagetitle="Candidatura", v=v)


@app.route("/be_a_candidate_confirm")
@login_required
def be_a_candidate_confirm():
    votation_id = int(request.args.get('votation_id'))
    v = votation.load_votation_by_id(votation_id)
    message = ("Ora sei un candidato",MSG_OK)
    o = candidate.candidate_dto()
    app.logger.info(o)
    o.votation_id = votation_id
    o.u.user_id = current_user.u.user_id
    o.passphrase_ok = 0
    error = candidate.validate_dto(o)
    if error == 0:
        candidate.insert_dto(o)
    else:
        message = (candidate.error_messages[error] + ": " + v.votation_description,MSG_KO )
    return render_template('be_a_candidate_confirm_template.html', pagetitle="Conferma candidatura", v=v,message=message)



@app.route("/votation_detail/<int:votation_id>")
@login_required
def votation_detail(votation_id):
    v = votation.load_votation_by_id(votation_id)
    candidates_array = None
    options_array = None
    counting = None
    if v.votation_type == votation.TYPE_DRAW:
        candidates_array = candidate.load_candidate_by_votation(votation_id)
    else:
        options_array = option.load_options_by_votation(votation_id)
    # if v.votation_status > votation.STATUS_WAIT_FOR_CAND_AND_GUAR:
    #     state_array = backend.election_state(votation_id)
    # else:
    #     state_array = []
    if v.votation_status == votation.STATUS_ENDED:
        counting = vote.votation_counting(v)
    return render_template('votation_detail_template.html', pagetitle="Dettaglio votazione", \
         v=v, candidates_array=candidates_array, \
         states=votation.states, options_array=options_array, \
         count_voters=voter.count_voters(votation_id), \
         count_votes=vote.count_votes(votation_id), votation_timing=votation_timing(v),counting=counting, \
         words=votation.WORDS, type_description=votation.TYPE_DESCRIPTION)

@app.route("/start_election/<int:votation_id>")
@login_required
def start_election(votation_id):
    v = votation.load_votation_by_id(votation_id)
    candidates_array = None
    if current_user.u.user_id == v.promoter_user.user_id:
        candidates_array = candidate.load_candidate_by_votation(votation_id)
        # TODO error handling
        backend.create_election(v.votation_id, len(candidates_array), len(votation.WORDS) )
        votation.update_status(votation_id, votation.STATUS_VOTING)
    return render_template('start_election_template.html', pagetitle="Inizio votazione", \
      v=v, candidates_array=candidates_array)

@app.route("/close_election/<int:votation_id>")
@login_required
def close_election(votation_id):
    v = votation.load_votation_by_id(votation_id)
    votation.update_status(votation_id,votation.STATUS_ENDED)
    return render_template('thank_you_template.html', \
    pagetitle="Votazione Chiusa", \
    message=("Votazione chiusa. Controlla i risultati.",MSG_OK))

@app.route("/delete_election/<int:votation_id>")
@login_required
def delete_election(votation_id):
    if request.args.get('confirm') == "yes":
        votation.deltree_votation_by_id(votation_id)
        return render_template('thank_you_template.html', \
        pagetitle="Cancellazione", \
        message=("Votazione cancellata",MSG_OK))
    else:
        return render_template('confirmation_template.html', \
        pagetitle="Cancellazione", \
        message=None,votation_id=votation_id)



@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route("/version")
def print_version():
    return render_template('version_template.html', pagetitle="Frontend Version", version=os.environ['voting_version'])
  
@app.route("/vote/<int:votation_id>",  methods=['GET', 'POST'])
@login_required
def vote_maj_jud(votation_id):
    v = votation.load_votation_by_id(votation_id)
    if votation_timing(v) != 0:
        return redirect('/votation_detail/'+str(votation_id))
    options_array = option.load_options_by_votation(votation_id)
    if request.method == 'GET':    
        return render_template('majority/vote_template.html', pagetitle="Vota", \
        v=v, options_array=options_array,words_array=votation.WORDS) 
    if request.method == 'POST':  
        vote_key = request.form["vote_key"]
        vote_array = []
        for c in options_array:
            param = "v_" + str(c.option_id)
            vote_array.append(int(request.form[param]))
        result = vote.save_votes(current_user.u.user_id, vote_key, votation_id, vote_array )
        if result:
            message = ("Voto registrato correttamente", MSG_OK)
        else:
            message = ("Errore. Voto NON registrato. Password Errata?",MSG_KO)
        return render_template('thank_you_template.html', pagetitle="Registrazione voto", message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
