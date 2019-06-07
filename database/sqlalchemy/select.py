from declare import Base, User,Votation, DBNAME, Option, Vote, Voter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///' + DBNAME, echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

l = session.query(User).all()
print('users: ', len(l))
for u in l:
    print(u.user_id, u.user_name)

u = session.query(User).filter(User.user_id == 1).first()
if u:
    print(u.user_name)

l = session.query(Votation).all()
print('votations: ', len(l))
for v in l:
    print(v.votation_id, v.promoter_user.user_name, v.votation_description, v.begin_date)


l = session.query(Option).all()
print('options: ', len(l))
for o in l:
    print(o.option_id, o.votation.votation_description,o.option_name)

l = session.query(Vote).all()
print('votes: ', len(l))
for v in l:
    print(v.vote_key,v.votation_id, v.votation.votation_description, v.option_id, v.option.option_name, v.jud_value)

l = session.query(Voter).all()
print('voters: ', len(l))
for v in l:
    print(v.user_id,v.user.user_name, v.votation_id, v.votation.votation_description)
