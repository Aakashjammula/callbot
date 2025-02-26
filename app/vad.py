import webrtcvad, requests, io, wave

def is_voice_active(audio_url):
    try:
        # Download the audio data
        audio_data = requests.get(audio_url).content
        audio_file = io.BytesIO(audio_data)
        
        with wave.open(audio_file, 'rb') as wf:
            # Check audio properties
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                print("VAD requires 16-bit mono audio")
                return True  # Default to assuming speech if format is wrong
                
            sample_rate = wf.getframerate()
            # WebRTC VAD only supports 8kHz, 16kHz, 32kHz, 48kHz
            if sample_rate not in [8000, 16000, 32000, 48000]:
                print(f"Unsupported sample rate: {sample_rate}Hz")
                return True  # Default to assuming speech if sample rate is unsupported
            
            # Initialize VAD with aggressiveness level 3 (0-3, 3 is most aggressive)
            vad = webrtcvad.Vad(3)
            
            # Process in 30ms chunks (sample_rate * 0.03 samples per chunk)
            frame_duration_ms = 30
            frame_size = int(sample_rate * frame_duration_ms / 1000)
            
            # Read all audio data
            wf.rewind()
            pcm_data = wf.readframes(wf.getnframes())
            
            # Count speech frames
            total_frames = 0
            speech_frames = 0
            
            # Process each 30ms chunk
            for i in range(0, len(pcm_data), frame_size*2):  # *2 because 16-bit audio = 2 bytes per sample
                chunk = pcm_data[i:i+frame_size*2]
                
                # Ensure chunk is exactly frame_size*2 bytes (required by WebRTC VAD)
                if len(chunk) == frame_size*2:
                    total_frames += 1
                    if vad.is_speech(chunk, sample_rate):
                        speech_frames += 1
            
            # Calculate speech ratio
            if total_frames == 0:
                return False
                
            speech_ratio = speech_frames / total_frames
            print(f"Speech detection: {speech_frames}/{total_frames} frames ({speech_ratio:.2%})")
            
            # Consider it speech if at least 10% of frames contain speech
            return speech_ratio >= 0.10
            
    except Exception as e:
        print(f"VAD error: {e}")
        return True  # Default to assuming speech on error