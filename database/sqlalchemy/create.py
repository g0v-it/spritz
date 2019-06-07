import os
from declare import Base, User,Votation,DBNAME
from sqlalchemy import create_engine

try: 
    os.remove(DBNAME)
except:
    pass



engine = create_engine('sqlite:///' + DBNAME, echo=True)
Base.metadata.create_all(engine)
