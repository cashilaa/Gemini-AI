def get_chat_prompt(user_query):
    return f"""You are an advanced health AI assistant. Provide detailed information, predictions, or insights on the following health-related query:

    {user_query}

    Consider various aspects such as general health, medical conditions, wellness trends, nutrition, fitness, mental health, and public health. If asked for predictions, base them on current scientific understanding and trends. Include relevant statistics or data if applicable.

    Remember to include a disclaimer that this information is for educational purposes only and not a substitute for professional medical advice, diagnosis, or treatment."""

def get_image_analysis_prompt():
    return "Analyze this health-related image and provide insights. Describe what you see and any potential health implications."

def get_symptom_checker_prompt(symptoms):
    return f"Given the following symptoms: {', '.join(symptoms)}, what are some possible conditions to be aware of? Provide a brief overview and recommend when to seek professional medical advice."

def get_meditation_prompt(meditation_type, duration):
    return f"Provide a {duration}-minute guided meditation script for {meditation_type}. Include clear instructions and calming language."

def get_nutrition_plan_prompt(goal, dietary_restrictions):
    return f"Create a one-day meal plan for {goal} with the following restrictions: {', '.join(dietary_restrictions)}. Include breakfast, lunch, dinner, and two snacks with approximate calorie counts."
