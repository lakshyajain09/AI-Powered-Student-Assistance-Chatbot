import os
import random
import openai  

# Set OpenAI API key
openai.api_key = "Enter your API-key"

def generate_response(intent, user_message, education_info):
    """
    Generate response using OpenAI API based on predicted intent
    
    Args:
        intent: The predicted intent from the model
        user_message: The original message from the user
        education_info: Dict containing education information
    
    Returns:
        str: The generated response
    """
    # For greeting, goodbye, thanks - use predefined responses
    if intent in ["greeting", "goodbye", "thanks"]:
        from app import intents
        responses = next((item["responses"] for item in intents["intents"] 
                         if item["tag"] == intent), None)
        if responses:
            return random.choice(responses)
    
    # For fallback intent
    if intent == "fallback":
        return "I'm not sure I understand. Could you rephrase your question about admissions, courses, scholarships, events, results, or grievance redressal?"
    
    # Extract relevant information based on intent
    context_info = {}
    if intent == "admissions":
        context_info = {course["name"]: course["admission_process"] for course in education_info["courses"]}
    elif intent == "courses":
        context_info = {course["name"]: {
            "branches": course.get("branches", []),
            "duration": course.get("duration", ""),
            "eligibility": course.get("eligibility", "")
        } for course in education_info["courses"]}
    elif intent == "scholarships":
        context_info = {scholarship["name"]: {
            "type": scholarship.get("type", ""),
            "details": scholarship.get("details", ""),
            "how_to_apply": scholarship.get("how_to_apply", "")
        } for scholarship in education_info["scholarships"]}
    elif intent == "events":
        context_info = {event["name"]: {
            "type": event.get("type", ""),
            "date": event.get("date", ""),
            "venue": event.get("venue", ""),
            "details": event.get("details", "")
        } for event in education_info["events"]}
    elif intent == "results":
        context_info = {f"{result['type']} {result['period']}": {
            "date": result.get("date", ""),
            "how_to_check": result.get("how_to_check", "")
        } for result in education_info["results"]}
    elif intent == "grievance":
        context_info = {grievance["type"]: {
            "contact": grievance.get("contact", ""),
            "procedure": grievance.get("procedure", "")
        } for grievance in education_info["grievances"]}
    
    # Generate response using OpenAI API
    try:
        prompt = f"""
        As a DTE Rajasthan Student Assistance Chatbot, generate a helpful response to the following user query.
        User query: {user_message}
        
        The query is related to: {intent}
        
        Available information on this topic:
        {context_info}
        
        Keep your response concise, friendly, and specific to the information provided.
        Focus on answering exactly what was asked without unnecessary details.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the Department of Technical Education, Rajasthan."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "I'm currently having trouble processing your request. Please try again later or contact the Department of Technical Education directly for assistance."
