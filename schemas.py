from Api.models import User, Wallets  # , Head
from marshmallow import Schema

"""
class HeadSchema(Schema):
    class Meta:
        model = Head
        fields = ("head_id", "headname","uah")
"""


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ("user_id", "username", "password")


class WalletsSchema(Schema):
    class Meta:
        model = Wallets
        fields = ("user_id", "name", "uah", "owner_uid")

