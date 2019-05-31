import dbmanager
import config
import option
import user
import votation

class voter_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.user_id = None
        self.votation_id = None
        self.voted = None


def insert_dto(o):
    try:
        conn = dbmanager.get_connection()
        c = conn.cursor()
        c.execute("""insert into voter(
                        user_id, votation_id,voted) values (%s,%s,%s)""",(o.user_id,o.votation_id, o.voted) )
        c.close()
        conn.close()
        return True
    except:
        return False

def update_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""update voter set voted = %s 
                    where user_id=%s and votation_id=%s""",(o.voted,o.user_id,o.votation_id) )
    c.close()
    conn.close()
    return True


def has_voted(o):
    result = False
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select count(*) from voter where user_id = %s and votation_id = %s and voted=1", (o.user_id,o.votation_id) )
    row = c.fetchone()
    if row[0] == 1:
        result = True
    c.close()
    conn.close()
    return result


def delete_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""delete from voter where user_id = %s and votation_id = %s """,(o.user_id,o.votation_id, ) )
    c.close()
    conn.close()
    return True

def count_voters(votation_id):
    """
    Count voters. Its pourpose is to compare with number of votes.
    """
    result = None
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select count(*) from voter where votation_id = %s and voted=1", (votation_id,) )
    row = c.fetchone()
    if row:
        result = row[0]
    c.close()
    conn.close()
    return result

def insert_voters_array(votation_id, ar):
    """returns number of inserted rows"""
    count = 0
    for user_name in ar:
        u = user.load_user_by_username(user_name)
        if u:
            o = voter_dto()
            o.votation_id = votation_id
            o.user_id = u.user_id
            o.voted = 0
            if insert_dto(o):
                count += 1
    return count
        
def split_string_remove_dup(text):
    lines = text.splitlines()
    lines = list(map(lambda l: l.strip(),lines))
    lines = filter(None,lines)
    lines = list(set(lines)) # removing duplicates  
    return lines

def is_voter(votation_id,user_id):
    """Have you the right to vote?"""
    result = False
    v = votation.load_votation_by_id(votation_id)
    if not v:
        return False
    #if votation_id == v.promoter_user.user_id: NO GOOD
        #return True
    if v.list_voters == 0:
        return True
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select count(*) from voter where user_id = %s and votation_id = %s", (user_id,votation_id) )
    row = c.fetchone()
    if row[0] == 1:
        result = True
    c.close()
    conn.close()
    return result

def set_voted(o):
    """insert or update the voter record"""
    result = False
    if has_voted(o):
        return True
    o.voted = 1
    result = insert_dto(o)
    if not result:
        result = update_dto(o)
    return result

