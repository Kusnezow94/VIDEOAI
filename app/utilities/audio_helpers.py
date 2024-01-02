```python
import requests
from app.models import User

def generate_audio(script, user_id):
    """
    This function uses the ElevenLabs API to generate audio from a given script.
    It requires the script text and the user's ID to retrieve the user-specific API key.
    
    :param script: The text script from which to generate audio.
    :param user_id: The ID of the user who is requesting the audio generation.
    :return: The URL of the generated audio file or None if an error occurs.
    """
    user = User.query.get(user_id)
    if not user or not user.elevenlabs_api_key:
        return None

    # Replace 'your_elevenlabs_api_url' with the actual ElevenLabs API URL
    elevenlabs_api_url = 'your_elevenlabs_api_url'
    headers = {
        'Authorization': f'Bearer {user.elevenlabs_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'script': script,
        # You can add more parameters here according to ElevenLabs API documentation
    }

    try:
        response = requests.post(elevenlabs_api_url, json=data, headers=headers)
        response.raise_for_status()
        # Assuming the API returns a JSON with an 'audio_url' field with the URL of the generated audio
        audio_url = response.json().get('audio_url')
        return audio_url
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while generating audio: {e}")
        return None
```