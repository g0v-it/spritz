#
# voter business logic: put commits here
#
import config
from model import Voter

db = config.db

import voter
import user

def insert_voters_array(votation_id, ar):
    """returns number of inserted rows"""
    count = 0
    for user_name in ar:
        u = user.load_user_by_username(user_name)
        if u:
            n = db.session.query(Voter).filter(Voter.user_id == u.user_id,Voter.votation_id==votation_id).count() 
            if n == 0:
                o = Voter(votation_id = votation_id, user_id = u.user_id, voted = 0)
                if voter.insert_dto(o):
                    count += 1
    if count > 0:
        db.session.commit()
    return count
        

def set_voted(o):
    """insert or update the voter record"""
    result = False
    if voter.has_voted(o):
        return True
    o.voted = 1
    result = voter.insert_dto(o)
    if not result:
        result = voter.update_dto(o)
    db.session.commit()
    return result

