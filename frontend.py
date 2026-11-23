import os
import streamlit as st
import requests
from config.city_tier import tier_1_cities, tier_2_cities

# Page Configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# Title & Description
st.title("🏥 Insurance Premium Predictor")
st.markdown("Yeh frontend **Streamlit** mein bana hai aur backend par **FastAPI + ML Model** ko call karta hai.")
st.divider()

# List of Cities from central config
all_cities = sorted(tier_1_cities + tier_2_cities)

# 2-Column Form Layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=119, value=28, step=1)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=250.0, value=70.0, step=0.5)
    height = st.number_input("Height (meters, e.g. 1.75)", min_value=0.5, max_value=2.4, value=1.75, step=0.01)
    smoker_choice = st.radio("Do you smoke?", options=["No", "Yes"], horizontal=True)
    is_smoker = True if smoker_choice == "Yes" else False

with col2:
    income_lpa = st.number_input("Annual Income (in LPA)", min_value=1.0, max_value=119.0, value=12.0, step=0.5)
    city = st.selectbox("City", options=all_cities, index=all_cities.index("Mumbai") if "Mumbai" in all_cities else 0)
    occupation = st.selectbox(
        "Occupation",
        options=['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'],
        index=6
    )

# Quick BMI preview
calculated_bmi = round(weight / (height ** 2), 1)
st.info(f"📊 **Calculated BMI Preview:** `{calculated_bmi}`")

st.divider()

# Backend URL (configurable via environment variable)
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/predict")

if st.button("🔮 Predict Insurance Premium", use_container_width=True, type="primary"):
    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": is_smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        with st.spinner("Connecting to FastAPI server & running ML model..."):
            response = requests.post(FASTAPI_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            predicted_category = result.get("predicted_category", "Unknown")
            confidence = result.get("confidence", 0.0)
            
            # Color-coded result display
            if predicted_category.lower() == "low":
                st.success(f"### 🎉 Predicted Premium Category: **{predicted_category}** (Confidence: {confidence * 100:.1f}%)")
                st.balloons()
            elif predicted_category.lower() == "medium":
                st.warning(f"### ⚠️ Predicted Premium Category: **{predicted_category}** (Confidence: {confidence * 100:.1f}%)")
            else:
                st.error(f"### 🚨 Predicted Premium Category: **{predicted_category}** (Confidence: {confidence * 100:.1f}%)")
                
            st.json(result)
        else:
            st.error(f"❌ Backend Error (Status {response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ **FastAPI Server Not Running!**")
        st.warning(
            f"Could not connect to `{FASTAPI_URL}`.\n\n"
            "Make sure the backend server is running in another terminal:\n"
            "```powershell\n"
            "uvicorn myapp:app --reload\n"
            "```"
        )
