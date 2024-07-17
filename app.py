import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv

from prompts import *
from charts import generate_health_chart
from styles import get_custom_css
from utils import get_daily_health_tip

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set up the model
model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(prompt, image=None):
    if image:
        response = vision_model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

def main():
    st.set_page_config(page_title="HealthMate AI", page_icon=":heart:", layout="wide")
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown('<p class="big-font">HealthMate AI</p>', unsafe_allow_html=True)
    st.write("Your comprehensive health companion powered by advanced AI")

    # Daily health tip
    st.info(f"💡 Daily Health Tip: {get_daily_health_tip()}")

    # Sidebar for different functionalities
    st.sidebar.title("Features")
    feature = st.sidebar.radio("Choose a feature:", ["Chat", "Image Analysis", "Health Charts", "Symptom Checker", "Meditation Guide", "Nutrition Planner"])

    if feature == "Chat":
        # Chat functionality
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What health-related question do you have?"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            full_prompt = get_chat_prompt(prompt)
            response = get_gemini_response(full_prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    elif feature == "Image Analysis":
        # Image Analysis functionality
        st.subheader("Health Image Analysis")
        uploaded_file = st.file_uploader("Upload an image for health analysis", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Analyze Image"):
                with st.spinner("Analyzing..."):
                    image_prompt = get_image_analysis_prompt()
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    image_part = {"mime_type": "image/png", "data": img_byte_arr}
                    response = get_gemini_response(image_prompt, image_part)
                    st.write(response)

    elif feature == "Health Charts":
        # Health Charts functionality
        st.subheader("Health Data Visualization")
        chart_type = st.selectbox("Select chart type:", ["BMI Distribution", "Common Health Issues"])
        use_custom_data = st.checkbox("Use custom data")
        
        if use_custom_data:
            if chart_type == "BMI Distribution":
                st.write("Enter percentages for each BMI category:")
                underweight = st.number_input("Underweight (%)", 0, 100, 10)
                normal = st.number_input("Normal (%)", 0, 100, 45)
                overweight = st.number_input("Overweight (%)", 0, 100, 30)
                obese = st.number_input("Obese (%)", 0, 100, 15)
                user_data = {
                    "BMI Range": ["Underweight", "Normal", "Overweight", "Obese"],
                    "Percentage": [underweight, normal, overweight, obese]
                }
            elif chart_type == "Common Health Issues":
                st.write("Enter prevalence for each health issue:")
                issues = ["Hypertension", "Diabetes", "Obesity", "Anxiety", "Depression"]
                user_data = {"Health Issue": issues, "Prevalence": []}
                for issue in issues:
                    prevalence = st.number_input(f"{issue} (%)", 0, 100, 20)
                    user_data["Prevalence"].append(prevalence)
            fig = generate_health_chart(chart_type, user_data)
        else:
            fig = generate_health_chart(chart_type)
        st.plotly_chart(fig)

    elif feature == "Symptom Checker":
        # Symptom Checker functionality
        st.subheader("Basic Symptom Checker")
        symptoms = st.multiselect("Select your symptoms:", 
                                  ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", "Body aches"])
        if st.button("Check Symptoms"):
            if symptoms:
                symptom_prompt = get_symptom_checker_prompt(symptoms)
                response = get_gemini_response(symptom_prompt)
                st.write(response)
            else:
                st.write("Please select at least one symptom.")

    elif feature == "Meditation Guide":
        # Meditation Guide functionality
        st.subheader("Guided Meditation")
        meditation_type = st.selectbox("Choose a meditation type:", ["Mindfulness", "Stress Relief", "Sleep Aid"])
        duration = st.slider("Select duration (minutes):", 5, 30, 10)
        if st.button("Start Guided Meditation"):
            meditation_prompt = get_meditation_prompt(meditation_type, duration)
            response = get_gemini_response(meditation_prompt)
            st.write(response)

    elif feature == "Nutrition Planner":
        # Nutrition Planner functionality
        st.subheader("Personalized Nutrition Plan")
        goal = st.selectbox("What's your nutrition goal?", ["Weight Loss", "Muscle Gain", "Balanced Diet"])
        dietary_restriction = st.multiselect("Any dietary restrictions?", ["Vegetarian", "Vegan", "Gluten-free", "Lactose-free"])
        if st.button("Generate Nutrition Plan"):
            plan_prompt = get_nutrition_plan_prompt(goal, dietary_restriction)
            response = get_gemini_response(plan_prompt)
            st.write(response)

    # Footer
    st.markdown("---")
    st.markdown("**Disclaimer:** HealthMate AI is for informational purposes only. Always consult with a qualified healthcare provider for medical advice.")
    
    # Feedback
    st.sidebar.markdown("---")
    if st.sidebar.button("Give Feedback"):
        st.sidebar.text_area("We'd love to hear your thoughts!", key="feedback")
        if st.sidebar.button("Submit Feedback"):
            st.sidebar.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
