import dbmanager
import config

class option_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.option_id = None
        self.votation_id = None
        self.option_name = None
        self.description = None

def load_options_by_votation(votation_id):
    """Returns a option_dto array"""
    ar = []
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from voting_option c where c.votation_id = %s order by option_id", (votation_id,) )
    row = c.fetchone()
    while row:
        o = option_dto()
        o.option_id = row['option_id']
        o.votation_id = row['votation_id']
        o.option_name = row['option_name']
        o.description = row['description']
        ar.append(o)
        row = c.fetchone()
    c.close()
    conn.close()
    return ar


def insert_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""insert into voting_option(
                    votation_id, option_name, description) values (%s,%s,%s)""",(o.votation_id, o.option_name ,o.description) )
    c.close()
    conn.close()

def delete_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from voting_option where option_id = %s", (o.option_id,) )
    c.close()
    conn.close()

def delete_options_by_votation(votation_id):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from voting_option where votation_id = %s", (votation_id,) )
    c.close()
    conn.close()


def save_options_from_text(votation_id,text):
    result = True
    lines = text.splitlines()
    lines = list(map(lambda l: l.strip().upper(),lines))
    lines = list(set(lines)) # removing duplicates  
    lines.sort()     
    for l in lines:
        if l.strip():
            o = option_dto()
            o.votation_id = votation_id
            o.option_name = l.strip()
            o.description = ""
            insert_dto(o)
    return result



