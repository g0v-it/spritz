import config
from model import Vote,Voter
from sqlalchemy import func,desc
db = config.db

import vote
import voter
import voter_bo

def save_vote(user_id, vote_key,votation_id,option_id):
    vu = Voter(user_id = user_id, votation_id = votation_id)
    b_has_voted = voter.has_voted(vu)
    if b_has_voted:
        votes = vote.load_vote_by_key(vote_key)
        if len(votes) == 0:
            return False
        vote.delete_votes_by_key(vote_key)
    o = Vote(vote_key = vote_key, \
        votation_id = votation_id, \
        option_id = option_id, \
        jud_value = 1)
    vote.insert_dto(o)
    voter_bo.set_voted(vu)
    db.session.commit()
    return True

def counting_votes(votation_id):
    """ Return a dict
    """
    v = db.session.query(Vote.option_id, func.count(Vote.option_id)).filter(Vote.votation_id == votation_id).group_by(Vote.option_id).order_by(desc(func.count(Vote.option_id))).all()
    ar = {}
    for row in v:
        ar[row[0]] = row[1]
    return ar    

