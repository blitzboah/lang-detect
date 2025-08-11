import os
from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SARVAM_API_KEY")
client = SarvamAI(api_subscription_key=api_key)

def detect_language(file_path: str) -> str:
    try:
        with open(file_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model="saarika:v2.5",
                language_code="unknown"
            )

        if isinstance(response, dict):
            lang_code = response.get("language_code")
            if lang_code:
                return lang_code.split("-")[0]

        if hasattr(response, "language_code") and response.language_code:
            return response.language_code.split("-")[0]

        raise RuntimeError(
            f"Sarvam AI did not return a valid language_code in the response: {response!r}"
        )

    except Exception as e:
        raise RuntimeError(f"Sarvam AI detection failed: {e}")
