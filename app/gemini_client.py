from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from app.utils import clean_response, is_ending_conversation
import os
from dotenv import load_dotenv
load_dotenv()
# System prompt to guide Gemini's responses
SYSTEM_PROMPT = """You are a helpful voice assistant. Follow these rules:
1. Keep responses brief and conversational - under 40 words
2. Use only plain text - no asterisks, bullets, or special formatting
3. Respond directly to questions without offering additional options
4. If the user says "goodbye", "end", "stop", or similar, respond with ONLY "Goodbye! It was nice talking with you."
5. Provide complete sentences that work well when read aloud
"""

# Initialize Gemini LLM through LangChain
google_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=40,
    timeout=8,
    max_retries=2,
    system=SYSTEM_PROMPT
)

# Keep conversation history
conversation_history = []

def query_gemini(user_input):
    try:
        if is_ending_conversation(user_input):
            return "Goodbye! It was nice talking with you."
            
        conversation_history.append(HumanMessage(content=user_input))
        limited_history = conversation_history[-6:]
        
        response = google_llm.invoke(limited_history)
        clean_content = clean_response(response.content)
        
        conversation_history.append(AIMessage(content=clean_content))
        return clean_content
    except Exception as error:
        print('Error querying Gemini:', error)
        return "I'm sorry, I couldn't understand that. Could you try asking in a different way?"
