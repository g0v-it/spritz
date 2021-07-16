import config
from model import Vote,Voter,Option,Votation
from sqlalchemy import func,desc
db = config.db

import vote_dao
import voter_dao
import option_dao
import votation_dao
import judgement_dao
import user


def save_votes(user_id, vote_key,votation_id,vote_array):
    """
    Save a vote, one rank number per option id.
    The vote in vote_array[0] is for the first option.
    The vote in vote_array[1] is for the second option, and so on.
    Every option need a vote.
    Also, the voter is set as voted.
    """
    u = user.load_user_by_id(user_id)
    if not u:
        return False
    if voter_dao.has_voted(user_id, votation_id):
        ar = vote_dao.load_vote_by_key(vote_key)
        if len(ar) == 0:
            return False
        vote_dao.delete_votes_by_key(vote_key)
    if vote_dao.save_vote(votation_id=votation_id, vote_key=vote_key, array_judgements=vote_array):
        if voter_dao.set_voted(user_id,votation_id):
            db.session.commit() 
            return True
    db.session.rollback()
    return False


def count_votes_by_option(votation_id, option_id):
    """
    It returns an array of counts.
    The array contains one count for each rank for one option.
    """
    jud_array = judgement_dao.load_judgement_by_votation(votation_id)
    ar = []
    for j in range(len(jud_array)):
        n = db.session.query(Vote).filter(Vote.votation_id == votation_id, Vote.option_id == option_id, Vote.jud_value == j).count()
        ar.append( n )
    return ar

def votation_counting(v):
    option_list = option_dao.load_options_by_votation(v.votation_id)
    counting = []
    for o in option_list:
        ar = count_votes_by_option(v.votation_id,o.option_id)
        m = maj_jud_result(o.option_id,ar)
        m.option_name = o.option_name
        counting.append(m)
    counting.sort()       
    counting.reverse()     
    return counting

