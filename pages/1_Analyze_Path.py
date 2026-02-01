# python -m streamlit run app.py

import streamlit as st
import joblib
import pandas as pd

# ------------------ PAGE CONFIG (MUST BE FIRST) ------------------
st.set_page_config(page_title="Global Pathways AI", layout="centered")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_explanation_data():
    return pd.read_csv("global_pathways_with_extras.csv")

explain_df = load_explanation_data()

india_abroad_model = joblib.load("india_vs_abroad_model.pkl")
country_model = joblib.load("country_recommendation_model.pkl")

# ------------------ STATIC DATA ------------------
country_financials = {
    'India': {'cost': 800000, 'salary': 600000},
    'Germany': {'cost': 2000000, 'salary': 5500000},
    'Canada': {'cost': 3500000, 'salary': 6000000},
    'UK': {'cost': 4500000, 'salary': 5800000},
    'USA': {'cost': 6000000, 'salary': 8000000},
    'Australia': {'cost': 5000000, 'salary': 6500000}
}

# ------------------ HELPERS ------------------
def career_insights(stream, interest):
    if interest in ["Technology", "Medicine"]:
        growth = "Very High"
        salary = "₹6–12 LPA (India) / $60–100K (Abroad)"
    elif interest in ["Business", "Research"]:
        growth = "High"
        salary = "₹4–8 LPA (India) / $40–70K (Abroad)"
    else:
        growth = "Moderate"
        salary = "₹3–6 LPA (India) / $30–50K (Abroad)"

    scholarship = "High" if stream == "Science" else "Medium"

    colleges_india = {
        "Science": ["IITs", "NITs", "BITS"],
        "Commerce": ["SRCC", "NMIMS", "Christ"],
        "Arts": ["LSR", "St. Stephens", "JNU"]
    }

    colleges_abroad = {
        "Science": ["MIT", "ETH Zurich", "Toronto"],
        "Commerce": ["Wharton", "INSEAD", "LBS"],
        "Arts": ["RCA", "Parsons", "RISD"]
    }

    return growth, salary, scholarship, colleges_india[stream], colleges_abroad[stream]


def calculate_roi(country, years=5):
    cost = country_financials[country]['cost']
    salary = country_financials[country]['salary']
    return round(((salary * years) - cost) / cost, 2)


def roi_label(roi):
    if roi >= 2.0:
        return "Strong ROI"
    elif roi >= 1.0:
        return "Moderate ROI"
    return "Low ROI"


# ------------------ UI ------------------
st.title("🌍 Global Pathways AI – MVP")

stream = st.selectbox("Academic Stream", ["Science", "Commerce", "Arts"])
marks = st.slider("12th Percentage", 40, 100, 75)
budget = st.selectbox("Budget Range", ["5-10L", "10-20L", "20-30L", "30-50L", "50L+"])
interest = st.selectbox("Primary Interest", ["Technology", "Business", "Medicine", "Arts", "Research", "Government"])
risk = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])

# ------------------ ACTION ------------------
if st.button("Analyze My Path"):
    user_df = pd.DataFrame([{
        "academic_stream": stream,
        "twelfth_percentage": marks,
        "budget_range": budget,
        "primary_interest": interest,
        "risk_appetite": risk
    }])

    decision = india_abroad_model.predict(user_df)[0]
    confidence = float(max(india_abroad_model.predict_proba(user_df)[0]) * 100)

    st.subheader("📌 Core Decision")
    st.success(f"{decision} ({confidence:.2f}%)")

    # Career insights
    growth, salary, scholarship, india_colleges, abroad_colleges = career_insights(stream, interest)

    st.subheader("📈 Career Insights")
    st.table(pd.DataFrame({
        "Parameter": ["Career Growth", "Scholarship Chance", "Avg Starting Salary"],
        "Value": [growth, scholarship, salary]
    }))

    st.subheader("🎓 Top Colleges in India")
    st.write(", ".join(india_colleges))

    st.subheader("🌍 Top Colleges Abroad")
    st.write(", ".join(abroad_colleges))

    # -------- Explanation dataset (SECOND LAYER) --------
    explain_row = explain_df[
        explain_df["academic_stream"] == stream
    ].iloc[0]

    st.subheader("📚 Entrance Exams (Demo)")
    st.table(pd.DataFrame({
        "Region": ["India", "Abroad"],
        "Exams": [
            explain_row["india_entrance_exams"],
            explain_row["abroad_entrance_exams"]
        ]
    }))

    st.subheader("🛂 Visa & Migration Overview")
    st.info(explain_row["visa_policy_summary"])

    st.subheader("🏫 University Comparison")
    st.write(explain_row["university_comparison"])

    st.subheader("📊 Approximate Cutoff Criteria")
    st.code(explain_row["cutoff_criteria"])

    # -------- Country + ROI --------
    if decision != "Stay in India":
        country = country_model.predict(user_df)[0]
        roi = calculate_roi(country)

        st.subheader("🌍 Country Recommendation & ROI")
        st.write("Recommended Country:", country)
        st.write("Estimated Cost:", f"₹{country_financials[country]['cost']:,}")
        st.write("Expected Salary:", f"₹{country_financials[country]['salary']:,}")
        st.write("5-Year ROI:", roi)
        st.info(f"ROI Strength: {roi_label(roi)}")
