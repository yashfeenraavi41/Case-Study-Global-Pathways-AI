import streamlit as st

st.set_page_config(
    page_title="Global Pathways AI",
    page_icon="🌍",
    layout="centered"
)

# ------------------ HERO SECTION ------------------
st.title("🌍 Global Pathways AI")
st.subheader("AI-powered decision support for education & career pathways")

st.write("""
Global Pathways AI helps students make **transparent, data-driven decisions**
about whether to **study in India or abroad**, and **which country makes the most sense**.

This is an **AI-assisted decision support system**, not a counselling service.
""")

st.divider()

# ------------------ WHAT IT DOES ------------------
st.subheader("🔍 What This Platform Does")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎓 Academic Profile")
    st.write("Analyzes stream, marks, and interests")

with col2:
    st.markdown("### 🌍 Global Comparison")
    st.write("India vs Abroad, country-level recommendations")

with col3:
    st.markdown("### 💰 ROI & Career Growth")
    st.write("Cost, salary outlook, and long-term ROI")

st.divider()

# ------------------ HOW IT WORKS ------------------
st.subheader("⚙️ How It Works")

st.markdown("""
1️⃣ You enter **basic academic & financial details**  
2️⃣ AI evaluates **India vs Abroad feasibility**  
3️⃣ If applicable, AI recommends the **best-fit country**  
4️⃣ You receive **career insights, ROI, exams & policy info**
""")

st.divider()

# ------------------ CTA ------------------
st.subheader("🚀 Get Started")

st.write("Click below to analyze your personalized pathway.")

if st.button("👉 Analyze My Path"):
    st.switch_page("pages/1_Analyze_Path.py")

# ------------------ FOOTER ------------------
st.caption("""
Prototype built for case-study demonstration purposes.
ML models are trained on synthetic but realistic data.
""")
