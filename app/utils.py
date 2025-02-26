import re

def clean_response(text):
    text = re.sub(r'\*+\s*', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_ending_conversation(user_input):
    ending_phrases = ["goodbye", "bye", "end", "stop", "exit", "quit", "thank you", "thanks"]
    return any(phrase in user_input.lower() for phrase in ending_phrases)
