# AI-Powered Student Assistance Chatbot

A Flask-based chatbot application that provides instant responses to student queries regarding technical education services and policies offered by the Department of Technical Education, Government of Rajasthan.

## Project Overview

This chatbot uses Natural Language Processing (NLP) and Machine Learning to understand user queries and provide accurate responses about admissions, courses, scholarships, events, results, and grievance redressal procedures.

## Team Members

1. Gunjan Nama (22EJCCS210)
2. Ritu Sharma (21EJCCS189)
3. Naham Hussain (22EJCCS216)
4. Lakshya Jain (22EJCCS213)

Project Guide: Mr. Amit Mithal, Associate Professor, Department of CSE

## Features

- Natural language understanding for student queries
- Real-time responses to questions about:
  - Admission processes
  - Course details
  - Scholarship information
  - Upcoming events
  - Examination results
  - Grievance redressal procedures
- User-friendly web interface
- Suggested queries for better user experience

## Technologies Used

- **Backend**: Python, Flask
- **NLP & ML**: NLTK, TensorFlow, Keras
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON (for prototype)

## Installation & Setup

1. Clone the repository:

   ```
   git clone https://github.com/lakshyajain09/ai-powered-student-assistance-chatbot.git
   cd ai-powered-student-assistance-chatbot
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   python app.py
   ```

5. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

- `app.py`: Main Flask application
- `requirements.txt`: Dependencies
- `static/`: Contains CSS and JavaScript files
- `templates/`: HTML templates
- `models/`: ML models for NLP
- `data/`: Training data and educational information
- `utils/`: Utility functions for response generation

## Future Enhancements

- Voice recognition capabilities
- Multilingual support
- Integration with additional services (online fee payment, examination scheduling)
- Career counseling features
- Mobile application version

## References

- NLTK documentation: https://www.nltk.org/
- TensorFlow documentation: https://www.tensorflow.org/
- Flask documentation: https://flask.palletsprojects.com/
