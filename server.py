
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

# ------------------ EXTENDED HELPERS ------------------
def evaluate_work_pathway(data, is_abroad=True):
    # Heuristic for demo purposes (Logic-based decision support)
    exp = int(data.get('experience', 0))
    skills = data.get('skills', 'General')
    industry = data.get('industry', 'Technology')
    
    # Decisions based on parameters
    if is_abroad:
        decision = "International Career Highly Viable" if exp >= 2 else "Early Career Exploration Recommended"
        confidence = 88.5 if exp >= 2 else 72.4
        visa = "High probability for skilled worker visa (Subclass 189/190 or H-1B/Work Permit)"
        salary = "₹45–90 LPA Equivalent"
        cost = "₹15–25L (Relocation & Reserves)"
    else:
        decision = "Strong Domestic Growth Potential"
        confidence = 91.2
        visa = "N/A - Work in local economic zones (SEZs)"
        salary = "₹8–25 LPA (Experience Dependent)"
        cost = "Minimal (Local Housing & Setup)"

    return {
        "decision": decision,
        "confidence": confidence,
        "insights": {
            "growth": "Exponential" if industry in ["Technology", "Medicine"] else "Steady",
            "salary_range": salary,
            "scholarship_chance": "High" if is_abroad else "N/A",
            "top_colleges_india": ["Industry Certs", "Top Tech Hubs"],
            "top_colleges_abroad": ["Fortune 500 Entry", "Global Startup Ecosystems"]
        },
        "exams": {
            "india": "Skilled Assessments",
            "abroad": "IELTS (General) / Job-Specific Certs"
        },
        "visa_summary": visa,
        "university_comparison": "Focus on high-growth demand in " + industry,
        "cutoff_criteria": "Exp: " + str(exp) + "yrs | Skills: " + skills,
        "recommendation": {
            "country": "Germany" if is_abroad else "India (Bangalore/Pune)",
            "roi": {"score": 3.5 if is_abroad else 2.1, "label": "Strong ROI", "cost": cost, "salary": salary}
        }
    }

def evaluate_study_local(data):
    stream = data.get('stream', 'Science')
    marks = int(data.get('marks', 85))
    
    return {
        "decision": "Domestic Tier-1 Pursuit Recommended",
        "confidence": 94.1,
        "insights": {
            "growth": "High",
            "salary_range": "₹6–18 LPA",
            "scholarship_chance": "Moderate (EWS/Merit)",
            "top_colleges_india": ["IITs", "BITS", "IIMs"],
            "top_colleges_abroad": ["N/A for Local Path"]
        },
        "exams": {
            "india": "JEE / CAT / GATE",
            "abroad": "N/A"
        },
        "visa_summary": "N/A - Native Resident Status",
        "university_comparison": "Focus on Tier-1 Institutions for maximum ROI",
        "cutoff_criteria": "Marks: " + str(marks) + "% | Percentile Target: 98+",
        "recommendation": {
            "country": "India",
            "roi": {"score": 1.8, "label": "Moderate ROI", "cost": "₹5–15L", "salary": "₹12L avg"}
        }
    }

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
        goal = data.get('goal', 'study_abroad')

        # 1. Study Abroad (Existing ML Models)
        if goal == 'study_abroad':
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

            decision = india_abroad_model.predict(user_df)[0]
            confidence = float(max(india_abroad_model.predict_proba(user_df)[0]) * 100)
            insights = get_career_insights(stream, interest)
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

            if decision != "Stay in India":
                rec_country = country_model.predict(user_df)[0]
                roi_info = calculate_roi(rec_country)
                response["recommendation"] = {
                    "country": rec_country,
                    "roi": roi_info
                }
            return jsonify(response)

        # 2. Work Abroad
        elif goal == 'work_abroad':
            return jsonify(evaluate_work_pathway(data, is_abroad=True))

        # 3. Work Local
        elif goal == 'work_local':
            return jsonify(evaluate_work_pathway(data, is_abroad=False))

        # 4. Study Local
        elif goal == 'study_local':
            return jsonify(evaluate_study_local(data))

        return jsonify({"error": "Invalid pathway selection"}), 400

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
