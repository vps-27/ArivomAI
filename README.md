Arivom AI – அறிவோம் AI

A Tamil-first digital fraud awareness platform that helps users understand and identify online scams through interactive learning and voice-based assistance.

About the Project

With the increasing use of digital payments and online services, digital fraud has become a major concern. Many people find it difficult to identify fraudulent calls, phishing links, fake job offers and UPI scams.

Arivom AI aims to make digital fraud awareness accessible through simple Tamil explanations, voice interactions and simulated scam scenarios.

Features

1. Digital Fraud Awareness
   - Ask questions about suspicious calls, messages and online activities.
   - Get simple Tamil explanations and safety guidance.

2. Tamil Voice Interaction
   - Convert Tamil speech into text using Gnani Prisma.
   - Generate Tamil audio responses using Gnani Timbre.

3. Scam Drill
   - Practise responding to simulated fraud situations.
   - Includes bank OTP fraud, UPI collect request fraud, fake job offers and phishing SMS.
   - Uses Google Gemini to evaluate responses and provide feedback.

4. Safety Guide
   - Learn about common digital scams and safety practices.
   - Understand how to respond to suspicious activities.

5. Progress Tracking
   - Track practice attempts and safe responses.
   - View your practice performance.

Technology Stack

- Python
- Streamlit
- Google Gemini API
- Gnani Prisma (Speech-to-Text)
- Gnani Timbre (Text-to-Speech)
- REST APIs
- Git and GitHub

Project Structure

ArivomAI/
    ArivomAI_Gemini_app.py
    requirements.txt
    .gitignore
    README.md
    assets/

Getting Started

1. Clone the repository

git clone https://github.com/vps-27/ArivomAI.git

2. Install the dependencies

pip install -r requirements.txt

3. Create a .env file and add your API credentials

GNANI_API_KEY=your_gnani_api_key
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

4. Run the application

streamlit run ArivomAI_Gemini_app.py

Note: Keep your API keys private. Do not upload the .env file to GitHub.

Project Objective

To make digital fraud awareness easier to understand and accessible to Tamil-speaking users through AI and voice technologies.

Future Scope

- Support for more Indian languages.
- Addition of more fraud scenarios.
- Improved interactive learning experiences.
- Expanded digital safety awareness resources.

Arivom AI – அறிவோம். விழிப்போம். பாதுகாப்போம்.
