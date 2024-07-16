import pandas as pd
import plotly.express as px

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