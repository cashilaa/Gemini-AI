import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from PIL import Image
import io
import random
import os
from dotenv import load_dotenv

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

def generate_health_chart(data_type, user_data=None):
    if data_type == "BMI Distribution":
        if user_data:
            df = pd.DataFrame(user_data)
        else:
            df = pd.DataFrame({
                "BMI Range": ["Underweight", "Normal", "Overweight", "Obese"],
                "Percentage": [10, 45, 30, 15]
            })
        fig = px.pie(df, values="Percentage", names="BMI Range", title="BMI Distribution")
    elif data_type == "Common Health Issues":
        if user_data:
            df = pd.DataFrame(user_data)
        else:
            df = pd.DataFrame({
                "Health Issue": ["Hypertension", "Diabetes", "Obesity", "Anxiety", "Depression"],
                "Prevalence": [25, 10, 35, 20, 15]
            })
        fig = px.bar(df, x="Health Issue", y="Prevalence", title="Prevalence of Common Health Issues")
    return fig

def get_daily_health_tip():
    tips = [
        "Drink at least 8 glasses of water today!",
        "Take a 10-minute walk to boost your mood and energy.",
        "Practice deep breathing for 5 minutes to reduce stress.",
        "Eat a serving of fruits and vegetables with each meal.",
        "Get 7-9 hours of sleep tonight for optimal health."
    ]
    return random.choice(tips)

def main():
    st.set_page_config(page_title="HealthMate AI", page_icon=":heart:", layout="wide")
    
    # Custom CSS for gray and black theme
    st.markdown("""
    <style>
    .big-font {
        font-size:36px !important;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .stApp {
        background-color: #2C2C2C;
        color: #E0E0E0 !important;
    }
    body {
        color: #E0E0E0;
    }
    p, .stMarkdown, .stText {
        color: #E0E0E0 !important;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stSelectbox {
        background-color: #3C3C3C;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">HealthMate AI</p>', unsafe_allow_html=True)
    st.write("Your comprehensive health companion powered by advanced AI")

    # Daily health tip
    st.info(f"💡 Daily Health Tip: {get_daily_health_tip()}")

    # Sidebar for different functionalities
    st.sidebar.title("Features")
    feature = st.sidebar.radio("Choose a feature:", ["Chat", "Image Analysis", "Health Charts", "Symptom Checker", "Meditation Guide", "Nutrition Planner"])

    if feature == "Chat":
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What health-related question do you have?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            full_prompt = f"""You are an advanced health AI assistant. Provide detailed information, predictions, or insights on the following health-related query:

            {prompt}

            Consider various aspects such as general health, medical conditions, wellness trends, nutrition, fitness, mental health, and public health. If asked for predictions, base them on current scientific understanding and trends. Include relevant statistics or data if applicable.

            Remember to include a disclaimer that this information is for educational purposes only and not a substitute for professional medical advice, diagnosis, or treatment."""

            response = get_gemini_response(full_prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    elif feature == "Image Analysis":
        st.subheader("Health Image Analysis")
        uploaded_file = st.file_uploader("Upload an image for health analysis", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            if st.button("Analyze Image"):
                with st.spinner("Analyzing..."):
                    image_prompt = "Analyze this health-related image and provide insights. Describe what you see and any potential health implications."
                    image_data = io.BytesIO()
                    image.save(image_data, format="PNG")
                    image_data = image_data.getvalue()
                    response = get_gemini_response(image_prompt, image_data)
                    st.write(response)

    elif feature == "Health Charts":
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
                user_data = {
                    "Health Issue": issues,
                    "Prevalence": []
                }
                for issue in issues:
                    prevalence = st.number_input(f"{issue} (%)", 0, 100, 20)
                    user_data["Prevalence"].append(prevalence)
            
            fig = generate_health_chart(chart_type, user_data)
        else:
            fig = generate_health_chart(chart_type)
        
        st.plotly_chart(fig)

    elif feature == "Symptom Checker":
        st.subheader("Basic Symptom Checker")
        symptoms = st.multiselect("Select your symptoms:", 
                                  ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", "Body aches"])
        if st.button("Check Symptoms"):
            if symptoms:
                symptom_prompt = f"Given the following symptoms: {', '.join(symptoms)}, what are some possible conditions to be aware of? Provide a brief overview and recommend when to seek professional medical advice."
                response = get_gemini_response(symptom_prompt)
                st.write(response)
            else:
                st.write("Please select at least one symptom.")

    elif feature == "Meditation Guide":
        st.subheader("Guided Meditation")
        meditation_type = st.selectbox("Choose a meditation type:", ["Mindfulness", "Stress Relief", "Sleep Aid"])
        duration = st.slider("Select duration (minutes):", 5, 30, 10)
        if st.button("Start Guided Meditation"):
            meditation_prompt = f"Provide a {duration}-minute guided meditation script for {meditation_type}. Include clear instructions and calming language."
            response = get_gemini_response(meditation_prompt)
            st.write(response)

    elif feature == "Nutrition Planner":
        st.subheader("Personalized Nutrition Plan")
        goal = st.selectbox("What's your nutrition goal?", ["Weight Loss", "Muscle Gain", "Balanced Diet"])
        dietary_restriction = st.multiselect("Any dietary restrictions?", ["Vegetarian", "Vegan", "Gluten-free", "Lactose-free"])
        if st.button("Generate Nutrition Plan"):
            plan_prompt = f"Create a one-day meal plan for {goal} with the following restrictions: {', '.join(dietary_restriction)}. Include breakfast, lunch, dinner, and two snacks with approximate calorie counts."
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