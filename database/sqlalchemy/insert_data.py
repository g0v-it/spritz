from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declare import Votation,User, Base, DBNAME, Option, Vote
from datetime import datetime

engine = create_engine('sqlite:///' + DBNAME, echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

new_user = User(user_name="aldo",pass_word='aldo')
session.add(new_user)
new_user = User(user_name="beppe",pass_word='beppe')
session.add(new_user)
new_user = User(user_name="carlo",pass_word='carlo')
session.add(new_user)
session.commit()

v = Votation(promoter_user_id = 1, \
    votation_description = "vot prova 1", \
    begin_date = datetime.now(), \
    end_date = datetime.now() )
session.add(v)
v = Votation(promoter_user_id = 2, \
    votation_description = "vot prova 2", \
    begin_date = datetime.today(), \
    end_date = datetime.today() )
session.add(v)

session.commit()

o = Option(option_name='opt1', votation_id = 1)
session.add(o)
o = Option(option_name='opt2', votation_id = 1)
session.add(o)
o = Option(option_name='opt1', votation_id = 2)
session.add(o)
o = Option(option_name='opt2', votation_id = 2)
session.add(o)

session.commit()

v = Vote(vote_key='key_test_1', votation_id=1, option_id=1, jud_value=1)
session.add(v)
v = Vote(vote_key='key_test_2', votation_id=1, option_id=1, jud_value=1)
session.add(v)
v = Vote(vote_key='key_test_3', votation_id=2, option_id=3, jud_value=2)
session.add(v)

# wrong insert:
v = Vote(vote_key='key_test_4', votation_id=2, option_id=1, jud_value=0)
session.add(v)

session.commit()
    


