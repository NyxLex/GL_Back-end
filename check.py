from sqlalchemy.orm import sessionmaker
from main import *

Session = sessionmaker(bind=engine)
session = Session()

user = User(user_id=1, username="Sasha ")
user2 = User(user_id=2, username="Masha ")

wallet1 = Wallets(user_id=1, owner_id=1, name="PersonalWallet", uah="200")
wallet2 = Wallets(user_id=2, owner_id=1, name="FamillyWallet", uah="400")
wallet3 = Wallets(user_id=3, owner_id=2, name="PersonalWallet", uah="100")
wallet4 = Wallets(user_id=4, owner_id=2, name="FamillyWallet",uah=wallet1.uah)

session.add(user)
session.add(user2)

session.add(wallet1)
session.add(wallet2)
session.add(wallet3)
session.add(wallet4)

session.commit()

session.close()
