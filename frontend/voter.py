import dbmanager
import config
import option

class voter_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.user_id = None
        self.votation_id = None
        self.voted = None


def insert_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""insert into voter(
                    user_id, votation_id,voted) values (%s,%s,%s)""",(o.user_id,o.votation_id, o.voted) )
    c.close()
    conn.close()

def update_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""update voter set voted = %s 
                    where user_id=%s and votation_id=%s""",(o.voted,o.user_id,o.votation_id) )
    c.close()
    conn.close()


def has_voted(o):
    result = False
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from voter where user_id = %s and votation_id = %s and voted=1", (o.user_id,o.votation_id) )
    row = c.fetchone()
    if row:
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

