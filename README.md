# Voice Assistant App

A powerful voice assistant application integrated with Twilio and Gemini LLM, enhanced with voice activity detection (VAD).

## 🚀 Features
- **Twilio Integration:** Seamlessly handle voice interactions via phone calls.
- **Gemini LLM Integration:** Provide intelligent responses using Google's Gemini model.
- **VAD:** Detects active speech using `webrtcvad` with audio preprocessing.
- **Modular Codebase:** Clean and maintainable structure following best practices.

## 📂 Project Structure
```
voice-assistant-app/
├── app/
│   ├── __init__.py            # Initializes the Flask app
│   ├── routes.py              # API routes and Twilio webhook
│   ├── gemini_client.py       # Gemini LLM integration
│   ├── vad.py                 # Voice Activity Detection (VAD) with preprocessing
│   └── utils.py               # Utility functions
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignored files
├── run.py                     # Start the Flask app
└── README.md                  # Project documentation
```

## 🛠️ Prerequisites
- **Python 3.8+**
- **Twilio Account:** Set up a phone number and webhook
- **Google Gemini API Key:** For LLM responses


## 🚧 Installation
```sh
# Clone the repository
git clone https://github.com/your-username/voice-assistant-app.git
cd voice-assistant-app

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with the following content:
```env
GEMINI_API_KEY=your_google_gemini_api_key
```

## 🚀 Run the Application
```sh
# Start the Flask server
python run.py
```
The server will be available at `http://localhost:3000`.

## 📞 Connect with Twilio
1. **Set Up a Twilio Phone Number:** Configure the phone number's webhook to `http://your-server-url/voice`.
2. **Test Calls:** Make a call to interact with the voice assistant.

## 🧪 Testing
- **Local Testing:** Use tools like `ngrok` to expose the local server to Twilio.
```sh
ngrok http 3000
```
- **Real Call Testing:** Make test calls to verify speech recognition and LLM responses.

## 💡 Troubleshooting
- Check `.env` variables are configured correctly.
- Review Flask logs for any errors during execution.

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Feel free to submit issues and pull requests! Contributions are welcome.

