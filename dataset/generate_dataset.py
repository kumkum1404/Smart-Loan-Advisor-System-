import random
import pandas as pd

random.seed(42)

NUM_RECORDS = 5000

employment_types = [
    "Government",
    "Private",
    "Business",
    "Self Employed"
]

loan_types = [
    "Personal",
    "Home",
    "Vehicle",
    "Education"
]

property_areas = [
    "Urban",
    "Semiurban",
    "Rural"
]

education = [
    "Graduate",
    "Not Graduate"
]

genders = [
    "Male",
    "Female"
]

married = [
    "Yes",
    "No"
]

records = []

for _ in range(NUM_RECORDS):

    age = random.randint(21, 60)

    gender = random.choice(genders)

    married_status = random.choice(married)

    dependents = random.randint(0, 4)

    education_level = random.choice(education)

    employment = random.choice(employment_types)

    monthly_income = random.randint(20000, 250000)

    monthly_expenses = random.randint(
        5000,
        int(monthly_income * 0.60)
    )

    existing_emi = random.randint(
        0,
        int(monthly_income * 0.25)
    )

    savings = random.randint(
        10000,
        1500000
    )

    credit_score = random.randint(300, 900)

    credit_history = random.choice([0, 1])

    loan_type = random.choice(loan_types)

    loan_amount = random.randint(
        100000,
        5000000
    )

    loan_tenure = random.choice(
        [60, 120, 180, 240, 300]
    )

    property_area = random.choice(property_areas)

    # -------------------------
    # Feature Engineering
    # -------------------------

    debt_ratio = (
        monthly_expenses + existing_emi
    ) / monthly_income

    savings_ratio = savings / monthly_income

    financial_score = (
        (credit_score / 900) * 40
        + (1 - debt_ratio) * 30
        + min(savings_ratio / 10, 1) * 20
        + (monthly_income / 250000) * 10
    )

    financial_score = round(financial_score, 2)

    # -------------------------
    # Approval Logic
    # -------------------------

    score = 0

    if credit_score >= 700:
        score += 2

    elif credit_score >= 600:
        score += 1

    if monthly_income >= 80000:
        score += 2

    elif monthly_income >= 50000:
        score += 1

    if debt_ratio < 0.40:
        score += 2

    elif debt_ratio < 0.60:
        score += 1

    if savings_ratio >= 5:
        score += 2

    elif savings_ratio >= 2:
        score += 1

    if credit_history == 1:
        score += 2

    if loan_amount <= monthly_income * 25:
        score += 1

    # Final Decision

    if score >= 7:
        loan_status = "Approved"
    else:
        loan_status = "Rejected"

    records.append({

        "Age": age,
        "Gender": gender,
        "Married": married_status,
        "Dependents": dependents,
        "Education": education_level,
        "Employment_Type": employment,
        "Monthly_Income": monthly_income,
        "Monthly_Expenses": monthly_expenses,
        "Existing_EMI": existing_emi,
        "Savings": savings,
        "Credit_Score": credit_score,
        "Credit_History": credit_history,
        "Loan_Type": loan_type,
        "Loan_Amount": loan_amount,
        "Loan_Tenure": loan_tenure,
        "Property_Area": property_area,
        "Debt_Ratio": round(debt_ratio, 2),
        "Savings_Ratio": round(savings_ratio, 2),
        "Financial_Score": financial_score,
        "Loan_Status": loan_status

    })

df = pd.DataFrame(records)

df.to_csv(
    "custom_loan_dataset.csv",
    index=False
)

print("\nDataset Generated Successfully\n")

print(df.head())

print("\nLoan Status Distribution\n")

print(df["Loan_Status"].value_counts())

print("\nApproval Percentage")

print(
    round(
        df["Loan_Status"].value_counts(normalize=True) * 100,
        2
    )
)