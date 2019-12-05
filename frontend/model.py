from config import db

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import Sequence,UniqueConstraint,PrimaryKeyConstraint,ForeignKeyConstraint
from sqlalchemy.orm import relationship

class VotingUser(db.Model):
    """
    The table votinguser contains accounts that login into the system.
    Even if you use an external sso like google or superauth or LDAP, you 
    need to put the username in this table.
    The numeric user_id is referred in other tables.
    The auth_test mode use users in this table with passwords not encripted
    you can insert directly into the table.
    Auth_test.py is for testing purpose only and you shouldn't 
    use it in prod.
    """
    __tablename__ = 'votinguser'
    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_name = Column(String(200), unique=True, nullable=False)
    pass_word = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True)
    verified = Column(Integer, nullable=True )


class Votation(db.Model):
    """
    The votation table holds election with name and some 
    other properties.
    The election is open between begin_date and end_date and the system 
    allow you to vote only in this period.
    The promoter of the election, after the end_date, needs to close
    the election to allow everybody to see results.
    The votation_type is a string as defined in the votation.py module.
    An election, to be complete, needs a set of options and a set of judgements
    (see below).
    """
    __tablename__ = 'votation'
    votation_id = Column(Integer, Sequence('votation_id_seq'), primary_key=True)
    promoter_user_id = Column(Integer, ForeignKey('votinguser.user_id'))
    promoter_user = relationship(VotingUser)
    votation_description = Column(String(500),nullable=False,unique=True)
    description_url = Column(String(500),nullable=False, default="")
    begin_date = Column(DateTime(),nullable=False)
    end_date = Column(DateTime(),nullable=False)
    votation_type = Column(String(10),nullable=False, default='simple')
    votation_status = Column(Integer,nullable=False, default=0)
    list_voters = Column(Integer,nullable=False, default=0)

class Option(db.Model):
    """
    Options are the object of the election.
    For example a list of candidates. 
    Each votation needs a set of options so voters can choose between them.
    The way you can choose options and count and arrange judgements (see below)
    define the election method.
    """
    __tablename__ = 'option'
    __table_args__ = (UniqueConstraint('votation_id','option_name'),)
    option_id = Column(Integer, Sequence('option_id_seq'), primary_key=True)
    votation_id = Column(Integer, ForeignKey('votation.votation_id'))
    votation = relationship(Votation)
    option_name = Column(String(50),nullable=False)
    def __repr__(self):
        return "<Option %d,%d,%s>" % (self.votation_id, self.option_id, self.option_name)

class Judgement(db.Model):
    """
    When a voter give their vote, he set a judgement for one or more
    options.
    Each election needs a set of judgements, for example:
      * Yes/No 
      * Excellent,Good/Bad/Don't know
      * 0,1,2,5,10
    The way you can choose options (see above) and count and arrange judgements 
    define the election method.
    The column jud_value give both an order and a score of the judgement.
    """
    __tablename__ = 'judgement'
    __table_args__ = (PrimaryKeyConstraint('votation_id','jud_value'), )
    votation_id = Column(Integer, ForeignKey('votation.votation_id'))
    votation = relationship(Votation)
    jud_value = Column(Integer, nullable=False)
    jud_name = Column(String(50),nullable=False)
    
class Vote(db.Model):
    """
    A vote in an election bind an option and a judgement.
    For example in a trivial voting system where you can vote only an
    option, you can give "Yes" to that option and "No" to all other options.
    The column vote_key is an hash, calculated by the client and passed to the server.
    The client generate the vote_key using a secret password that only the user
    knows.
    A vote for an election by a user is a set of rows in the "vote" table and all
    have the same vote_key.
    Each time a user put a vote, the system add or update a row in the "voter" table
    and add or update some rows in the "vote" table.
    Since only the user can generate the vote_key, he can change his vote.
    A "select distinct" on the vote_key column give the number of votes.
    """
    __tablename__ = 'vote'
    __table_args__ = (PrimaryKeyConstraint('vote_key','votation_id','option_id'), )
                    #   ForeignKeyConstraint(['option_id','votation_id'], \
                    #                        ['option.votation_id','option.option_id']))
    vote_key = Column(String(128))
    votation_id = Column(Integer,ForeignKey('votation.votation_id'),nullable=False)
    votation = relationship(Votation)
    option_id = Column(Integer,ForeignKey('option.option_id'),nullable=False)
    option = relationship(Option)
    jud_value = Column(Integer, nullable=False)
    def __repr__(self):
        return "<Vote %d,%d,%d>" % (self.votation_id, self.option_id, self.jud_value)
    
class Voter(db.Model):
    """
    The voter table has a double purpose:
      1. it records if a user voted in a election
      2. it contains all users allowed to vote in a election
    If everybody are allowed to vote, initially the system don't
    insert any row for that election.
    If the promoter wants to restrict the access of the election, the system
    inserts some user_id in the voter table.
    When the user put a vote, the system insert the row (if necessary) and
    set to 1 the "voted" column.
    """
    __tablename__ = 'voter'
    __table_args__ = (PrimaryKeyConstraint('user_id','votation_id'), )
    user_id = Column(Integer, ForeignKey('votinguser.user_id'))
    user = relationship(VotingUser)
    votation_id = Column(Integer,ForeignKey('votation.votation_id'),nullable=False)
    votation = relationship(Votation)
    voted = Column(Integer)

