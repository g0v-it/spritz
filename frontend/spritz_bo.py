import config
from datetime import date,datetime
import user
import option
import voter
import vote
import votation
from model import Votation,Vote,Voter,Option
from flask_babel import gettext
_ = gettext

db = config.db


def insert_votation_with_options(v,option_array):
    result = True
    try:
        if votation.insert_votation_dto(v):
            for o in option_array:
                if not option.insert_dto(o):
                    result = False
        else:
            result = False
    except Exception as e:
        result = False
        print ("Exception insert_votation_and_options: " + str(e))
    if result:
        db.session.commit()
    else:
        db.session.rollback()
    return result



