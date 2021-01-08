from flask import Flask, jsonify, request, abort
from flask_restful import reqparse, fields, Resource, marshal_with


from proj import *
from check_models import Session
from schemas import UserSchema, WalletsSchema
from models import User, Wallets, hash_password


# validation
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(405)
def wrong(e):
    return jsonify(error=str(e)), 405


@app.route('/wallet/<int:user_id>/get_wallet', methods=['GET'])
def get_wallet(user_id):
    session = Session()
    try:
        wallet = session.query(Wallets).filter_by(user_id=int(user_id)).one()
    except:
        abort(404, description="Wallet not found")
    return WalletsSchema().dump(wallet)


@app.route('/wallet/', methods=['POST'])
def create_wallet():
    session = Session()

    data = request.get_json()

    try:
        wallet = Wallets(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405
    #  if not "owner_uid" != User.user_id:
    #     abort(404, description="Wallet owner not found")

    session.add(wallet)
    session.commit()

    return jsonify({"Success": "Wallet has been created"}), 200


@app.route('/wallet/<int:user_id>/change', methods=['PUT'])
def update_wallet(user_id):
    session = Session()
    try:
        wallet = session.query(Wallets).filter_by(user_id=int(user_id)).one()
    except:
        abort(404, description="Wallet not found")

    data = request.get_json()
    try:

        if data.get('name', None):
            wallet.name = data['name']


    except:
        abort(405, description="Invalid input")

    session.commit()

    return jsonify({"Success": "Wallet has been changed"}), 200


@app.route('/wallet/<int:user_id>/delete', methods=['DELETE'])
def delete_wallet(user_id):
    session = Session()
    try:
        wallet = session.query(Wallets).filter_by(user_id=int(user_id)).one()
    except:
        abort(404, description="Wallet not found")

    session.delete(wallet)

    session.commit()

    return jsonify({"Success": "Wallet has been deleted"}), 200


@app.route('/user/<int:user_id>/get_user', methods=['GET'])
def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=int(user_id)).one()
    except:
        abort(404, description="User not found")
    return UserSchema().dump(user)


@app.route('/user/', methods=['POST'])
def create_user():
    session = Session()

    data = request.get_json()

    try:
        user = User(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405

    user.hash_password()

    session.add(user)
    session.commit()

    return jsonify({"Success": "User has been created"}), 200


@app.route('/user/<int:user_id>/delete_user', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=int(user_id)).one()
    except:
        abort(404, description="User not found")

    session.delete(user)

    session.commit()

    return jsonify({"Success": "User has been deleted"}), 200


"""


@auth.verify_password
def verify_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, required=True)
user_put_args.add_argument("password", type=str, required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("user_id", type=int)
user_update_args.add_argument("username", type=str)
user_update_args.add_argument("password", type=str)

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'password': fields.String

}


class UserApi(Resource):
    @auth.login_required
    @marshal_with(user_fields)
    def get(self):
        session = Session()
        exist = session.query(User).all()
        if not exist:
            abort(404, message="No one user in database")
        return exist

    @marshal_with(user_fields)
    def post(self):
        session = Session()
        args = user_put_args.parse_args()
        exist = User(username=args['username'], password=hash_password(args['password']) )
        session.add(exist)
        session.commit()
        return exist, 201

    @auth.login_required
    @marshal_with(user_fields)
    def put(self):
        session = Session()
        args = user_update_args.parse_args()
        # result = session.query(User).filter_by(id=user_id).first()
        exist = auth.current_user()
        if not exist:
            abort(404, message="User doesn't exist, cannot update")
        if args['username']:
            exist.username = args['username']
        if args['password']:
            exist.password = hash_password(args['password'])

        exist = session.merge(exist)
        session.add(exist)
        session.commit()

        return exist

    @auth.login_required
    def delete(self, user_id):
        session = Session()
        # result = session.query(User).filter_by(id=user_id).first()
        exist = auth.current_user()
        if not exist:
            abort(500, message="User doesn't exist, cannot delete")
        result = session.merge(exist)
        session.delete(exist)
        session.commit()
        return "User deleted", 204
#api.add_resource(UseridApi, "/user/<int:user_id>")
api.add_resource(UserApi, "/user")
"""


"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
engine = create_engine('sqlite:///database.db', echo=True, connect_args={'check_same_thread': False})
api = Api(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()
Session = sessionmaker(bind=engine)
Session = scoped_session(Session)
"""

if __name__ == "__main__":
    app.run(debug=True)
