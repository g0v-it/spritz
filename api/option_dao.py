import config
from model import Option

db = config.db

# class option_dto:
#     """DTO class for the database table"""
#     def __init__(self):
#         self.option_id = None
#         self.votation_id = None
#         self.option_name = None

def load_options_by_votation(votation_id):
    """Returns a option_dto array"""
    ar = db.session.query(Option).filter(Option.votation_id == votation_id).order_by(Option.option_id).all()
    return ar


def insert_dto(o):
    try:
        db.session.add(o)
        o = db.session.query(Option).filter(Option.votation_id == o.votation_id, Option.option_name == o.option_name).first()
    except Exception as e:
        print("option.insert_dto: " + str(e))
        return False
    return True

def delete_dto(o):
    try:
        db.session.delete(o)
    except Exception as e:
        print("option.delete_dto: " + str(e))
        return False
    return True

def delete_options_by_votation(votation_id):
    try:
        ar = db.session.query(Option).filter(Option.votation_id == votation_id).all()
        for o in ar: 
            db.session.delete(o)
    except Exception as e:
        print("option.delete_options_by_votation: " + str(e))
        return False
    return True

def save_options_from_text(votation_id,text):
    lines = text.splitlines()
    lines = list(map(lambda l: l.strip().upper(),lines))
    lines = list(set(lines)) # removing duplicates  
    lines.sort()     
    for l in lines:
        if l.strip():
            o = Option(votation_id=votation_id, option_name=l)
            if not insert_dto(o):
                return False
    return True



