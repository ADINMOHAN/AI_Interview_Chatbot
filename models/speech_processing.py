from gtts import gTTS
import os
import tempfile
import playsound


def text_to_speech(text):
    try:
        # Generate speech from the provided text
        tts = gTTS(text=text, lang='en')
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            
            # Play the generated speech
            playsound.playsound(fp.name)
        
        # Delete the temporary file after playing
        os.remove(fp.name)
    
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
