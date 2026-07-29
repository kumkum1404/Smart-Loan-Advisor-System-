import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read API Key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_ai_advice(
    age,
    income,
    loan_amount,
    credit_score,
    financial_score,
    prediction,
    emi
):
    prompt = f"""
You are a professional Financial Advisor.

Analyze the following user's loan profile and provide personalized financial advice.

Age: {age}

Monthly Income: ₹{income}

Loan Amount: ₹{loan_amount}

Credit Score: {credit_score}

Financial Score: {financial_score}

Predicted Loan Status: {prediction}

Estimated EMI: ₹{emi}

Requirements:

1. Congratulate or guide the user.
2. Explain whether taking this loan is financially safe.
3. Mention one risk if applicable.
4. Give 3 financial improvement tips.
5. Keep the response professional and under 150 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=300
    )

    return response.choices[0].message.content

    #for Chatbot
def chat_with_ai(user_message, report_data):
    
    prompt = f"""
You are LoanSense Copilot, an AI Financial Assistant.

The user's loan report is:

{report_data}

User Question:
{user_message}

Instructions:
- Answer only questions related to loans, finance, EMI, banks, credit score and financial planning.
- Use the user's report to give personalized advice.
- Be friendly and professional.
- Keep answers under 120 words.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": "You are an expert AI Financial Advisor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,

        max_tokens=250

    )

    return response.choices[0].message.content   