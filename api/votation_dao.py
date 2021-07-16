#
# This module is a DAO (data access object), only simple operations. 
# No logic here.
# No commit here.
# Functions with commit are in votation_bo
#
import config
#import re
from datetime import date,datetime
import user
import option_dao
import voter_dao
import vote_dao
from model import Votation,Vote,Voter,Option

db = config.db

STATUS_WAIT_FOR_CAND_AND_GUAR = 0
STATUS_VOTING = 1
STATUS_ELABORATION = 2
STATUS_ENDED = 3
STATUS_FAILED = 4
TYPE_DRAW = 'draw'
TYPE_MAJORITY_JUDGMENT = 'maj_jud'
TYPE_MAJORITY_JUDGMENT_SECURE = 'maj_jud_sec'
TYPE_SIMPLE_MAJORITY = 'simple_maj'
TYPE_LIST_RAND = 'list_rand'

# WORDS = [_('No opinion'), _('Poor'), _('Not enough'), _('Acceptable'), _('Good'), _('Very good')]


# class votation_dto:
#     """DTO class for the database table"""

#     def __init__(self):
#         self.votation_id = None
#         self.promoter_user = user.user_dto()
#         self.votation_description = None
#         self.description_url = None
#         self.begin_date = None
#         self.end_date = None
#         self.votation_type = None
#         self.votation_status = None
#         self.list_voters = None



# def get_blank_dto():
#     v = votation_dto()
#     v.votation_id = 0
#     v.promoter_user.user_id = 0
#     v.votation_description = ''
#     v.description_url = ''
#     v.begin_date = ''
#     v.end_date = ''
#     v.votation_type = ''
#     v.votation_status = 0
#     v.list_voters = 0
#     return v


def load_votation_by_id(votation_id):
    """Returns a votation_dto object or None"""
    v = db.session.query(Votation).filter(Votation.votation_id == votation_id).first()
    return v


def load_votations():
    """Returns a votation_dto array"""
    ar = db.session.query(Votation).order_by(Votation.votation_id).all()
    return ar

def load_votations_by_promoter_user_id(promoter_user_id):
    """Returns a votation_dto array"""
    ar = db.session.query(Votation).filter(Votation.promoter_user_id == promoter_user_id).all()
    return ar

def insert_votation_dto(v):
    """Insert the votation_dto into the DB"""
    try:
        db.session.add(v)
        db.session.flush()
        v = db.session.query(Votation).filter(Votation.votation_description == v.votation_description).first()
    except Exception as e:
        print (">>>Exception insert_votation_dto: " + str(e) + "<<<")
        return False
    return True



def delete_votation_by_id(votation_id):
    """Delete the votation from the DB"""
    result = False
    v = db.session.query(Votation).filter(Votation.votation_id == votation_id).first()
    if v:
        db.session.delete(v)
        result = True
    return result

def validate_dto(v):
    """Validate data for writing in DB. Returns (True/False, "Error message")"""
    result = True
    errorMessage = "Data validated"
    if result:
        if user.load_user_by_id(v.promoter_user_id) == None:
            result = False
            errorMessage = "Promoter user id not valid"
    if result:
        if len(v.votation_description.strip()) == 0:
            result = False
            errorMessage = "Description is mandatory"
    # if result:
    #     if not validate_string_date(v.begin_date):
    #         result = False
    #         errorMessage = "Begin date not valid"
    # if result:
    #     if not validate_string_date(v.end_date):
    #         result = False
    #         errorMessage = "End date not valid"
    if result:
        if v.end_date < v.begin_date:
            result = False
            errorMessage = "Begin and End dates are not in sequence"
    if result:
        if v.votation_type != TYPE_DRAW and \
           v.votation_type != TYPE_MAJORITY_JUDGMENT and \
           v.votation_type != TYPE_MAJORITY_JUDGMENT_SECURE and \
           v.votation_type != TYPE_SIMPLE_MAJORITY and \
           v.votation_type != TYPE_LIST_RAND:
            result = False
            errorMessage = "Votation Type not valid"
    if result:
        if v.votation_status < STATUS_WAIT_FOR_CAND_AND_GUAR or v.votation_status > STATUS_FAILED:
            result = False
            errorMessage = "Status not valid: {}".format(v.votation_status)
    return (result, errorMessage)


def validate_string_date(d):
    result = True
    try:
        y = int(d[0:4])
        m = int(d[5:7])
        d = int(d[8:10])
        date(y, m, d)
    except:
        result = False
    return result


def update_status(votation_id, new_status):
    v = db.session.query(Votation).filter(Votation.votation_id == votation_id).first()
    if v:
        v.votation_status = new_status
        #db.session.commit()
        return True
    return False



def votation_timing(vdto):
    # timing of votation
    now = datetime.utcnow()
    votation_timing = 0 # ok to vote
    if now < vdto.begin_date:
        votation_timing = -1 # too early
    if now > vdto.end_date:
        votation_timing = +1 # too late
    return votation_timing

