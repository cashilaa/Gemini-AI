import random
import os
from dotenv import load_dotenv

def get_daily_health_tip():
    tips = [
        "Drink at least 8 glasses of water today!",
        "Take a 10-minute walk to boost your mood and energy.",
        "Practice deep breathing for 5 minutes to reduce stress.",
        "Eat a serving of fruits and vegetables with each meal.",
        "Get 7-9 hours of sleep tonight for optimal health."
    ]
    return random.choice(tips)

def load_environment():
    load_dotenv()