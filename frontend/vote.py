import dbmanager
import config
import option
import voter
import votation

class vote_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.vote_key    = None
        self.votation_id = None
        self.option_id   = None
        self.jud_value   = None


def insert_dto(o):
    try:
        conn = dbmanager.get_connection()
        c = conn.cursor()
        c.execute("""insert into vote(
                vote_key, votation_id, option_id,jud_value) values (%s,%s,%s,%s)""",(o.vote_key,o.votation_id, o.option_id ,o.jud_value) )
        c.close()
        conn.close()
        return True
    except:
        return False

def delete_votes_by_key(vote_key):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from vote where vote_key = %s", (vote_key,) )
    c.close()
    conn.close()

def delete_votes_by_votation_id(votation_id):
    """
    For testing pourpose
    """
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from vote where votation_id = %s", (votation_id,) )
    c.close()
    conn.close()


def load_vote_by_key(vote_key):
    """Returns a vote_dto array"""
    ar = []
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from vote c where c.vote_key = %s order by option_id", (vote_key,) )
    row = c.fetchone()
    while row:
        o = vote_dto()
        o.vote_key = row['vote_key']
        o.votation_id = row['votation_id']
        o.option_id = row['option_id']
        o.jud_value = row['jud_value']
        ar.append(o)
        row = c.fetchone()
    c.close()
    conn.close()
    return ar

def count_votes(votation_id):
    """
    Count number of different vote_key. Its pourpose is to compare with voters.
    """
    result = None
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select count(*) from (select distinct vote_key from vote where votation_id = %s) A", (votation_id,) )
    row = c.fetchone()
    if row:
        result = row[0]
    c.close()
    conn.close()
    return result