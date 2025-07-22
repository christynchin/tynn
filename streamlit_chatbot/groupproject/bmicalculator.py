import streamlit as st

# App title
st.title("🌟 BMI Calculator Web App")

# User inputs
st.header("Enter your details:")
name = st.text_input("👤 Name:")
gender = st.radio("⚧️ Gender:", ("Male", "Female"))
age = st.number_input("🎂 Age:", min_value=0, max_value=120, step=1)
height = st.number_input("📏 Height (in meters):", min_value=0.0, format="%.2f")
weight = st.number_input("⚖️ Weight (in kilograms):", min_value=0.0, format="%.1f")

# Calculate BMI
if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        bmi = weight / (height ** 2)
        st.subheader(f"Hello {name}, here are your results:")
        st.write(f"**BMI:** {bmi:.2f}")

        # BMI interpretation and tips
        if bmi < 18.5:
            st.warning("You are underweight.")
            st.info("💡 Tip: Add more calories, protein, and healthy fats to your meals.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a normal weight.")
            st.info("💡 Tip: Maintain your weight with a balanced diet and regular activity.")
        elif 25 <= bmi < 29.9:
            st.info("You are overweight.")
            st.info("💡 Tip: Consider more veggies and physical activity in your routine.")
        else:
            st.error("You are obese.")
            st.info("💡 Tip: Consult a doctor, and consider gentle exercises and smaller meal portions.")

        # Extra health note based on age
        if age < 18:
            st.info("🧒 You're under 18 — BMI may not fully reflect your health. Talk to a doctor or a parent.")
        elif age > 60:
            st.info("👵 At your age, maintaining strength and balanced nutrition is key. Keep moving safely!")

    else:
        st.error("❗ Please enter valid height and weight.")

