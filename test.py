from flask_testing import TestCase

from Api.models import Base
from Api.main import *
from Api.models import User, Wallets

from sqlalchemy.util import b64encode

engine = create_engine('sqlite:///database.db', echo=True, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine


class Tests(TestCase):
    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 5000

    def create_app(self):
        return app

    def setUp(self):
        session = Session()
        Base.metadata.drop_all()
        Base.metadata.create_all()
        user = User(user_id=1, username="Yurii",
                    password="$2b$12$JocZlwrAvWHczuyydKjUjeTuYkuPmRJfKE3llexSEkha7c1v5ofVq")
        user1 = User(user_id=2, username="Nyx", password="$2b$12$JocZlwrAvWHczuyydKjUjeTuYkuPmRJfKE3llexSEkha7c1v5ofVq")
        user2 = User(user_id=3, username="Lex", password="$2b$12$JocZlwrAvWHczuyydKjUjeTuYkuPmRJfKE3llexSEkha7c1v5ofVq")

        wallet1 = Wallets(user_id=1, name="Wallet1", uah=210, owner_uid=2)
        wallet2 = Wallets(user_id=2, name="Wallet2", uah=240, owner_uid=1)

        #   transaction = Transactions(user_id=1, from_wallet=wallet1, to_wallet=wallet2, amount=20)
        session.add(user)
        session.add(user1)
        session.add(user2)
        session.add(wallet1)
        session.add(wallet2)
        #  session.add(transaction)
        session.commit()


class Tests_Controller(Tests):
    def test_get_all_users(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.get("/user", headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(200, test.status_code)

    def test_get_all_users_wrong_req(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.get("/user/", headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(404, test.status_code)

    def test_get_all_users_wrong_auth(self):
        credentials = b64encode(b"Yuri:1234")
        test = self.client.get("/user", headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(401, test.status_code)



    def test_post_user(self):
        exist = self.client.post("/user",
                               data={"user_id": 4, "username": "Yu", "password": "1234", })
        print(exist.data)
        self.assertEqual(201, exist.status_code)

    def test_post_user_wrong_req(self):
        exist = self.client.post("/user/",
                               data={"user_id": 4, "username": "Yu", "password": "1234", })
        print(exist.data)
        assert exist.status_code == 404



    def test_put_user(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.put("/user", headers={"Authorization": f"Basic {credentials}"},
                              data={"username": "Vasiliy"})
        print(exist.data)
        assert exist.status_code == 200

    def test_put_user_wrong_req(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.put("/user/", headers={"Authorization": f"Basic {credentials}"},
                              data={"username": "Vasiliy"})
        print(exist.data)
        assert exist.status_code == 404

    def test_put_user_wrong_auth(self):
        credentials = b64encode(b"Yurii_wrong:1234")
        exist = self.client.put("/user", headers={"Authorization": f"Basic {credentials}"},
                              data={"username": "Vasiliy"})
        print(exist.data)
        assert exist.status_code == 401



    def test_get_user_by_id(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.get("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert exist.status_code == 200

    def test_get_user_by_id_wrong(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.get("/user/10a", headers={"Authorization": f"Basic {credentials}"})
        assert exist.status_code == 404

    def test_get_user_by_id_wrong_auth(self):
        credentials = b64encode(b"Yuri:1234")
        exist = self.client.get("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert exist.status_code == 401



    def test_delete_user_wrong_auth(self):
        credentials = b64encode(b"wrong_user:1234")
        exist = self.client.delete("/user", headers={"Authorization": f"Basic {credentials}"})
        assert exist.status_code == 401

    def test_delete_user_wrong_req(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.delete("/user/", headers={"Authorization": f"Basic {credentials}"})
        assert exist.status_code == 404

    def test_user_delete(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.delete("/user", headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(204, test.status_code)

    # Wallets
    def test_get_wallet(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.get("/wallet/1/get_wallet", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(200, test.status_code)

    def test_get_wallet_wrong_user(self):
        credentials = b64encode(b"wrong:1234")
        test = self.client.get("/wallet/1/get_wallet", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(401, test.status_code)

    def test_get_wallet_wrong_id(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.get("/wallet/100/get_wallet", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(404, test.status_code)

    def test_post_wallet_invalid_input(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.post("/wallet/", headers={"Authorization": f"Basic {credentials}"},
                               data={"user_id": 9,
                                     "name": "Wallet",
                                     "uah": 100,
                                     "owner_uid": 10})
        print(exist.data)
        self.assertEqual(405, exist.status_code)

    def test_wallet_put_wrong(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.put("/wallet/4/change", headers={"Authorization": f"Basic {credentials}"},
                               data={"user_id": 4, "name": "mywallet2", "uah": 100, "owner_uid": 4, })
        print(test.data)
        self.assertEqual(404, test.status_code)

    def test_wallet_put(self):
        credentials = b64encode(b"Yurii:1234")
        test = self.client.put("/wallet/1/change", headers={"Authorization": f"Basic {credentials}"},
                               data={"name": "my_wallet2", })
        print(test.data)
        self.assertEqual(405, test.status_code)

    def test_delete_wallet(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.delete("/wallet/1/delete", headers={"Authorization": f"Basic {credentials}"})
        print(exist.status_code)
        assert exist.status_code == 200

    def test_delete_wallet_wrong_id(self):
        credentials = b64encode(b"Yurii:1234")
        exist = self.client.delete("/wallet/100/delete", headers={"Authorization": f"Basic {credentials}"})
        print(exist.status_code)
        assert exist.status_code == 404

    def test_delete_wallet_wrong_auth(self):
        credentials = b64encode(b"Yurii21:1234")
        exist = self.client.delete("/wallet/1/delete", headers={"Authorization": f"Basic {credentials}"})
        print(exist.status_code)
        assert exist.status_code == 401

