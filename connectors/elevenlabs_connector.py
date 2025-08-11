import os
from io import BytesIO
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=eleven_api_key)

def detect_language(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            audio_data = BytesIO(f.read())

        response = client.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",
            diarize=False,
            tag_audio_events=False
        )

        if not isinstance(response, dict):
            response = response.dict()

        if "language_code" in response and response["language_code"]:
            return response["language_code"].split("-")[0]

        raise RuntimeError(f"ElevenLabs did not return a language_code: {response!r}")

    except Exception as e:
        raise RuntimeError(f"ElevenLabs detection failed: {e}")
