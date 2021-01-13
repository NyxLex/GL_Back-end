from Api.models import *

Session = sessionmaker(bind=engine)
session = Session()
"""
user1 = User(user_id=1, username="Yuriy", password="123")
wallet1 = Wallets(user_id=1, name="Wallet1", uah=210, owner=user1)
wallet2 = Wallets(user_id=2, name="Wallet2", uah=240, owner=user1)
transaction = Transactions(user_id=1, from_wallet=wallet1, to_wallet=wallet2, amount=20)

session.add(user1)
session.add(wallet1)
session.add(wallet2)
session.add(transaction)
"""
session.commit()

session.close()
