from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user")

    created_at = db.Column(db.DateTime, server_default=db.func.now())



    def __repr__(self):
        return f"<User {self.email}>"
    
class Prediction(db.Model):
    
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    income = db.Column(db.Float, nullable=False)

    expense = db.Column(db.Float, nullable=False)

    emi = db.Column(db.Float, nullable=False)

    credit_score = db.Column(db.Integer, nullable=False)

    loan_amount = db.Column(db.Float, nullable=False)

    tenure = db.Column(db.Integer, nullable=False)

    prediction = db.Column(db.String(20), nullable=False)

    probability = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    interest_rate = db.Column(db.Float)

    monthly_emi = db.Column(db.Float)

    total_interest = db.Column(db.Float)

    total_payment = db.Column(db.Float)

    risk = db.Column(db.String(20))

    recommendation = db.Column(db.Text)

    messages = db.relationship(
    "ChatMessage",
    backref="prediction",
    lazy=True,
    cascade="all, delete-orphan"
)

class ChatMessage(db.Model):
    
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)

    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey("predictions.id"),
        nullable=False
    )

    sender = db.Column(db.String(10), nullable=False)   # user / ai

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


class BankLoanRate(db.Model):
    
    __tablename__="bank_loan_rates"


    id=db.Column(
        db.Integer,
        primary_key=True
    )


    bank_name=db.Column(
        db.String(100)
    )


    loan_type=db.Column(
        db.String(50)
    )


    interest_rate=db.Column(
        db.Float
    )


    processing_fee=db.Column(
        db.String(50)
    )


    max_tenure=db.Column(
        db.Integer
    )


    updated_at=db.Column(
        db.DateTime,
        server_default=db.func.now()
    )