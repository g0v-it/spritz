import vote
import voter
import votation
import option
import random
import dbmanager

def insert_dto(o):
    c = conn.cursor()
    c.execute("""insert into vote(
                    vote_key, votation_id, option_id,jud_value) values (%s,%s,%s,%s)""",(o.vote_key,o.votation_id, o.option_id ,o.jud_value) )
    c.close()

if __name__ == '__main__':
    votation_id=4
    conn = dbmanager.get_connection()
    option_array = option.load_options_by_votation(votation_id)
    for i in range(1000):
        print(i)
        user_id = i + 103
        v = vote.vote_dto()
        v.votation_id = votation_id
        v.vote_key = "keyx" + str(user_id)
        for o in option_array:
            v.option_id = o.option_id
            v.jud_value = random.randint(0,len(votation.WORDS)-1)
            insert_dto(v)
    conn.close()
    input("pause...")


