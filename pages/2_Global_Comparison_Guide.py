# import streamlit as st
# import pandas as pd

# st.set_page_config(
#     page_title="Global Comparison Guide",
#     page_icon="📘",
#     layout="wide"
# )

# st.title("📘 Global Comparison Guide")
# st.caption("Informational guidance for demonstration purposes only")

# st.divider()
# st.subheader("🌍 Country-wise Overview")

# tab_usa, tab_canada, tab_germany = st.tabs(["🇺🇸 USA", "🇨🇦 Canada", "🇩🇪 Germany"])

# with tab_usa:
#     st.markdown("""
#     **Exams:** SAT / GRE / IELTS  
#     **Visa:** F-1 Visa  
#     **Post-study:** OPT (1–3 years)  
#     **Top Universities:** MIT, Harvard, Stanford
#     """)

# with tab_canada:
#     st.markdown("""
#     **Exams:** IELTS / GRE  
#     **Visa:** Study Permit  
#     **Post-study:** PGWP + PR pathway  
#     **Top Universities:** Toronto, UBC, McGill
#     """)

# with tab_germany:
#     st.markdown("""
#     **Exams:** IELTS / APS  
#     **Visa:** Student Residence Permit  
#     **Post-study:** 18-month job search visa  
#     **Top Universities:** TU Munich, RWTH Aachen
#     """)

# # =====================================================
# # 1️⃣ ENTRANCE EXAMS (STREAM-WISE)
# # =====================================================
# st.subheader("🎓 Entrance Exams by Stream (India vs Abroad)")

# exam_df = pd.DataFrame({
#     "Stream / Field": ["Engineering", "Medical", "Law", "Business", "Arts"],
#     "India": [
#         "JEE Main / JEE Advanced",
#         "NEET",
#         "CLAT / AILET",
#         "CUET / IPMAT",
#         "CUET / University-specific exams"
#     ],
#     "Abroad": [
#         "SAT / ACT + IELTS",
#         "MCAT / IELTS",
#         "LSAT / IELTS",
#         "GMAT / IELTS",
#         "SAT / IELTS / Portfolio"
#     ]
# })

# st.table(exam_df)
# st.subheader("💰 Average Education Cost Comparison (₹ Lakhs)")

# cost_df = pd.DataFrame({
#     "Country": ["India", "USA", "Canada", "Germany"],
#     "Avg Cost (₹ Lakhs)": [10, 55, 35, 20]
# })

# st.bar_chart(cost_df.set_index("Country"))


# # =====================================================
# # 2️⃣ VISA & MIGRATION POLICIES
# # =====================================================
# st.subheader("🛂 Visa & Migration Policies (Overview)")

# visa_df = pd.DataFrame({
#     "Region": ["India", "USA", "Canada", "Germany", "UK", "Australia"],
#     "Student Visa": [
#         "Not required",
#         "F-1 Visa",
#         "Study Permit",
#         "Student Residence Permit",
#         "Student Route Visa",
#         "Subclass 500"
#     ],
#     "Post-Study Work / PR": [
#         "N/A",
#         "OPT (1–3 years)",
#         "PGWP + PR pathways",
#         "18-month job search visa",
#         "Graduate Route (2 years)",
#         "Temporary Graduate Visa"
#     ]
# })

# st.table(visa_df)

# # =====================================================
# # 3️⃣ UNIVERSITY COMPARISON (ABROAD)
# # =====================================================
# st.subheader("🏫 Top University Comparison (Abroad)")

# uni_df = pd.DataFrame({
#     "University": ["MIT", "Harvard", "Yale"],
#     "Country": ["USA", "USA", "USA"],
#     "Known For": [
#         "Engineering, AI, Technology",
#         "Business, Law, Medicine",
#         "Law, Humanities, Social Sciences"
#     ],
#     "Typical Acceptance Rate": [
#         "4–5%",
#         "4–6%",
#         "5–7%"
#     ]
# })

# st.table(uni_df)

# # =====================================================
# # 4️⃣ APPROXIMATE CUTOFF CRITERIA
# # =====================================================
# st.subheader("📊 Approximate Cutoff Criteria")

# cutoff_df = pd.DataFrame({
#     "Exam": ["JEE Advanced", "NEET", "CLAT", "GRE", "GMAT", "IELTS"],
#     "India (Typical Cutoff)": [
#         "Top 10k–15k rank",
#         "600+ score",
#         "90+ percentile",
#         "N/A",
#         "N/A",
#         "N/A"
#     ],
#     "Abroad (Typical Requirement)": [
#         "N/A",
#         "N/A",
#         "N/A",
#         "310+",
#         "650+",
#         "7.0+"
#     ]
# })

# st.table(cutoff_df)

# st.divider()

# # =====================================================
# # DISCLAIMER
# # =====================================================
# st.info("""
# ℹ️ **Disclaimer**

# • All information shown here is **approximate and indicative**  
# • Data is included **for prototype and comparison purposes only**  
# • Actual requirements may vary by university and year  
# • This page does **not influence AI recommendations**
# """)
import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Global Guide",
    page_icon="📘",
    layout="wide"
)

# ---------------- OPTIONAL: HIDE SIDEBAR ----------------
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- BACK TO HOME ----------------
if st.button("🔙 Back to Home"):
    st.switch_page("app.py")

# ---------------- HEADER ----------------
st.title("📘 Global Comparison Guide")
st.caption("Informational guidance for demonstration purposes only")

st.divider()

# =====================================================
# 🌍 COUNTRY-WISE OVERVIEW
# =====================================================
st.subheader("🌍 Country-wise Overview")

tab_usa, tab_canada, tab_germany = st.tabs([" USA", " Canada", "Germany"])

with tab_usa:
    st.markdown("""
    **Entrance Exams:** SAT / GRE / IELTS  
    **Student Visa:** F-1  
    **Post-study Work:** OPT (1–3 years)  
    **Top Universities:** MIT, Harvard, Stanford
    """)

with tab_canada:
    st.markdown("""
    **Entrance Exams:** IELTS / GRE  
    **Student Visa:** Study Permit  
    **Post-study Work:** PGWP + PR pathway  
    **Top Universities:** University of Toronto, UBC, McGill
    """)

with tab_germany:
    st.markdown("""
    **Entrance Exams:** IELTS / APS  
    **Student Visa:** Student Residence Permit  
    **Post-study Work:** 18-month job search visa  
    **Top Universities:** TU Munich, RWTH Aachen
    """)

st.divider()

# =====================================================
# 1️⃣ ENTRANCE EXAMS (STREAM-WISE)
# =====================================================
st.subheader("🎓 Entrance Exams by Stream (India vs Abroad)")

exam_df = pd.DataFrame({
    "Stream / Field": ["Engineering", "Medical", "Law", "Business", "Arts"],
    "India": [
        "JEE Main / JEE Advanced",
        "NEET",
        "CLAT / AILET",
        "CUET / IPMAT",
        "CUET / University-specific exams"
    ],
    "Abroad": [
        "SAT / ACT + IELTS",
        "MCAT / IELTS",
        "LSAT / IELTS",
        "GMAT / IELTS",
        "SAT / IELTS / Portfolio"
    ]
})

st.table(exam_df)

# =====================================================
# 📊 COST COMPARISON (BAR CHART)
# =====================================================
st.subheader("💰 Average Education Cost Comparison (₹ Lakhs)")

cost_df = pd.DataFrame({
    "Country": ["India", "USA", "Canada", "Germany"],
    "Avg Cost (₹ Lakhs)": [10, 55, 35, 20]
})

st.bar_chart(cost_df.set_index("Country"))

# =====================================================
# 🔥 DIFFICULTY HEATMAP
# =====================================================
st.subheader("🔥 Relative Difficulty Comparison")

difficulty_df = pd.DataFrame(
    {
        "Entrance Difficulty": [3, 5, 4, 4],
        "Visa Complexity": [1, 4, 3, 2],
        "Cost Pressure": [2, 5, 4, 2]
    },
    index=["India", "USA", "Canada", "Germany"]
)

st.dataframe(
    difficulty_df.style.background_gradient(cmap="Reds"),
    use_container_width=True
)

# =====================================================
# 2️⃣ VISA & MIGRATION POLICIES
# =====================================================
st.subheader("🛂 Visa & Migration Policies (Overview)")

visa_df = pd.DataFrame({
    "Region": ["India", "USA", "Canada", "Germany", "UK", "Australia"],
    "Student Visa": [
        "Not required",
        "F-1 Visa",
        "Study Permit",
        "Student Residence Permit",
        "Student Route Visa",
        "Subclass 500"
    ],
    "Post-Study Work / PR": [
        "N/A",
        "OPT (1–3 years)",
        "PGWP + PR pathways",
        "18-month job search visa",
        "Graduate Route (2 years)",
        "Temporary Graduate Visa"
    ]
})

st.table(visa_df)

# =====================================================
# 3️⃣ UNIVERSITY COMPARISON (ABROAD)
# =====================================================
st.subheader("🏫 Top University Comparison (Abroad)")

uni_df = pd.DataFrame({
    "University": ["MIT", "Harvard", "Yale"],
    "Country": ["USA", "USA", "USA"],
    "Known For": [
        "Engineering, AI, Technology",
        "Business, Law, Medicine",
        "Law, Humanities, Social Sciences"
    ],
    "Typical Acceptance Rate": [
        "4–5%",
        "4–6%",
        "5–7%"
    ]
})

st.table(uni_df)

# =====================================================
# 4️⃣ APPROXIMATE CUTOFF CRITERIA
# =====================================================
st.subheader("📊 Approximate Cutoff Criteria")

cutoff_df = pd.DataFrame({
    "Exam": ["JEE Advanced", "NEET", "CLAT", "GRE", "GMAT", "IELTS"],
    "India (Typical Cutoff)": [
        "Top 10k–15k rank",
        "600+ score",
        "90+ percentile",
        "N/A",
        "N/A",
        "N/A"
    ],
    "Abroad (Typical Requirement)": [
        "N/A",
        "N/A",
        "N/A",
        "310+",
        "650+",
        "7.0+"
    ]
})

st.table(cutoff_df)

# =====================================================
# 📘 GLOSSARY
# =====================================================
st.subheader("📘 Glossary (Exams & Visas)")

with st.expander("Click to view glossary"):
    st.markdown("""
    **JEE** – Engineering entrance exam (India)  
    **NEET** – Medical entrance exam (India)  
    **CLAT** – Law entrance exam (India)  
    **SAT** – Undergraduate test (Abroad)  
    **GRE** – Graduate-level aptitude test  
    **IELTS** – English proficiency test  

    **F-1 Visa** – US student visa  
    **PGWP** – Canada post-graduation work permit  
    **OPT** – US post-study work authorization
    """)

# =====================================================
# 📄 DOWNLOADABLE PDF GUIDE
# =====================================================
def safe_text(text):
    return (
        text.replace("–", "-")
            .replace("₹", "Rs.")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
    )

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    content = """
GLOBAL PATHWAYS AI - COMPARISON GUIDE

- Entrance exams (India vs Abroad)
- Visa and migration overview
- Top universities
- Cutoff benchmarks

Note: This guide is for demonstration purposes only.
"""

    pdf.multi_cell(0, 8, safe_text(content))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# =====================================================
# DISCLAIMER
# =====================================================
st.divider()
st.info("""
ℹ️ **Disclaimer**

• All information is approximate and indicative  
• Data is included for prototype demonstration only  
• Actual requirements vary by country and university  
• This page does NOT influence AI recommendations
""")

