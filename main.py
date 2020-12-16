from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    user_id = Column("user_id", Integer, primary_key=True)
    username = Column('username', String, unique=True)


class Wallets(Base):
    __tablename__ = "wallets"
    owner_id = Column(Integer, ForeignKey(User.user_id))
    user_id = Column("user_id", Integer, primary_key=True)
    name = Column(String)
    uah = Column(Integer)
    owner = orm.relationship(User, backref="wallets", lazy="joined")


engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)
