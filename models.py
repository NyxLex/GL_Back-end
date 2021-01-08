from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, session
from proj import *

Base = declarative_base()

"""
class Head(Base):
    __tablename__ = "Head"
    head_id = Column("head_id", Integer, primary_key=True)
    headname = Column('headname', String, unique=True)
    uah = Column(Integer)
   # wid = Column(Integer, primary_key=True)
"""


def hash_password(password):
    return generate_password_hash(password).decode('utf-8')


def check_password(self, password):
    return check_password_hash(self.password, password)

class User(Base):
    __tablename__ = "User"
    user_id = Column("user_id", Integer, primary_key=True)
    username = Column('username', String, unique=True)
    password = Column("password", String)



class Wallets(Base):
    __tablename__ = "wallets"
    user_id = Column("user_id", Integer, primary_key=True)
    name = Column('name', String)
    # uah = Column(BigInteger, ForeignKey(User.p_uah))
    uah = Column(BigInteger)
    owner_uid = Column(Integer, ForeignKey(User.user_id))
    owner = orm.relationship(User, backref="wallets", lazy="joined")


class Transactions(Base):
    __tablename__ = "transactions"
    amount = Column(BigInteger)
    user_id = Column(Integer, primary_key=True)
    from_wallet_wid = Column(Integer, ForeignKey(Wallets.user_id))
    to_wallet_wid = Column(Integer, ForeignKey(Wallets.user_id))
    from_wallet = orm.relationship(
        Wallets, foreign_keys=[from_wallet_wid], backref="transactions_from", lazy="joined"
    )
    to_wallet = orm.relationship(
        Wallets, foreign_keys=[to_wallet_wid], backref="transactions_to", lazy="joined"
    )
engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)
