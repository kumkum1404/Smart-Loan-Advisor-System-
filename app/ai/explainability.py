def explain_prediction(data, prediction):
    
    reasons = []

    if data["Credit_Score"] >= 750:
        reasons.append("Excellent Credit Score")

    elif data["Credit_Score"] >= 650:
        reasons.append("Good Credit Score")

    else:
        reasons.append("Low Credit Score")



    if data["Monthly_Income"] >= 60000:
        reasons.append("Strong Monthly Income")

    elif data["Monthly_Income"] >= 30000:
        reasons.append("Average Monthly Income")

    else:
        reasons.append("Low Monthly Income")



    if data["Savings"] >= 200000:
        reasons.append("Healthy Savings")



    if data["Existing_EMI"] < data["Monthly_Income"]*0.25:
        reasons.append("Low Existing EMI")



    if prediction=="Approved":
        status="Financial profile meets loan eligibility."

    else:
        status="Financial profile needs improvement."



    return {

        "status":status,

        "reasons":reasons

    }