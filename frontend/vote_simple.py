import vote
import voter
import dbmanager


def save_vote(user_id, vote_key,votation_id,option_id):
    #print(user_id, vote_key,votation_id,option_id)
    vu = voter.voter_dto()
    vu.user_id = user_id
    vu.votation_id = votation_id
    b_has_voted = voter.has_voted(vu)
    if b_has_voted:
        votes = vote.load_vote_by_key(vote_key)
        if len(votes) == 0:
            return False
        vote.delete_votes_by_key(vote_key)
    o = vote.vote_dto()
    o.vote_key = vote_key
    o.votation_id = votation_id
    o.option_id = option_id
    o.jud_value = 1
    vote.insert_dto(o)
    voter.set_voted(vu)
    return True

def counting_votes(votation_id):
    """ Return an array 
    """
    conn = dbmanager.get_connection()
    ar = {}
    c = conn.cursor()
    q = "select option_id, count(*) from vote where votation_id = %s group by option_id order by 2 desc"
    c.execute(q, (votation_id, ))
    row = c.fetchone()
    while row:
        ar[row[0]] = row[1]
        row = c.fetchone()      
    c.close()
    return ar    

