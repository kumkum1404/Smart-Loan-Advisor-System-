
from app import create_app
from flask import render_template, request, redirect, url_for, flash,  session
from app.models import db, User, Prediction , ChatMessage , BankLoanRate
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.ml.predict import predict_loan
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import os
import os
from app.ai.groq_ai import get_ai_advice
from app.ai.groq_ai import chat_with_ai
from flask import jsonify





print("Current Folder :", os.getcwd())
print("Database Path :", os.path.abspath("instance/loan_prediction.db"))

app = create_app()
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Email already exists?
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("login"))

    return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        print("Entered Email:", email)

        user = User.query.filter_by(email=email).first()

        print("User Found:", user)

        if user:
            print("Password Match:", bcrypt.check_password_hash(user.password, password))

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            flash("Login Successful!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("auth/login.html")
    

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully", "success")

    return redirect(url_for("home"))

@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():

    Prediction.query.filter_by(user_id=current_user.id).delete()

    db.session.delete(current_user)

    db.session.commit()

    logout_user()

    flash("Your account has been deleted successfully.", "success")

    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():

    predictions = Prediction.query.filter_by(
        user_id=current_user.id
    ).all()

    total_predictions = len(predictions)

    approved = sum(
        1 for p in predictions
        if p.prediction == "Approved"
    )

    rejected = total_predictions - approved

    approval_rate = 0

    if total_predictions:
        approval_rate = round(
            approved / total_predictions * 100,
            2
        )

    latest = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    return render_template(

        "dashboard/dashboard.html",

        total_predictions=total_predictions,

        approved=approved,

        rejected=rejected,

        approval_rate=approval_rate,

        latest=latest

    )

@app.route("/planner")
@login_required
def planner():
    session.pop("new_prediction", None)
    return render_template(
        "loan/planner.html",
        user=current_user
    )

@app.route("/predict", methods=["POST"])
@login_required
def predict():

    import math

    # -----------------------------
    # Get Form Values
    # -----------------------------

    income = float(request.form["income"])
    expense = float(request.form["expense"])
    emi_existing = float(request.form["emi"])
    savings = float(request.form["savings"])
    credit_score = int(request.form["credit_score"])

    loan_amount = float(request.form["loan_amount"])
    tenure = int(request.form["tenure"])      # Months

    # -----------------------------
    # Data for ML Model
    # -----------------------------

    data = {

        "Age": int(request.form["age"]),
        "Gender": request.form["gender"],
        "Married": request.form["married"],
        "Dependents": int(request.form["dependents"]),
        "Education": request.form["education"],
        "Employment_Type": request.form["employment"],
        "Monthly_Income": income,
        "Monthly_Expenses": expense,
        "Existing_EMI": emi_existing,
        "Savings": savings,
        "Credit_Score": credit_score,
        "Credit_History": int(request.form["credit_history"]),
        "Loan_Type": request.form["loan_type"],
        "Loan_Amount": loan_amount,
        "Loan_Tenure": tenure,
        "Property_Area": request.form["property_area"]

    }

    # -----------------------------
    # AI Prediction
    # -----------------------------

    prediction, probability = predict_loan(data)

    prediction = str(prediction)
   


    # -----------------------------
    # Interest Rate Suggestion
    # -----------------------------

    if credit_score >= 800:
        interest_rate = 8.25

    elif credit_score >= 750:
        interest_rate = 8.50

    elif credit_score >= 700:
        interest_rate = 9.00

    elif credit_score >= 650:
        interest_rate = 10.00

    else:
        interest_rate = 11.50

    # -----------------------------
    # EMI Calculation
    # -----------------------------

    monthly_rate = interest_rate / (12 * 100)

    months = tenure

    monthly_emi = (
        loan_amount
        * monthly_rate
        * pow(1 + monthly_rate, months)
    ) / (
        pow(1 + monthly_rate, months) - 1
    )

    monthly_emi = round(monthly_emi, 2)

    # -----------------------------
    # Total Interest & Payment
    # -----------------------------

    total_payment = round(monthly_emi * months, 2)

    total_interest = round(
        total_payment - loan_amount,
        2
    )

    # -----------------------------
    # Salary Analysis
    # -----------------------------

    safe_emi = round(income * 0.30, 2)

    emi_ratio = round((monthly_emi / income) * 100, 2)

    if monthly_emi <= safe_emi:

        affordability = "Yes"

        risk = "Low"

        recommendation = (
            "Your income can comfortably support this loan. "
            "The EMI is within the recommended limit."
        )

    elif monthly_emi <= income * 0.45:

        affordability = "Moderate"

        risk = "Medium"

        recommendation = (
            "The loan is affordable, but your monthly repayment burden "
            "will be moderate."
        )

    else:

        affordability = "No"

        risk = "High"

        recommendation = (
            "The EMI is high compared to your income. "
            "Consider reducing the loan amount or increasing the tenure."
        )

    
# -----------------------------
# AI Financial Advisor
# -----------------------------

    ai_advice = get_ai_advice(

       age=data["Age"],
       income=income,
       loan_amount=loan_amount,
       credit_score=credit_score,
       financial_score=probability,
       prediction=prediction,
       emi=monthly_emi
    )
    # -----------------------------
    # Bank Offers
    # -----------------------------

    if prediction == "Approved":

        bank_offers = [

            {
                "bank": "State Bank of India",
                "interest": "8.50%",
                "tenure": "30 Years"
            },

            {
                "bank": "HDFC Bank",
                "interest": "8.65%",
                "tenure": "25 Years"
            },

            {
                "bank": "ICICI Bank",
                "interest": "8.75%",
                "tenure": "30 Years"
            },

            {
                "bank": "Axis Bank",
                "interest": "8.90%",
                "tenure": "20 Years"
            }

        ]

    else:

        bank_offers = []

    # -----------------------------
    # Save History
    # -----------------------------
    history = Prediction(


    user_id=current_user.id,

    income=income,

    expense=expense,

    emi=emi_existing,

    credit_score=credit_score,

    loan_amount=loan_amount,

    tenure=tenure,

    prediction=prediction,

    probability=probability,

    interest_rate=interest_rate,

    monthly_emi=monthly_emi,

    total_interest=total_interest,

    total_payment=total_payment,

    risk=risk,

    recommendation=recommendation

)

    db.session.add(history)

    db.session.commit()
    session["prediction_id"] = history.id

    session["new_prediction"] = True

    chat_history = ChatMessage.query.filter_by(
    prediction_id=history.id
    ).order_by(ChatMessage.id.asc()).all()

    # -----------------------------
    # Result Page
    # ----------------------------
    return render_template(


    "loan/result.html",

    prediction=prediction,

    probability=probability,
    recommendation=recommendation,

    bank_offers=bank_offers,

    income=income,

    expense=expense,

    emi_existing=emi_existing,

    loan_amount=loan_amount,

    tenure=tenure,

    interest_rate=interest_rate,

    monthly_emi=monthly_emi,

    total_interest=total_interest,

    total_payment=total_payment,

    safe_emi=safe_emi,

    emi_ratio=emi_ratio,

    affordability=affordability,

    risk=risk,
    ai_advice=ai_advice,

   chat_history=chat_history

)


#FOR CHATBOT
@app.route("/chat", methods=["POST"])
@login_required
def chat():

    message = request.json.get("message")
    prediction_id = session.get("prediction_id")

    user_chat = ChatMessage(

        prediction_id=prediction_id,

        sender="user",

        message=message

    )

    db.session.add(user_chat)

    latest = Prediction.query.get(prediction_id)
    if latest is None:

        return jsonify({

            "reply":"Please analyze your loan first."

        })

    previous_messages = ChatMessage.query.filter_by(
        prediction_id=prediction_id
    ).order_by(
        ChatMessage.created_at.asc()
    ).all()

    chat_history = ""
    for msg in previous_messages:
        chat_history += f"""
    {msg.sender}: {msg.message}
    """

    report = f"""

Monthly Income : ₹{latest.income}

Monthly Expense : ₹{latest.expense}

Credit Score : {latest.credit_score}

Loan Amount : ₹{latest.loan_amount}

Monthly EMI : ₹{latest.monthly_emi}

Interest Rate : {latest.interest_rate}%

Prediction : {latest.prediction}

Approval Probability : {latest.probability}%

Risk Level : {latest.risk}

Recommendation :

{latest.recommendation}

"""
    reply = chat_with_ai(
        message,

        report + "\n\nPrevious Conversation:\n" + chat_history

    )

    # Save AI Reply

    ai_chat = ChatMessage(

        prediction_id=prediction_id,

        sender="ai",

        message=reply

    )

    db.session.add(ai_chat)

    db.session.commit()

    return jsonify({

        "reply":reply

    })

@app.route("/history")
@login_required
def history():

    predictions = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    return render_template(
        "loan/history.html",
        predictions=predictions
    )

@app.route("/emi", methods=["GET", "POST"])
@login_required
def emi():

    if request.method == "POST":

        principal = float(request.form["loan_amount"])

        annual_rate = float(request.form["interest"])

        years = int(request.form["tenure"])

        monthly_rate = annual_rate / 12 / 100

        months = years * 12

        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

        total_payment = emi * months

        total_interest = total_payment - principal

        return render_template(

            "loan/emi_result.html",

            emi=round(emi, 2),

            total_payment=round(total_payment, 2),

            total_interest=round(total_interest, 2)

        )
    
    # if request.headers.get("X-Requested-With") == "XMLHttpRequest":
    
    #     return render_template(
    #         "loan/emi_content.html"
    #     )

    return render_template("loan/emi_calculator.html")


@app.route("/compare-banks")
@login_required
def compare_banks():

    banks = [

        {
            "name": "SBI Bank",
            "rate": 8.5,
            "fee": "₹5000",
            "tenure": 30
        },

        {
            "name": "HDFC Bank",
            "rate": 8.7,
            "fee": "₹6000",
            "tenure": 25
        },

        {
            "name": "ICICI Bank",
            "rate": 9.4,
            "fee": "₹5500",
            "tenure": 25
        },

        {
            "name": "Axis Bank",
            "rate": 9.0,
            "fee": "₹6000",
            "tenure": 20
        },

    ]


    # AI recommendation logic

    best_bank = min(
        banks,
        key=lambda x: x["rate"]
    )


    return render_template(

        "loan/compare_banks.html",

        banks=banks,

        best_bank=best_bank

    )


from flask import send_file
import os
import tempfile

@app.route("/report")
@login_required
def report():

    latest = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    if not latest:
        flash("No prediction history found.", "warning")
        return redirect(url_for("history"))

    # Temporary PDF file
    pdf_path = os.path.join(tempfile.gettempdir(), "loan_report.pdf")

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Loan Prediction Report</b>", styles["Title"]))
    story.append(Paragraph(f"User: {current_user.full_name}", styles["Normal"]))
    story.append(Paragraph(f"Email: {current_user.email}", styles["Normal"]))
    story.append(Paragraph(f"Loan Amount: ₹ {latest.loan_amount}", styles["Normal"]))
    story.append(Paragraph(f"Income: ₹ {latest.income}", styles["Normal"]))
    story.append(Paragraph(f"Credit Score: {latest.credit_score}", styles["Normal"]))
    story.append(Paragraph(f"Prediction: {latest.prediction}", styles["Normal"]))
    story.append(Paragraph(f"Confidence: {latest.probability}%", styles["Normal"]))

    doc.build(story)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="Loan_Report.pdf",
        mimetype="application/pdf"
    )


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        current_user.full_name = request.form["full_name"]

        password = request.form["password"]

        if password:

            current_user.password = bcrypt.generate_password_hash(
                password
            ).decode("utf-8")

        db.session.commit()

        flash("Profile Updated Successfully!", "success")

        return redirect(url_for("settings"))

    return render_template("settings/settings.html")

@app.route("/profile")
@login_required
def profile():

    return render_template("profile/profile.html")

@app.route("/create_admin")
def create_admin():

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if admin:
        return "Admin already exists."

    password = bcrypt.generate_password_hash("admin123").decode("utf-8")

    admin = User(
        full_name="Administrator",
        email="admin@gmail.com",
        password=password,
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    return "Admin Created Successfully!"


@app.route("/admin")
@login_required
def admin():

    if current_user.role != "admin":

        flash("Access Denied!", "danger")

        return redirect(url_for("dashboard"))

    users = User.query.all()

    predictions = Prediction.query.order_by(
        Prediction.created_at.desc()
    ).all()

    total_users = len(users)

    total_predictions = len(predictions)

    approved = sum(
        1 for p in predictions
        if p.prediction == "Approved"
    )

    rejected = sum(
        1 for p in predictions
        if p.prediction == "Rejected"
    )

    approval_rate = 0

    if total_predictions > 0:
        approval_rate = round(
            approved / total_predictions * 100,
            2
        )

    return render_template(

        "admin/dashboard.html",

        users=users,

        predictions=predictions,

        total_users=total_users,

        total_predictions=total_predictions,

        approved=approved,

        rejected=rejected,

        approval_rate=approval_rate

    )

@app.route("/check_users")
def check_users():

    users = User.query.all()

    output = ""

    for user in users:
        output += f"""
        <b>Name:</b> {user.full_name}<br>
        <b>Email:</b> {user.email}<br>
        <b>Role:</b> {user.role}<br>
        <hr>
        """

    return output

@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):

    if current_user.role != "admin":

        flash("Access Denied!", "danger")

        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    if user.role == "admin":

        flash("Admin account cannot be deleted.", "warning")

        return redirect(url_for("admin"))

    Prediction.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)

    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for("admin"))

@app.route("/test-ai")   #GROQ AI Test Route
def test_ai():

    advice = get_ai_advice(
        age=25,
        income=50000,
        loan_amount=800000,
        credit_score=760,
        financial_score=85,
        prediction="Approved",
        emi=14500
    )

    return f"<h2>AI Financial Advisor</h2><br>{advice}"

if __name__ == "__main__":
    app.run(debug=True)