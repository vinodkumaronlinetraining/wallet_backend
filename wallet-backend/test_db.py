from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # entry point


# creating the file test.db and add path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# create database object:
db = SQLAlchemy(app)


# creating the table:
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    city = db.Column(db.String(50), default="Hyd")

    def __repr__(self):
        return f"Student({self.name}, {self.age})"
    

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))

    transactions = db.relationship("Transaction", backref="user", lazy=True)
    #                              model name,     txn.user

    def __repr__(self):
        return f"User({self.first_name})"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            
        }

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)

    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False )
#                                                   tablename.columnname

    def __repr__(self):
        return f" Transaction ({self.amount}), user_id=({self.user_id})"
    
with app.app_context():
    db.create_all()
    print("Table created")

# add data:
with app.app_context():
    s1 = Student(name="Vinod", age=40, city="banglore")
    s2 = Student(name="Kiran", age=30, city="banglore")
    s3 = Student(name="kumar", age=25, city="Hyd")


    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)

    u1 = User(first_name="vinod")
    u2 = User(first_name="Kiran")
    t1 = Transaction(amount=100, user=u1)
    t2 = Transaction(amount=200, user=u1)
    t3 = Transaction(amount=50, user=u2)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)

    db.session.commit()
    print("Data added")

# Read data:
with app.app_context():
    all_students = Student.query.all()
    print("All students: ", all_students)

    # Users:
    all_Users = User.query.all()
    print("All Users:", all_Users)

    # Transactions:
    all_Txns = Transaction.query.all()
    print("All transactions:", all_Txns)

    # filtered transaction:
    user = db.session.get(User, 1)
    if user:
        print(user.to_dict())
    else:
        print("no user found")

    # # get by id:
    # student = Student.query.get(1)
    # print("Student 1:", student)

    # # filter:
    # banglore = Student.query.filter_by(city="banglore").all()
    # print("In banglore: ", banglore)

    # # filter with condition:
    # young = Student.query.filter(Student.age <35).all()
    # print("Under 35:", young)

# # update:
# with app.app_context():
#     student = Student.query.get(1)
#     student.city = "Chennai"
#     db.session.commit()
#     print("Updated data:", student.city)
# # delete:

# with app.app_context():
#     student = Student.query.get(2)
#     db.session.delete(student)
#     db.session.commit()
#     print("Deleted student 2")

