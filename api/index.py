#!/usr/bin/env python3
import os
from flask import Flask, render_template,request,redirect,url_for,jsonify
from flask_login import LoginManager, login_required, current_user,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
import config 
import datetime
from config import MSG_INFO,MSG_OK,MSG_KO
#per abilitare CORS
from flask_cors import CORS, cross_origin



app = Flask(__name__)
# per abilitare CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# fine CORS

app.secret_key = os.urandom(24) 
# flask-login initialization
login_manager = LoginManager()
login_manager.init_app(app)
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
if config.AUTH == 'test':
    import auth_test as auth

@login_manager.user_loader
def load_user(user_name):
    u = user.User(user_name)
    if u.is_valid():
        return u
    return None







# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('login'))

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
#
######################### A P I ####################################
#

@app.route("/api/login", methods=['POST',])
def api_login():
    j = request.json
    user_name = j["username"]
    pass_word = j["password"]
    auth_data = {'username': user_name, 'password': pass_word}
    auth_result = auth.auth(auth_data)
    if auth_result['logged_in']:
        u = user.User(auth_result['username'])
        login_user(u)
        result = {"rc":True, "username": u.u.user_name, "user_id": u.u.user_id }
    else:
        result = {"rc":False }
    return jsonify(result), 201



@app.route("/api/votation", methods=['POST','GET'])
#@login_required
def api_votation():
    if request.method == "POST":
        j = request.json
        v = Votation()
        v.promoter_user_id     = j["promoter_user_id"]   
        v.votation_description = j["votation_description"]
        v.description_url      = j["description_url"]
        v.begin_date           = j["begin_date"]
        v.end_date             = j["end_date"]
        v.votation_type        = j["votation_type"]
        v.votation_status      = j["votation_status"]
        v.list_voters          = j["list_voters"]
        options_text           = j["options_text"]
        judgement_text         = j["judgement_text"]
        errmsg, msg_ok = votation_bo.insert_votation_with_options(v, options_text, judgement_text)
        result = {"rc":msg_ok, "error_message": errmsg , "votation_id": v.votation_id}
        return jsonify(result), 201
    if request.method == "GET":
        votations = votation_dao.load_votations()
        l = []
        for v in votations:
            o = {"votation_id":          v.votation_id,
                "promoter_user_id":     v.promoter_user_id     ,  
                "votation_description": v.votation_description,
                "description_url":      v.description_url    , 
                "begin_date":           str(v.begin_date)   ,       
                "end_date":             str(v.end_date)    ,        
                "votation_type":        v.votation_type   ,    
                "votation_status":      v.votation_status,     
                "list_voters":          v.list_voters}
            l.append(o)
        result = {"rc":True, "votations": l }
        return jsonify(result), 201


@app.route("/api/votation/<int:votation_id>", methods=['GET',])
@login_required
def api_votation_get_by_id(votation_id):
    v = votation_dao.load_votation_by_id(votation_id)
    o = {"votation_id":          v.votation_id,
        "promoter_user_id":     v.promoter_user_id     ,  
        "votation_description": v.votation_description,
        "description_url":      v.description_url    , 
        "begin_date":           str(v.begin_date)   ,       
        "end_date":             str(v.end_date)    ,        
        "votation_type":        v.votation_type   ,    
        "votation_status":      v.votation_status,     
        "list_voters":          v.list_voters}
    result = {"rc":True, "votation": o }
    return jsonify(result), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
