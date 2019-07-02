import config
from model import Vote,Votation

db = config.db

import option
import voter
import votation


# class vote_dto:
#     """DTO class for the database table"""
#     def __init__(self):
#         self.vote_key    = None
#         self.votation_id = None
#         self.option_id   = None
#         self.jud_value   = None


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
    