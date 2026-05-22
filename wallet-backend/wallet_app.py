# routes for users- user login, user register, get all users, deleteuser
# routes for transactions- get all, update, add, delete

from urllib import response

from flask import Flask, jsonify, request, session
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re
import jwt
from datetime import datetime, timedelta
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wallet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]= "wallet-secret-key"

db = SQLAlchemy(app)
# user model:
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    password = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(20), default="Standard")
    wallet_balance = db.Column(db.Float, default=1000.0)
    cashback = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)

    transactions = db.relationship("Transaction", backref="user", lazy=True)

    def get_fee_rate(self):
        return 0.01 if self.account_type == "premium" else 0.02
    
    def get_transaction_limit(self):
        return 50000 if self.account_type == "premium" else 10000



    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "account_type": self.account_type,
            "wallet_balance": self.wallet_balance,
            "cashback": self.cashback,
            "is_active": self.is_active

        }
    
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, default=0.0)
    net_amount = db.Column(db.Float, default=0)
    date = db.Column(db.String(30), default=lambda: datetime.now().strftime("%Y-%m-%d"))



    def to_dict(self):
        return{
            "id": self.id,
            "userId": self.user_id,
            "type": self.type,
            "amount": self.amount,
            "fee": self.fee,
            "net_amount": self.net_amount,
            "date": self.date
        }


# utility function to validate password:
def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z@\d]{8,}$'
    return bool(re.fullmatch(pattern, password))

#   create the tables
with app.app_context():
    db.create_all()
    print("Tables created")

# wrapper to check token:
from functools import wraps
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer"):
            return jsonify({"error":"Token missing"})
        token = token.split()[1]
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = db.session.get(User, payload["user_id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"})
        except Exception:
            return jsonify({"error": "Invalid token"})
        return f(current_user, *args, **kwargs)
    return decorated


# home route:
@app.route("/")
def home():
    return jsonify({
        "message": " The wallet app API is running"
    })

# user routes:

# 1. get all the users:
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# 2. get user by id:
@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404

# add user: 
@app.route("/api/users", methods=["POST"])
def register():
    data = request.get_json()

    # basic json check
    # handle cases where get_json returned a string (malformed content-type)
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = None

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # validate:
    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"error": "First name and Last name are missing"}), 400
    if not data.get("password"):
        return jsonify({"error": "password required"}), 400
    
    if not validate_password(data["password"]):
        return jsonify({
            "error": " Password must contain 8+ chars, uppercase, lowercase, digits"
        })
    
    # checking for duplicate users:
    existing = User.query.filter_by(
        first_name = data["first_name"],
        last_name = data["last_name"]
    ).first()

    if existing:
        return jsonify({"error": "User already exists"})
    
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        address=data.get("address"),
        password=data["password"],
        account_type=data.get("account_type", "Standard"),
        wallet_balance=1000.0
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


# PUT method to update profile:
@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"})
    
    data = request.get_json()

    if "first_name" in data: user.first_name = data["first_name"]
    if "last_name" in data: user.last_name = data["last_name"]
    if "address" in data: user.address = data["address"]
    if "account_type" in data: user.account_type = data["account_type"]
    if "is_active" in data: user.is_active = data["is_active"]

    db.session.commit()
    return jsonify(user.to_dict())

# login:
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    user  = User.query.filter_by(
        first_name = data.get("first_name"),
        last_name = data.get("last_name")
    ).first()

    if not user or user.password != data.get("password"):
        return jsonify({"error": "invalid credentials"})

    payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=1)}
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
        response

    
    return jsonify({"token": token, "user": user.to_dict()})
   
# logout:
# @app.route("/api/logout", methods=["POST"])
# def logout():
#     session.pop("user_id", None)
#     return jsonify({"message":"Logged out successfully"})

    


# get transactions:
@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    user_id = request.args.get("userId")

    if user_id:
        txns = Transaction.query.filter_by(user_id=user_id).all()
    else:
        txns = Transaction.query.all()

    return jsonify([t.to_dict() for t in txns])

# get transaction by id:
@app.route("/api/transactions/<int:txn_id>", methods=["GET"])
def get_transaction(txn_id):
    txn = db.session.get(Transaction, txn_id)
    if not txn:
        return jsonify({"error": "Transaction not found"})
    return jsonify(txn.to_dict())



# add transaction:
@app.route("/api/transactions", methods=["POST"])
@token_required
def add_transaction(current_user):
    

    data = request.get_json()

    amount = data.get("amount")

    if not amount or float(amount) <= 0:
        return jsonify({"error": " invalid amount"})
    
    txn_type = data.get("type")
    if txn_type not in ["credit", "debit"]:
        return jsonify({"error": " invalid transaction type"})
    
    
    

    amount = float(amount)

    if amount> current_user.get_transaction_limit():
        return jsonify({
            "error": f"exceeds the limit of {current_user.get_transaction_limit()}"
        })
    
    fee = round(amount * current_user.get_fee_rate(), 2)
    net_amount = round( amount - fee if txn_type == "credit" else -(amount+ fee),2)

    if txn_type == "debit" and current_user.wallet_balance + net_amount <0:
        return jsonify({"error": "low balance"})
    
    txn = Transaction(
        user_id = current_user.id,
        type = txn_type,
        amount = amount,
        fee = fee,
        net_amount= net_amount,
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    )
    db.session.add(txn)

    current_user.wallet_balance = round(current_user.wallet_balance + net_amount, 2)
    if current_user.account_type == "Premium" and txn_type =="credit":
        current_user.cashback = round(current_user.cashback + amount* 0.05, 2)

    db.session.commit()

    return jsonify(txn.to_dict())

# delete:
@app.route("/api/transactions/<int:txn_id>", methods=["DELETE"])
def delete_transaction(txn_id):
    txn = db.session.get(Transaction, txn_id)
    if not txn:
        return jsonify({"error": "Transactions not found"})
    
    user = db.session.get(User, txn.user_id)
    if user:
        user.wallet_balance = round(user.wallet_balance - txn.net_amount, 2)

    db.session.delete(txn)
    db.session.commit()
    return jsonify({"message": " Transaction deleted", "id": txn_id})

# refresh the token:
@app.route("/api/refresh", methods=["POST"])
def refresh_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer"):
        return jsonify({"error": "missing token"})
    token = token.split()[1]
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"], options={"verify_exp": False})
        new_payload = {"user_id": payload["user_id"], "exp": datetime.utcnow()+ timedelta(minutes=10)}
        new_token = jwt.encode(new_payload, app.config["SECRET_KEY"], algorithm="HS256")
        if isinstance(new_token, bytes):
            new_token = new_token.decode("utf-8")
        return jsonify({"token": new_token})
    except Exception:
        return jsonify({"error": "invalid request"})


if __name__ == "__main__":
    app.run(debug=True)