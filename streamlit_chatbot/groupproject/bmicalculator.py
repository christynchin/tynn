import streamlit as st
import google.generativeai as genai
import os

# --- Securely load API key ---
# For deployment, store your API key in a .streamlit/secrets.toml file:
# GOOGLE_API_KEY="AIzaSyB2pYxqJg5pzRP_Z4cVJi7XvgFvGLo0bdk"
# For local testing, you can temporarily hardcode it or use environment variables.
# As you provided it in the prompt, I'll use it directly for this example.
# In a real-world scenario, you should use st.secrets["GOOGLE_API_KEY"]
# or environment variables for better security.
key=st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')

if not key:
    st.error("Google API Key not found. Please set it in your Streamlit secrets or as an environment variable.")
    st.stop()

# ---------- Page config ----------
st.set_page_config(page_title="BMI Calculator & Chatbot", page_icon="💪", layout="centered")

# ---------- Custom CSS styling ----------
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .main {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 24px;
        }
        /* Chatbot specific styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .stChatMessage[data-role="user"] {
            background-color: #e0f7fa; /* Light blue for user */
            align-self: flex-end;
            margin-left: auto;
        }
        .stChatMessage[data-role="assistant"] {
            background-color: #f1f8e9; /* Light green for assistant */
            align-self: flex-start;
            margin-right: auto;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- App Title ----------
st.title("💖BMI Calculator & Chatbot💖")

# --- BMI Calculator Section ---
st.markdown("---")
st.header("BMI Calculator")

with st.container():
    st.header("👤 Personal Information")
    name = st.text_input("Your Name", key="bmi_name_input") # Added key
    gender = st.radio("Gender", ("Male", "Female"), horizontal=True, key="bmi_gender_radio") # Added key
    age = st.number_input("Age", min_value=0, max_value=120, step=1, key="bmi_age_input") # Added key

st.markdown("---")

with st.container():
    st.header("📏 Measurements")
    height = st.number_input("Height (in meters)", min_value=0.0, format="%.2f", key="bmi_height_input") # Added key
    weight = st.number_input("Weight (in kilograms)", min_value=0.0, format="%.1f", key="bmi_weight_input") # Added key

# ---------- Calculate Button ----------
if st.button("🧮 Calculate BMI", key="bmi_calculate_button"): # Added key
    if height > 0 and weight > 0:
        bmi = weight / (height ** 2)
        st.markdown("---")
        st.subheader(f"👋 Hello, {name}!")
        st.success(f"Your BMI is **{bmi:.2f}**")

        user_question = f"health tips for bmi value of {bmi}."

        if user_question:
            with st.spinner("Thinking... 💡"):
                try:
                    response = model.generate_content(user_question)
                    st.markdown("#### Tips for your bmi:")
                    st.write(response.text)
                except Exception as e:
                    st.error("Something went wrong while getting a response from Gemini.")
                    st.exception(e)

        # Extra Tips Based on Age
    if age < 18:
        st.info("🧒 Since you're under 18, BMI might not reflect your health fully. Please consult a doctor.")
    elif age > 60:
        st.info("👵 You're over 60. Focus on muscle strength, healthy meals, and hydration.")
    else:
        st.error("⚠️ Please enter valid height and weight to calculate BMI.")

# --- Chatbot Section ---
st.markdown("---")
st.header("🤖 Ask the Chatbot Anything!")
st.write("I can answer general questions about health, fitness, and nutrition. Please note I am an AI and cannot provide medical advice.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    try:
        # Start a new chat session if it's the first message or if the session was reset
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
        
        # Send message to Gemini and get response
        response = st.session_state.chat_session.send_message(prompt)
        assistant_response = response.text

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"An error occurred: {e}. Please try again.")
        # Optionally, remove the last user message if an error occurred during response generation
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop()

# --- Footer ---
st.markdown("---")
st.caption("💻 Built with Python & Streamlit | Designed by You ✨")
