import streamlit as st
from utils import get_daily_health_tip, load_environment
from charts import generate_health_chart
from prompts import get_gemini_response
import styles

def main():
    load_environment()
    st.set_page_config(page_title="HealthMate AI", page_icon=":heart:", layout="wide")
    styles.apply_custom_css()

    st.markdown('<p class="big-font">HealthMate AI</p>', unsafe_allow_html=True)
    st.write("Your comprehensive health companion powered by advanced AI")

    st.info(f"💡 Daily Health Tip: {get_daily_health_tip()}")

    st.sidebar.title("Features")
    feature = st.sidebar.radio("Choose a feature:", ["Chat", "Image Analysis", "Health Charts", "Symptom Checker", "Meditation Guide", "Nutrition Planner"])

    if feature == "Chat":
        chat_feature()
    elif feature == "Image Analysis":
        image_analysis_feature()
    elif feature == "Health Charts":
        health_charts_feature()
    elif feature == "Symptom Checker":
        symptom_checker_feature()
    elif feature == "Meditation Guide":
        meditation_guide_feature()
    elif feature == "Nutrition Planner":
        nutrition_planner_feature()

    display_footer()
    display_feedback()

def chat_feature():
    st.subheader("Health Chat")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What health-related question do you have?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        full_prompt = f"""You are an advanced health AI assistant. Provide detailed information, predictions, or insights on the following health-related query:

        {prompt}

        Consider various aspects such as general health, medical conditions, wellness trends, nutrition, fitness, mental health, and public health. If asked for predictions, base them on current scientific understanding and trends. Include relevant statistics or data if applicable.

        Remember to include a disclaimer that this information is for educational purposes only and not a substitute for professional medical advice, diagnosis, or treatment."""

        response = get_gemini_response(full_prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def image_analysis_feature():
    pass

def health_charts_feature():
    pass

def symptom_checker_feature():
    pass

def meditation_guide_feature():
    pass

def nutrition_planner_feature():
    pass

def display_footer():
    st.markdown("---")
    st.markdown("**Disclaimer:** HealthMate AI is for informational purposes only. Always consult with a qualified healthcare provider for medical advice.")

def display_feedback():
    st.sidebar.markdown("---")
    if st.sidebar.button("Give Feedback"):
        st.sidebar.text_area("We'd love to hear your thoughts!", key="feedback")
        if st.sidebar.button("Submit Feedback"):
            st.sidebar.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
