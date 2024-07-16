# HealthMate AI

HealthMate AI is a comprehensive health companion powered by advanced AI, built using Streamlit and the Gemini AI model.


## Features

- AI-powered health chat
- Image analysis for health-related images
- Health data visualization
- Basic symptom checker
- Guided meditation scripts
- Personalized nutrition planning

## Installation

1. Clone this repository:
git clone https://github.com/cashilaa/gemini-AI.git
cd healthmate-ai
Copy
2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Copy
3. Install the required packages:
pip install -r requirements.txt
Copy
4. Set up your environment variables:
Create a `.env` file in the project root and add your Gemini API key:
GEMINI_API_KEY=your_api_key_here
Copy
## Usage

Run the Streamlit app:
streamlit run app.py
Copy
Navigate to the provided local URL in your web browser to use the application.

## Project Structure

- `app.py`: Main application file
- `utils.py`: Utility functions
- `charts.py`: Chart generation functions
- `prompts.py`: AI prompts and responses
- `styles.py`: CSS styles
- `.env`: Environment variables (not tracked in version control)
- `requirements.txt`: List of required Python packages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

HealthMate AI is for informational purposes only. Always consult with a qualified healthcare
