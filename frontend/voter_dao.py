#
# voter DAO: no commit here
#
import config
from model import Voter,Option,VotingUser,Votation

db = config.db

#import option_dao
import user
import votation_dao
from sqlalchemy import desc
# class voter_dto:
#     """DTO class for the database table"""
#     def __init__(self):
#         self.user_id = None
#         self.votation_id = None
#         self.voted = None

def load_voters_list(votation_id):
    return db.session.query(Voter).filter(Voter.votation_id == votation_id).order_by(desc(Voter.voted)).all()
    

def insert_dto(o):
    try:
        db.session.add(o)
    except Exception as e:
        print ("Exception voter_dao.insert_dto: " + str(e))
        return False
    return True

def update_dto(o):
    v = db.session.query(Voter).filter(Voter.votation_id == o.votation_id, Voter.user_id == o.user_id).first()
    if v:
        v.voted = o.voted
        return True
    return False


def has_voted(user_id, votation_id):
    result = False
    n = db.session.query(Voter).filter(Voter.votation_id == votation_id, Voter.user_id == user_id, Voter.voted==1).count()
    if n == 1:
        result = True
    return result

def set_voted(user_id, votation_id):
    """insert or update the voter record"""
    result = False
    if has_voted(user_id, votation_id):
        return True
    voter1 = db.session.query(Voter).filter(Voter.votation_id == votation_id, Voter.user_id == user_id).first()
    if voter1:
        voter1.voted = 1
        result = True
    else:
        o = Voter(votation_id = votation_id, user_id=user_id, voted=1)
        result = insert_dto(o)
    return result


def delete_dto(o):
    result = False
    v = db.session.query(Voter).filter(Voter.votation_id == o.votation_id, Voter.user_id == o.user_id).first()
    if v:
        db.session.delete(v)
        result = True
    return result

# this is ok to be here and not in the bo
def delete_by_votation_id(votation_id):
    ar = db.session.query(Voter).filter(Voter.votation_id == votation_id).all()
    for v in ar:
        db.session.delete(v)
    return True

def count_voters(votation_id):
    """
    Count voters. Its pourpose is to compare with number of votes.
    """
    return db.session.query(Voter).filter(Voter.votation_id == votation_id, Voter.voted == 1).count()


        
def split_string_remove_dup(text):
    lines = text.splitlines()
    lines = list(map(lambda l: l.strip(),lines))
    lines = filter(None,lines)
    lines = list(set(lines)) # removing duplicates  
    return lines

def is_voter(votation_id,user_id):
    """Have you the right to vote?"""
    result = False
    v = votation_dao.load_votation_by_id(votation_id)
    if not v:
        return False
    #if votation_id == v.promoter_user.user_id: NO GOOD
        #return True
    if v.list_voters == 0:
        return True
    n = db.session.query(Voter).filter(Voter.votation_id == votation_id, Voter.user_id == user_id).count()
    if n == 1:
        result = True
    return result



