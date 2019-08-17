import config
from model import Judgement

db = config.db

def load_judgement_by_votation(votation_id):
    """Returns an array"""
    ar = db.session.query(Judgement).filter(Judgement.votation_id == votation_id).order_by(Judgement.jud_value).all()
    return ar

def insert_dto(o):
    try:
        db.session.add(o)
        #o = db.session.query(Judgement).filter(Judgement.votation_id == o.votation_id, Judgement.judgement_name == o.judgement_name).first()
    except Exception as e:
        print("judgement.insert_dto: " + str(e))
        return False
    return True

def delete_dto(o):
    try:
        db.session.delete(o)
    except Exception as e:
        print("judgement.delete_dto: " + str(e))
        return False
    return True

def delete_judgements_by_votation(votation_id):
    try:
        ar = db.session.query(Judgement).filter(Judgement.votation_id == votation_id).all()
        for o in ar: 
            db.session.delete(o)
    except Exception as e:
        print("judgement.delete_judgements_by_votation: " + str(e))
        return False
    return True

def save_judgements_from_text(votation_id,text):
    if not text:
        return True
    lines = text.splitlines()
    lines = list(map(lambda l: l.strip().upper(),lines))
    #lines = list(set(lines)) # NO, this alter the ordering  
    lines.reverse() # the gui send you in reverse order
    v = 0           # but you have to save it from zero
    for l in lines:
        if l.strip():
            o = Judgement(votation_id=votation_id, jud_name=l,jud_value=v)
            v += 1
            if not insert_dto(o):
                return False
    return True



