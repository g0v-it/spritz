#!/usr/bin/env python3
import os
from flask import Flask, render_template,request,redirect,url_for
from flask_login import LoginManager, login_required, current_user,login_user,logout_user
from flask_babel import Babel,gettext
from flask_sqlalchemy import SQLAlchemy
import config 
import datetime
from config import MSG_INFO,MSG_OK,MSG_KO

LANGUAGES = {
    'en': 'English',
    'it': 'Italian'
}
current_language = None

app = Flask(__name__)
app.secret_key = os.urandom(24) 
# flask-login initialization
login_manager = LoginManager()
login_manager.init_app(app)
# flask-babel initialization
babel = Babel(app=app)
_ = gettext
# flask-sqlalchemy initialization
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
config.db = db

import user
import votation_dao
# import candidate
#import backend
import option_dao
import judgement_dao
import vote_dao
import vote_maj_jud
import vote_simple
import voter_dao
import voter_bo
import votation_bo
from model import Votation
if config.AUTH == 'ldap':
    import auth_ldap as auth
if config.AUTH == 'google':
    import auth_google as auth
if config.AUTH == 'superauth':
    import auth_superauth as auth
if config.AUTH == 'test':
    import auth_test as auth

@babel.localeselector
def get_locale():
    # return 'it'
    if current_language:
        return current_language
    return request.accept_languages.best_match(LANGUAGES.keys())

@login_manager.user_loader
def load_user(user_name):
    u = user.User(user_name)
    if u.is_valid():
        return u
    return None

@app.route("/")
@login_required
def index():
    return render_template('index_template.html', pagetitle=_("Main menu"))

@app.route("/credits")
def credits():
    return render_template('docs/credits.html', pagetitle=_("Credits"))

@app.route("/terms-and-conditions")
def termsandconditions():
    return render_template('docs/terms-and-conditions.html', pagetitle=_("Credits"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    message = None
    #print(auth.CLIENT_ID)
    if request.method == 'POST': 
        auth_data = auth.get_auth_data(request)
        auth_result = auth.auth(auth_data)
        if auth_result['logged_in']:
            u = user.User(auth_result['username'])
            login_user(u)
            message = (auth_result['message'],MSG_OK)
        else:
            message = (auth_result['message'],MSG_KO)
    return render_template(auth.LOGIN_TEMPLATE, pagetitle=_("Login"),message=message, CLIENT_ID=auth.CLIENT_ID)

@app.route("/superauthcallback", methods=['GET',])
def superauth_callback():
    message = None
    auth_data = auth.get_auth_data(request)
    auth_result = auth.auth(auth_data)
    if auth_result['logged_in']:
        u = user.User(auth_result['username'])
        login_user(u)
        message = (auth_result['message'],MSG_OK)
    else:
        message = (auth_result['message'],MSG_KO)
    return render_template(auth.LOGIN_TEMPLATE, pagetitle=_("Login result"),message=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout_template.html', pagetitle="Logout")




@app.route("/votation_propose", methods=['GET', 'POST'])
@login_required
def votation_propose():
    v = Votation()
    message = (_("Please, insert data"),MSG_INFO)
    if request.method == 'POST':    
        #v.votation_id = request.form['votation_id']
        v.votation_description = request.form['votation_description']
        v.description_url = request.form['description_url']
        v.begin_date = request.form['begin_date'] + " " + request.form['begin_time']
        v.end_date = request.form['end_date'] + " " + request.form['end_time']
        v.votation_type = request.form['votation_type']
        v.list_voters = 0
        if 'list_voters' in  request.form.keys():
            v.list_voters = request.form['list_voters']
        v.promoter_user_id = current_user.u.user_id
        if v.votation_type == votation_dao.TYPE_DRAW:
            v.votation_status = votation_dao.STATUS_WAIT_FOR_CAND_AND_GUAR
        else:
            v.votation_status = votation_dao.STATUS_VOTING
        message = votation_bo.insert_votation_with_options(v, request.form['votation_options'], request.form['votation_juds'])
    return render_template('votation_propose_template.html', pagetitle=_("New election"), \
    votation_obj=v, message=message,utcnow=str(datetime.datetime.utcnow()) )

@app.route("/votation_list")
@login_required
def votation_list():
    votations_array = votation_dao.load_votations()
    votations_array.reverse()
    return render_template('votation_list_template.html', pagetitle=_("Election list"), \
    votations_array=votations_array,states=votation_dao.states,type_description=votation_dao.TYPE_DESCRIPTION)

# @app.route("/be_a_candidate/<int:votation_id>")
# @login_required
# def be_a_candidate(votation_id):
#     v = votation_dao.load_votation_by_id(votation_id)
#     return render_template('be_a_candidate_template.html', pagetitle="Candidatura", v=v)


# @app.route("/be_a_candidate_confirm")
# @login_required
# def be_a_candidate_confirm():
#     votation_id = int(request.args.get('votation_id'))
#     v = votation_dao.load_votation_by_id(votation_id)
#     message = ("Ora sei un candidato",MSG_OK)
#     o = candidate.candidate_dto()
#     app.logger.info(o)
#     o.votation_id = votation_id
#     o.u.user_id = current_user.u.user_id
#     o.passphrase_ok = 0
#     error = candidate.validate_dto(o)
#     if error == 0:
#         candidate.insert_dto(o)
#     else:
#         message = (candidate.error_messages[error] + ": " + v.votation_description,MSG_KO )
#     return render_template('be_a_candidate_confirm_template.html', pagetitle="Conferma candidatura", \
#         v=v,message=message)



@app.route("/votation_detail/<int:votation_id>")
@login_required
def votation_detail(votation_id):
    v = votation_dao.load_votation_by_id(votation_id)
    if v.votation_type == votation_dao.TYPE_MAJORITY_JUDGMENT:
        return votation_detail_maj_jud(v)
    # if v.votation_type == votation_dao.TYPE_DRAW:
    #     return votation_detail_draw(v)
    if v.votation_type == votation_dao.TYPE_SIMPLE_MAJORITY:
        return votation_detail_simple(v)


# def votation_detail_draw(v):
#     candidates_array = None
#     counting = None
#     candidates_array = candidate.load_candidate_by_votation(v.votation_id)
#     # if v.votation_status > votation_dao.STATUS_WAIT_FOR_CAND_AND_GUAR:
#     #     state_array = backend.election_state(votation_id)
#     # else:
#     #     state_array = []
#     return render_template('draw/votation_detail_template.html', pagetitle="Election details", \
#          v=v, candidates_array=candidates_array, \
#          states=votation_dao.states,  \
#          count_voters=voter_dao.count_voters(v.votation_id), \
#          count_votes=vote_dao.count_votes(v.votation_id), \
#          votation_timing=votation_dao.votation_timing(v),counting=counting, \
#          words=votation_dao.WORDS, type_description=votation_dao.TYPE_DESCRIPTION)


def votation_detail_maj_jud(v):
    options_array = option_dao.load_options_by_votation(v.votation_id)
    juds_array = judgement_dao.load_judgement_by_votation(v.votation_id)
    counting = None
    is_voter = voter_dao.is_voter(v.votation_id, current_user.u.user_id)
    if v.votation_status == votation_dao.STATUS_ENDED:
        counting = vote_maj_jud.votation_counting(v)
    return render_template('majority_jud/votation_detail_template.html', pagetitle=_("Election details"), \
         v=v,  \
         states=votation_dao.states, options_array=options_array,juds_array=juds_array, \
         count_voters=voter_dao.count_voters(v.votation_id), \
         count_votes=vote_dao.count_votes(v.votation_id), \
         votation_timing=votation_dao.votation_timing(v),counting=counting, \
         type_description=votation_dao.TYPE_DESCRIPTION, \
         is_voter=is_voter)

def votation_detail_simple(v):
    options_array = option_dao.load_options_by_votation(v.votation_id)
    counting = None
    is_voter = voter_dao.is_voter(v.votation_id, current_user.u.user_id)
    if v.votation_status == votation_dao.STATUS_ENDED:
        counting = vote_simple.counting_votes(v.votation_id)
    return render_template('simple_majority/votation_detail_template.html', pagetitle=_("Election details"), \
         v=v,  \
         states=votation_dao.states, options_array=options_array, \
         count_voters=voter_dao.count_voters(v.votation_id), \
         count_votes=vote_dao.count_votes(v.votation_id), \
         votation_timing=votation_dao.votation_timing(v),counting=counting, \
         type_description=votation_dao.TYPE_DESCRIPTION, \
         is_voter=is_voter)


@app.route("/close_election/<int:votation_id>")
@login_required
def close_election(votation_id):
    #v = votation_dao.load_votation_by_id(votation_id)
    #votation_dao.update_status(votation_id,votation_dao.STATUS_ENDED)
    votation_bo.set_votation_status_ended(votation_id)
    return render_template('thank_you_template.html', \
    pagetitle=_("Election closed"), \
    message=(_("Election closed, please, check results"),MSG_OK))

@app.route("/delete_election/<int:votation_id>")
@login_required
def delete_election(votation_id):
    if request.args.get('confirm') == "yes":
        votation_bo.deltree_votation_by_id(votation_id)
        return render_template('thank_you_template.html', \
        pagetitle=_("Delete"), \
        message=(_("Election deleted"),MSG_OK))
    else:
        return render_template('confirmation_template.html', \
        pagetitle=_("Delete"), \
        message=None,votation_id=votation_id)

@app.route("/add_voters", methods=["POST",])
@login_required
def add_voters():
    votation_id = request.form['votation_id']
    v = votation_dao.load_votation_by_id(votation_id)
    if v.promoter_user.user_id == current_user.u.user_id: 
        list_voters = request.form['list_voters']
        ar = voter_dao.split_string_remove_dup(list_voters)
        n = voter_bo.insert_voters_array(votation_id,ar)
        return render_template('thank_you_template.html', \
        pagetitle=_("Voter"), \
        message=(_("{} voters being added").format(n),MSG_OK))
    if v.promoter_user.user_id != current_user.u.user_id:
        return render_template('thank_you_template.html', \
            pagetitle=_("Voters"), \
            message=(_("Sorry, only the owner of this election can add voters"),MSG_KO))        

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


# @app.route("/version")
# def print_version():
#     return render_template('version_template.html', pagetitle="Frontend Version", version=os.environ['voting_version'])
  
@app.route("/vote/<int:votation_id>",  methods=['GET', 'POST'])
@login_required
def vote_(votation_id):
    v = votation_dao.load_votation_by_id(votation_id)
    if votation_dao.votation_timing(v) != 0:
        return redirect('/votation_detail/'+str(votation_id))
    if voter_dao.is_voter(votation_id, current_user.u.user_id) == False:
        return redirect('/votation_detail/'+str(votation_id))
    if v.votation_type == votation_dao.TYPE_MAJORITY_JUDGMENT:
        return votemajjud(v)
    if v.votation_type == votation_dao.TYPE_SIMPLE_MAJORITY:
        return votesimplemaj(v)
        
def votemajjud(v):
    options_array = option_dao.load_options_by_votation(v.votation_id)
    if request.method == 'GET':    
        return render_template('majority_jud/vote_template.html', pagetitle=_("Vote"), \
        v=v, options_array=options_array,words_array=judgement_dao.load_judgement_by_votation(v.votation_id)) 
    if request.method == 'POST':  
        vote_key = request.form["vote_key"]
        vote_array = []
        for c in options_array:
            param = "v_" + str(c.option_id)
            vote_array.append(int(request.form[param]))
        result = vote_maj_jud.save_votes(current_user.u.user_id, vote_key, v.votation_id, vote_array )
        if result:
            message = (_("Your vote has been registered"), MSG_OK)
        else:
            message = (_("Error. Vote NOT registered. Wrong Password?"),MSG_KO)
        return render_template('thank_you_template.html', pagetitle=_("Vote registering"), message=message)

def votesimplemaj(v):
    options_array = option_dao.load_options_by_votation(v.votation_id)
    if request.method == 'GET':    
        return render_template('simple_majority/vote_template.html', pagetitle="Vota", \
        v=v, options_array=options_array) 
    if request.method == 'POST':  
        vote_key = request.form["vote_key"]
        my_vote = request.form["my_vote"]
        result = vote_simple.save_vote(current_user.u.user_id, vote_key, v.votation_id,my_vote)
        if result:
            message = (_("Your vote has been registered"), MSG_OK)
        else:
            message = (_("Error. Vote NOT registered. Wrong Password?"),MSG_KO)
        return render_template('thank_you_template.html', pagetitle=_("Vote registering"), message=message)

@app.route("/update_end_date/<int:votation_id>",  methods=['GET',])
@login_required
def update_end_date(votation_id):
    v = votation_dao.load_votation_by_id(votation_id)
    if current_user.u.user_id == v.promoter_user.user_id:
        end_date = request.args.get('end_date')
        end_time = request.args.get('end_time')
        if end_date and end_time:
            votation_bo.update_end_date(votation_id, end_date + " " + end_time)
            return "OK"
    return "KO"

@app.route("/lang/<lang_code>")
@login_required
def lang(lang_code):
    global current_language
    current_language = lang_code
    return render_template('index_template.html', pagetitle=_("Main menu"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
