import streamlit as st
import openai

# Page Config
st.set_page_config(page_title="AquaAI - Aquascape Diagnostics", page_icon="🌿")
st.title("🌿 AquaAI: Aquascape & Plant Health Advisor")
st.write("Diagnose parameter imbalances, lighting issues, and algae outbreaks instantly.")

# User inputs API Key (or store securely in environment secrets)
api_key = st.secrets["OPENAI_API_KEY"]

st.subheader("1. Enter Your Tank Parameters")
col1, col2 = st.columns(2)

with col1:
    co2_status = st.selectbox("CO2 Injection Level", ["No CO2", "Low (<15ppm)", "Optimal (20-30ppm)", "Fluctuating"])
    light_hours = st.slider("Photoperiod (Hours of Light/Day)", 4, 12, 8)
    fertilizer = st.selectbox("Dosing Method", ["None", "Lean Dosing (ADA style)", "Estimative Index (EI)", "All-in-One Liquid"])

with col2:
    nitrate = st.number_input("Nitrate / NO3 (ppm)", min_value=0.0, max_value=100.0, value=10.0)
    phosphate = st.number_input("Phosphate / PO4 (ppm)", min_value=0.0, max_value=10.0, value=1.0)
    algae_type = st.selectbox("Observed Algae Problem", ["None / General Checkup", "Black Beard Algae (BBA)", "Green Dust Algae (GDA)", "Hair / Thread Algae", "Staghorn", "Blue-Green Algae (Cyanobacteria)"])

st.subheader("2. Specific Issue Description")
user_notes = st.text_area("Describe plant growth (e.g., melting leaves, slow growth, pale tops):", "")

if st.button("Analyze Tank & Prescribe Action"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            You are an expert aquascaper and aquatic botanist.
            Analyze the following aquarium parameters and provide a structured diagnosis:
            - CO2 Level: {co2_status}
            - Lighting: {light_hours} hours/day
            - Dosing Method: {fertilizer}
            - Nitrate (NO3): {nitrate} ppm
            - Phosphate (PO4): {phosphate} ppm
            - Main Algae Issue: {algae_type}
            - User Notes: {user_notes}

            Format your response clearly:
            1. **Primary Cause of Imbalance**
            2. **Immediate Action Steps (Next 48 Hours)**
            3. **Long-Term Nutrient & Light Maintenance Plan**
            """

            with st.spinner("Analyzing ecosystem dynamics..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                
            st.success("Diagnosis Complete!")
            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error connecting to AI backend: {e}")