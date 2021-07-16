#
# This module si a BO (business object)
# Business logic and commit here, please
#
import config
from datetime import date,datetime
import option_dao
import voter_dao
import vote_dao
import votation_dao
import judgement_dao
from config import MSG_INFO,MSG_OK,MSG_KO
from model import Votation,Vote,Voter,Option

db = config.db

def insert_votation_with_options(v,options_text,judgement_text):
    """Save votation and options.
    Options_text is a string like "A\nB\nC"
    Judgement_text is a string like "A\nB\nC" as well
    Returns a couple (string,int) -> ('Saved', MSG_OK) or (error description, MSG_KO) 
    """
    bok,errmsg = votation_dao.validate_dto(v)
    if v.votation_type == votation_dao.TYPE_SIMPLE_MAJORITY:
        judgement_text = "VOTED\nNOT VOTED"
    if bok:
        result = ("Election data saved", MSG_OK)
        if votation_dao.insert_votation_dto(v):
            if option_dao.save_options_from_text(v.votation_id,options_text):
                if judgement_dao.save_judgements_from_text(v.votation_id,judgement_text):
                    pass
                else:
                    result = ('Cannot save judgements',MSG_KO)
            else:
                result = ('Cannot save options',MSG_KO)
        else:
            result = ('Cannot save the election', MSG_KO)
    else:
        result = (errmsg, MSG_KO)
    if result[1] == MSG_OK:
        db.session.commit()
    else:
        db.session.rollback()
    return result

def set_votation_status_voting(votation_id):
    votation_dao.update_status(votation_id, votation_dao.STATUS_VOTING)
    db.session.commit()

def set_votation_status_ended(votation_id):
    votation_dao.update_status(votation_id, votation_dao.STATUS_ENDED)
    db.session.commit()

def update_end_date(votation_id, new_datetime):
    v = db.session.query(Votation).filter(Votation.votation_id == votation_id).first()
    if v:
        v.end_date = new_datetime
        db.session.commit()
        return True
    return False

def deltree_votation_by_id(votation_id):
    """Delete the votation from the DB
    with all dependencies"""
    vote_dao.delete_votes_by_votation_id(votation_id)
    voter_dao.delete_by_votation_id(votation_id)
    option_dao.delete_options_by_votation(votation_id)
    judgement_dao.delete_judgements_by_votation(votation_id)
    votation_dao.delete_votation_by_id(votation_id)
    db.session.commit()
    return True



