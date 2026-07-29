<h1 align="center">
🚀 Smart Loan Advisor System
</h1>

<p align="center">
AI-Powered Loan Prediction Platform built using Machine Learning and Flask
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask">
<img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn">
<img src="https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap">
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite">

</p>

---

# 📌 Overview

Smart Loan Advisor System is an AI-powered fintech web application that predicts loan eligibility using Machine Learning while providing users with an interactive dashboard to manage loan planning and financial decisions.

The system combines Machine Learning, Flask, and a modern responsive UI to simplify loan analysis through intelligent predictions, EMI calculations, bank comparison, and financial insights.

---

# ✨ Features

✅ AI Loan Eligibility Prediction

✅ Explainable AI Recommendations

✅ Interactive Dashboard

✅ Secure Login & Registration

✅ Loan Planner

✅ EMI Calculator

✅ Compare Loan Interest Rates

✅ Loan Prediction History

✅ PDF Report Generation

✅ User Profile Management

✅ Settings Module

✅ Responsive UI

---

# 🧠 Machine Learning Models

The project evaluates multiple ML algorithms for loan prediction:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)

The best-performing model is used for prediction.

---

# 🖥️ Tech Stack

### Backend

- Python
- Flask
- Flask Login
- Flask SQLAlchemy
- Flask Bcrypt

### Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

### Frontend

- HTML
- CSS
- Bootstrap
- JavaScript
- Chart.js

### Database

- SQLite

### Reports

- ReportLab

---

# 🔄 Project Workflow

```text
                         USER
                           │
                           ▼
                 Register / Login
                           │
                           ▼
                  User Dashboard
                           │
                           ▼
                Fill Loan Planner Form
                           │
                           ▼
             Input Validation & Preprocessing
                           │
                           ▼
          Machine Learning Prediction Model
          (Gradient Boosting Classifier)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      Loan Approved              Loan Rejected
             │                           │
             └─────────────┬─────────────┘
                           ▼
            Explainable AI Recommendation
                           │
                           ▼
                 EMI Calculation Module
                           │
                           ▼
               Compare Bank Interest Rates
             (Static Data → Future Live API)
                           │
                           ▼
          Store Prediction in SQL Database
                 (SQLite + SQLAlchemy)
                           │
                           ▼
          Loan History & PDF Report Download
                           │
                           ▼
             AI Financial Assistant (Groq)
```

---

## 📌 Workflow Explanation

### Step 1: User Authentication
- Secure User Registration & Login
- Password Hashing using Flask-Bcrypt

### Step 2: Dashboard
- Personalized dashboard after login
- Quick access to all loan services

### Step 3: Loan Planner
Users enter:
- Age
- Income
- Employment Type
- Credit Score
- Loan Amount
- Existing Debt
- Savings Ratio
- Financial Information

### Step 4: Data Processing
- Input Validation
- Data Cleaning
- Feature Engineering
- Preprocessing

### Step 5: AI Loan Prediction
The trained **Gradient Boosting Machine Learning Model** predicts:
- Loan Approval Status
- Approval Probability

### Step 6: Explainable AI
Provides reasons behind the prediction:
- Positive Factors
- Risk Factors
- Financial Suggestions

### Step 7: EMI Calculator
Calculates:
- Monthly EMI
- Total Interest
- Total Repayment Amount

### Step 8: Bank Comparison
Current Features:
- Compare Interest Rates
- Processing Fees
- Loan Tenure

**Future Enhancement**
- Real-Time Bank Interest Rate API Integration

### Step 9: Database Storage
Prediction details are securely stored using:
- SQLite
- SQLAlchemy ORM

### Step 10: Reports & History
Users can:
- View Prediction History
- Download PDF Reports

### Step 11: AI Financial Assistant
AI chatbot provides:
- Loan Guidance
- Financial Advice
- Budget Recommendations

---


# 🚀 Installation

Clone Repository

```bash
git clone https://github.com/kumkum1404/Smart-Loan-Advisor-System-.git
```

Go inside folder

```bash
cd Smart-Loan-Advisor-System-
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run project

```bash
python run.py
```

---

# 🔮 Future Enhancements

- Real-Time Bank API Integration

- Live Interest Rate Comparison

- Personalized AI Loan Recommendations

- Credit Score Analysis

- Email Notifications / SMS Alerts

- PostgreSQL Cloud Database

---

# 🔗 Project Links

### GitHub

https://github.com/kumkum1404/Smart-Loan-Advisor-System-

### Live Demo

https://loansense-ai-fom6.onrender.com

---

# 👩‍💻 Developer

**Kumkum Manjhi**

Final Year B.Tech CSE Student

⭐ If you like this project, don't forget to star the repository.