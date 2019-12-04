import config
from model import Vote,Voter
from sqlalchemy import func,desc
db = config.db

import vote_bo
import voter_dao
import option_dao

def save_vote(user_id, vote_key,votation_id,option_id):
    """
    User choose only one option
    The jud is always 1
    Insert an array of zeros with only one 1.
    """
    option_list = option_dao.load_options_by_votation(votation_id)
    ar = []
    for o in option_list:
        if o.option_id == option_id:
            ar.append(1)
        else:
            ar.append(0)
    return vote_bo.save_votes(user_id, vote_key, votation_id, ar)

def counting_votes(votation_id):
    """ Return a dict
    """
    v = db.session.query(Vote.option_id, func.count(Vote.option_id)) \
                  .filter(Vote.votation_id == votation_id, Vote.jud_value == 1) \
                  .group_by(Vote.option_id) \
                  .order_by(desc(func.count(Vote.option_id))) \
                  .all()
    ar = {}
    for row in v:
        ar[row[0]] = row[1]
    return ar    

