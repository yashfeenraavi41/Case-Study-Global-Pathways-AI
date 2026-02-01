from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
# Enable CORS for the React frontend (running on port 5173 by default with Vite)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

# ------------------ LOAD MODELS & DATA ------------------
try:
    india_abroad_model = joblib.load("india_vs_abroad_model.pkl")
    country_model = joblib.load("country_recommendation_model.pkl")
    explain_df = pd.read_csv("global_pathways_with_extras.csv")
    print("Models and Data loaded successfully.")
except Exception as e:
    print(f"Error loading models/data: {e}")

# ------------------ STATIC DATA ------------------
country_financials = {
    'India': {'cost': 800000, 'salary': 600000},
    'Germany': {'cost': 2000000, 'salary': 5500000},
    'Canada': {'cost': 3500000, 'salary': 6000000},
    'UK': {'cost': 4500000, 'salary': 5800000},
    'USA': {'cost': 6000000, 'salary': 8000000},
    'Australia': {'cost': 5000000, 'salary': 6500000}
}

# Values for UI comparison tables
comparison_data = {
    "exams": [
        {"field": "Engineering", "india": "JEE Main / Advanced", "abroad": "SAT / ACT + IELTS"},
        {"field": "Medical", "india": "NEET", "abroad": "MCAT / IELTS"},
        {"field": "Law", "india": "CLAT / AILET", "abroad": "LSAT / IELTS"},
        {"field": "Business", "india": "CUET / IPMAT", "abroad": "GMAT / IELTS"},
        {"field": "Arts", "india": "CUET", "abroad": "SAT / IELTS / Portfolio"},
    ],
    "costs": [
        {"country": "India", "cost": 10},
        {"country": "USA", "cost": 55},
        {"country": "Canada", "cost": 35},
        {"country": "Germany", "cost": 20},
    ],
    "visa": [
        {"region": "USA", "visa": "F-1 Visa", "post_study": "OPT (1–3 years)"},
        {"region": "Canada", "visa": "Study Permit", "post_study": "PGWP + PR pathways"},
        {"region": "Germany", "visa": "Student Permit", "post_study": "18-month job search"},
        {"region": "UK", "visa": "Student Route", "post_study": "Graduate Route (2 years)"},
        {"region": "Australia", "visa": "Subclass 500", "post_study": "Temporary Graduate"},
    ]
}

# ------------------ HELPERS ------------------
def get_career_insights(stream, interest):
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

    return {
        "growth": growth,
        "salary_range": salary,
        "scholarship_chance": scholarship,
        "top_colleges_india": colleges_india.get(stream, []),
        "top_colleges_abroad": colleges_abroad.get(stream, [])
    }

def calculate_roi(country, years=5):
    if country not in country_financials: return 0
    cost = country_financials[country]['cost']
    salary = country_financials[country]['salary']
    roi = round(((salary * years) - cost) / cost, 2)
    
    label = "Low ROI"
    if roi >= 2.0: label = "Strong ROI"
    elif roi >= 1.0: label = "Moderate ROI"
    
    return {"score": roi, "label": label, "cost": cost, "salary": salary}

# ------------------ ENDPOINTS ------------------

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Global Pathways AI - API is running", "endpoints": ["/api/static-data", "/api/evaluate"]})

@app.route('/api/static-data', methods=['GET'])
def get_static_data():
    return jsonify(comparison_data)

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        # Expected keys: stream, marks, budget, interest, risk
        stream = data.get('stream')
        marks = data.get('marks')
        budget = data.get('budget')
        interest = data.get('interest')
        risk = data.get('risk')

        user_df = pd.DataFrame([{
            "academic_stream": stream,
            "twelfth_percentage": marks,
            "budget_range": budget,
            "primary_interest": interest,
            "risk_appetite": risk
        }])

        # Core Decision
        decision = india_abroad_model.predict(user_df)[0]
        confidence = float(max(india_abroad_model.predict_proba(user_df)[0]) * 100)

        # Career Insights
        insights = get_career_insights(stream, interest)

        # Explanation Data
        explain_row = explain_df[explain_df["academic_stream"] == stream].iloc[0]
        
        response = {
            "decision": decision,
            "confidence": round(confidence, 2),
            "insights": insights,
            "exams": {
                "india": explain_row["india_entrance_exams"],
                "abroad": explain_row["abroad_entrance_exams"]
            },
            "visa_summary": explain_row["visa_policy_summary"],
            "university_comparison": explain_row["university_comparison"],
            "cutoff_criteria": explain_row["cutoff_criteria"]
        }

        # Country Recommendation
        if decision != "Stay in India":
            rec_country = country_model.predict(user_df)[0]
            roi_info = calculate_roi(rec_country)
            response["recommendation"] = {
                "country": rec_country,
                "roi": roi_info
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
