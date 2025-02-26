from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather
from app import app, executor
from app.gemini_client import query_gemini
from app.vad import is_voice_active
from app.utils import is_ending_conversation
@app.route('/')
def home():
    return "Voice Assistant Server is running. Use POST /voice for Twilio webhook."

@app.route('/voice', methods=['POST'])
def voice():
    response = VoiceResponse()
    speech_result = request.form.get('SpeechResult')
    recording_url = request.form.get('RecordingUrl')
    
    # Check if this is the initial call (no speech result yet)
    if not speech_result and not recording_url:
        gather = Gather(input='speech', speech_timeout='auto', action='/voice')
        prompt = 'Hello i am a general assistant,what can i help you with today'
        gather.say(prompt, voice='alice')
        response.append(gather)
        return str(response), 200, {'Content-Type': 'text/xml'}
     
    if recording_url and not speech_result:
        if not is_voice_active(recording_url):
            response.say("I didn't quite catch that. Could you speak a bit louder?", voice='alice')
            gather = Gather(input='speech', speech_timeout='auto', action='/voice')
            response.append(gather)
            return str(response), 200, {'Content-Type': 'text/xml'}
        else:
            # Voice detected but speech not recognized
            response.say("I heard you speaking but couldn't understand. Could you try again?", voice='alice')
            gather = Gather(input='speech', speech_timeout='auto', action='/voice')
            response.append(gather)
            return str(response), 200, {'Content-Type': 'text/xml'}
    
    # Process the recognized speech
    if speech_result:
        try:
            future = executor.submit(query_gemini, speech_result)
            gemini_response = future.result(timeout=10)
            response.say(gemini_response, voice='alice')
            
            # If the user is ending the conversation, don't gather more input
            if is_ending_conversation(speech_result):
                # End call after goodbye message
                response.hangup()
            else:
                # Add a brief pause before asking for next input
                response.pause(length=1)
                gather = Gather(input='speech', speech_timeout='auto', action='/voice')
                gather.say("Anything else?", voice='alice')
                response.append(gather)
                
        except Exception as error:
            print('Error processing request:', error)
            response.say('Sorry, I had trouble with that request. Let\'s try again.', voice='alice')
            gather = Gather(input='speech', speech_timeout='auto', action='/voice')
            response.append(gather)
    else:
        gather = Gather(input='speech', speech_timeout='auto', action='/voice')
        prompt = 'What can I help you with today?'
        gather.say(prompt, voice='alice')
        response.append(gather)

    return str(response), 200, {'Content-Type': 'text/xml'}