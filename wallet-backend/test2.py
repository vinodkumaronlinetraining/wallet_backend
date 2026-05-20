from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdata.db"
db = SQLAlchemy(app)


#  user model:
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))

    transactions = db.relationship("Transaction", backref="user", lazy=True)
    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "city": self.city
        }
    
#  transaction model:
class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)

    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "user_id": self.user_id
        }

@app.route("/")
def home():
    return "Flask Users Api is running"

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"})


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "first_name" not in data:
        return jsonify({"error": "First name should be required"}), 400
    
    user = User(
        first_name= data["first_name"],
        city = data.get("city")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    data = request.get_json()
    user.first_name = data.get("first_name", user.first_name)
    user.city = data.get("city" , user.city)

    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted"})


# transaction routes:
@app.route("/users/<int:id>/transactions", methods=["GET"])
def get_user_transactions(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": " User not found"}), 404
    return jsonify([t.to_dict() for t in user.transactions])

@app.route("/users/<int:id>/transactions", methods=["POST"])
def add_transaction(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": " User not found"}), 404
    data = request.json
    if not data or "amount" not in data:
        return jsonify({"error":"missing data of amount"})
    
    txn = Transaction(amount=data["amount"], user=user)

    db.session.add(txn)
    db.session.commit()
    return jsonify(txn.to_dict())


if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


