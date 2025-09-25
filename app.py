import streamlit as st
from transformers import pipeline
from datetime import datetime

# === Step 1: Initialize classifier ===
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1
)

# === Step 2: Define categories and routing ===
categories = [
    "Account Access Issue", 
    "Billing / Invoice Query", 
    "Technical / System Support", 
    "Feature Request", 
    "General Feedback"
]

team_mapping = {
    "Account Access Issue": "Team A",
    "Billing / Invoice Query": "Team B",
    "Technical / System Support": "Team C",
    "Feature Request": "Team D",
    "General Feedback": "Team E"
}

urgent_keywords = ["cannot access", "crashed", "error", "fail"]

# === Step 3: Client schedule (simple example) ===
clients = {
    "alpha": {"email": "alpha@gmail.com", "next_available_slot": 0},
    "beta": {"email": "beta@gmail.com", "next_available_slot": 0},
    "gamma": {"email": "gamma@gmail.com", "next_available_slot": 0},
}

# === Step 4: Alternative suggestions based on category ===
alternative_suggestions = {
    "Account Access Issue": [
        "Try resetting your password again.",
        "Check if the account is locked and unlock if possible.",
        "Verify that you are using the correct username or email."
    ],
    "Billing / Invoice Query": [
        "Check the invoice details for duplicate charges.",
        "Verify the billing cycle and subscription plan.",
        "Confirm recent payments and adjustments."
    ],
    "Technical / System Support": [
        "Restart the application or system.",
        "Check for updates or patches.",
        "Verify network connectivity and error logs."
    ],
    "Feature Request": [
        "Check if there is an existing workaround.",
        "See if a temporary solution can meet the requirement.",
        "Confirm the feasibility of the request before escalating."
    ],
    "General Feedback": [
        "Acknowledge the feedback and thank the client.",
        "Check if immediate action is needed.",
        "Forward to the relevant team if applicable."
    ]
}

# === Step 5: Streamlit UI ===
st.title("🚀 TCS AI-Powered Client Query Routing Agent")
st.subheader("Smart Routing, Faster Responses, Happier Clients")

# Input fields
employee_name = st.text_input("Employee Name:")
employee_email = st.text_input("Employee Email:")
query = st.text_area("Enter Client Query:")

if st.button("Route Query"):
    if not query.strip():
        st.warning("Please enter a client query!")
    elif not employee_name.strip() or not employee_email.strip():
        st.warning("Please enter employee details!")
    else:
        # Step 1: Determine category
        if "invoice" in query.lower() or "billing" in query.lower():
            predicted_category = "Billing / Invoice Query"
        elif "crash" in query.lower() or "error" in query.lower() or "fail" in query.lower():
            predicted_category = "Technical / System Support"
        elif "account" in query.lower():
            predicted_category = "Account Access Issue"
        elif "feature" in query.lower() or "add" in query.lower():
            predicted_category = "Feature Request"
        else:
            result = classifier(query, candidate_labels=categories, hypothesis_template="This text is about {}.")
            predicted_category = result['labels'][0]

        assigned_team = team_mapping[predicted_category]

        # Step 2: Assign client based on earliest available slot
        selected_client = min(clients.items(), key=lambda x: x[1]["next_available_slot"])
        client_name = selected_client[0].capitalize()
        client_email = selected_client[1]["email"]
        clients[client_name.lower()]["next_available_slot"] += 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Step 3: Display results
        st.markdown(f"**Employee:** {employee_name} ({employee_email})")
        st.markdown(f"**Client:** {client_name} ({client_email})")
        st.markdown(f"**Query:** {query}")
        st.markdown(f"**Predicted Category:** {predicted_category}")
        st.markdown(f"**Assigned Team:** {assigned_team}")
        st.markdown(f"**Timestamp:** {timestamp}")

        # Step 4: Urgency check
        if any(word in query.lower() for word in urgent_keywords):
            st.error("⚠️ Urgent query detected!")

        # Step 5: Show alternative suggestions
        st.subheader("💡 Suggested Actions Before Escalating to Client:")
        for idx, suggestion in enumerate(alternative_suggestions[predicted_category], 1):
            st.markdown(f"{idx}. {suggestion}")

        st.success("Query processed successfully!")
    