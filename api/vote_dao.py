import config
from model import Vote,Votation
from sqlalchemy import func
db = config.db

#import option_dao
import voter_dao
import votation_dao
import option_dao
import judgement_dao


def insert_dto(o):
    try:
        db.session.add(o)
    except Exception as e:
        print ("Exception vote.insert_dto: " + str(e))
        return False
    return True

def delete_votes_by_key(vote_key):
    ar = db.session.query(Vote).filter(Vote.vote_key == vote_key).all()
    for v in ar:
        db.session.delete(v)
    return True

def delete_votes_by_votation_id(votation_id):
    """
    For testing pourpose
    """
    ar = db.session.query(Vote).filter(Vote.votation_id == votation_id).all()
    for v in ar:
        db.session.delete(v)
    return True


def load_vote_by_key(vote_key):
    """Returns a vote_dto array"""
    ar = db.session.query(Vote).filter(Vote.vote_key == vote_key).all()
    return ar

def count_votes(votation_id):
    """
    Count number of different vote_key. Its pourpose is to compare with voters.
    """
    n = db.session.query(Vote.vote_key).filter(Vote.votation_id == votation_id).distinct().count()
    return n    

def __counts_votes_by_options_and_jud(votation_id,option_id,jud_value):
    """
    Count votes for an option and a judgement value.
    Returns the count
    """
    n = db.session.query(Vote.option_id) \
        .filter(Vote.votation_id == votation_id, Vote.option_id == option_id, Vote.jud_value == jud_value) \
        .count()
    return n

def __counts_votes_by_options(votation_id,option_id):
    """
    Count votes for an option.
    Returns dict {jud_value: count, ...}
    """
    d = {}
    jud_array = judgement_dao.load_judgement_by_votation(votation_id)
    for j in jud_array:
        n = __counts_votes_by_options_and_jud(votation_id,option_id, j.jud_value)
        d[j.jud_value] = n
    return d

def counts_votes_by_votation(votation_id):
    """
    Count votes.
    Returns dict of dict {option_id: {jud_value: count, ... } ... }
    """
    result = {}
    option_array = option_dao.load_options_by_votation(votation_id)
    for o in option_array:
        d = __counts_votes_by_options(votation_id, o.option_id)
        result[o.option_id] = d
    return result

def save_vote(votation_id, vote_key, array_judgements):
    option_array = option_dao.load_options_by_votation(votation_id)
    jud_array = judgement_dao.load_judgement_by_votation(votation_id)
    if len(array_judgements) != len(option_array):
        return False
    valid_jud = []
    for j in jud_array:
        valid_jud.append(j.jud_value)
    i = 0
    for o in option_array:
        if array_judgements[i] not in valid_jud:
            return False
        v = Vote(vote_key = vote_key, \
                 votation_id = votation_id, \
                 option_id = o.option_id, \
                 jud_value = array_judgements[i])
        insert_dto(v)
        i += 1
    return True