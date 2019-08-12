import dbmanager
import config
import re
from datetime import date
import user
import votation_dao

class candidate_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.votation_id = None
        self.u = user.user_dto()
        self.passphrase_ok = None
        self.order_n = None

def load_candidate_by_votation(votation_id):
    """Returns a candidate_dto array"""
    ar = []
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from candidate c where c.votation_id = %s order by order_n", (votation_id,) )
    row = c.fetchone()
    while row:
        o = candidate_dto()
        o.votation_id = row['votation_id']
        o.passphrase_ok = row['passphrase_ok']
        o.order_n = row['order_n']
        o.u = user.load_user_by_id(row['user_id'])
        ar.append(o)
        row = c.fetchone()
    c.close()
    conn.close()
    return ar

def load_candidate(votation_id,user_id):
    """Returns a candidate_dto """
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from candidate c where c.votation_id = %s and c.user_id = %s", (votation_id,user_id) )
    row = c.fetchone()
    o = candidate_dto()
    o.votation_id = row['votation_id']
    o.passphrase_ok = row['passphrase_ok']
    o.order_n = row['order_n']
    o.u = user.load_user_by_id(row['user_id'])
    c.close()
    conn.close()
    return o

def check_for_duplicate(o):
    """Returns true/false"""
    result = False
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select 1 from candidate where votation_id = %s and user_id=%s", (o.votation_id,o.u.user_id) )
    row = c.fetchone()
    if row:
        result = True
    c.close()
    conn.close()
    return result

def insert_dto(o):
    """Insert the candidate_dto into the DB"""   
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""insert into candidate(
                    votation_id, 
                    user_id, passphrase_ok,order_n) select %s,%s,0,count(*)+1 from candidate where votation_id = %s""",(o.votation_id, o.u.user_id,o.votation_id) )
    c.close()
    conn.close()

def delete_dto(o):
    """Delete the candidate_dto from the DB"""   
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from candidate where votation_id = %s and user_id = %s", (o.votation_id,o.u.user_id) )
    c.close()
    conn.close()

error_messages = [
    "", \
    "User undefined", \
    "Votation undefined", \
    "The user id is invalid", \
    "The votation id is invalid", \
    "Duplicate record", \
]
        
def validate_dto(o):
    """Validate data for writing in DB. Returns error code, 0 on success"""
    result = 0
    if result==0:
        if o.u.user_id == None:
            result = 1
    if result==0:
        if o.votation_id == None:
            result = 2
    if result==0:
        u = user.load_user_by_id(o.u.user_id)
        if u == None:
            result = 3
    if result==0:
        u = votation_dao.load_votation_by_id(o.votation_id)
        if u == None:
            result = 4
    if result==0:
        if check_for_duplicate(o):
            result = 5
    return result
            
def set_passphrase_ok(user_id,votation_id):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""update candidate set passphrase_ok = 1 where 
                    votation_id = %s and
                    user_id = %s""",(votation_id, user_id) )
    c.close()
    conn.close()

def candidates_passphrases_complete(votation_id):
    """Check if all candidates has sent the passphrase"""
    ar = load_candidate_by_votation(votation_id)
    if len(ar) == 0:
        return False
    for c in ar:
        if c.passphrase_ok == 0:
            return False
    return True

