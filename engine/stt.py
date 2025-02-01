import os
import pydub
import requests
from dotenv import load_dotenv

load_dotenv()


class STT:
    def __init__(self):
        HF_TOKEN = os.getenv('HF_TOKEN')
        HF_MODEL_URL = os.getenv('HF_MODEL_URL')
        self.API_URL = HF_MODEL_URL
        self.headers = {
            "Accept" : "application/json",
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "audio/wav" 
        }

    def transcribe(self, audio_path: str):
        with open(audio_path, "rb") as audio:
            response = requests.post(self.API_URL, headers=self.headers, data=audio)
            if response.status_code != 200:
                return None
        return response.json().get('text')
