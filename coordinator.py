import time
from typing import Optional

from connectors import (
    openai_connector,
    gemini_connector,
    sarvam_connector,
    elevenlabs_connector
)

# Language code standardization mapping
LANGUAGE_CODE_MAPPING = {
    # Tamil variations
    "ta": "ta", "tam": "ta", "tamil": "ta",

    # Hindi variations
    "hi": "hi", "hin": "hi", "hindi": "hi",

    # English variations
    "en": "en", "eng": "en", "english": "en",

    # Bengali variations
    "bn": "bn", "ben": "bn", "bengali": "bn",

    # Telugu variations
    "te": "te", "tel": "te", "telugu": "te",

    # Marathi variations
    "mr": "mr", "mar": "mr", "marathi": "mr",

    # Gujarati variations
    "gu": "gu", "guj": "gu", "gujarati": "gu",

    # Kannada variations
    "kn": "kn", "kan": "kn", "kannada": "kn",

    # Malayalam variations
    "ml": "ml", "mal": "ml", "malayalam": "ml",

    # Punjabi variations
    "pa": "pa", "pan": "pa", "punjabi": "pa",
}

def normalize_language_code(lang_code: str) -> str:
    if not lang_code:
        return lang_code

    normalized = lang_code.lower().strip()

    if "-" in normalized:
        normalized = normalized.split("-")[0]

    return LANGUAGE_CODE_MAPPING.get(normalized, normalized)

def run_connector(connector_func, provider_name: str, file_path: str, ground_truth: Optional[str] = None):
    start_time = time.time()
    status = "success"
    error_msg = None
    language_code: Optional[str] = None
    normalized_language: Optional[str] = None
    accuracy = None

    try:
        raw_language_code = connector_func(file_path)
        language_code = raw_language_code
        normalized_language = normalize_language_code(raw_language_code)

        if ground_truth and normalized_language:
            normalized_ground_truth = normalize_language_code(ground_truth)
            accuracy = "correct" if normalized_language == normalized_ground_truth else "incorrect"

    except Exception as e:
        status = "error"
        error_msg = str(e)

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    cost_data = calculate_cost(provider_name, time_taken)

    result = {
        "provider": provider_name,
        "language_raw": language_code,
        "language_normalized": normalized_language,
        "time_taken": f"{time_taken}s",
        "cost_usd": cost_data["cost_usd"],
        "status": status,
        "error": error_msg
    }

    if ground_truth:
        result["accuracy"] = accuracy
        result["ground_truth_normalized"] = normalize_language_code(ground_truth)

    return result

def calculate_cost(provider_name: str, time_taken: float):
    if provider_name == "SarvamAI":
        # INR 30 per hour
        rate_inr_per_sec = 30 / 3600
        cost_in_inr = time_taken * rate_inr_per_sec
        usd_rate = 87
        cost_usd = round(cost_in_inr / usd_rate, 4)

        return {
            "cost_usd": cost_usd,
            "cost_inr": round(cost_in_inr, 4),
            "rate": "INR 30/hour"
        }

    if provider_name == "ElevenLabs":
        # $0.40 per hour
        cost_per_sec_usd = 0.40 / 3600
        cost_usd = round(time_taken * cost_per_sec_usd, 4)

        return {
            "cost_usd": cost_usd,
            "rate": "$0.40/hour"
        }

    if provider_name == "OpenAI":
        # Whisper API: ~$0.006 per minute
        estimated_cost = round((time_taken / 60) * 0.006, 4)
        return {
            "cost_usd": estimated_cost,
            "rate": "~$0.006/minute (estimated)"
        }

    if provider_name == "Google Gemini":
        estimated_cost = round((time_taken / 60) * 0.004, 4)
        return {
            "cost_usd": estimated_cost,
            "rate": "~$0.004/minute (estimated)"
        }

    return {"cost_usd": 0, "rate": "free/unknown"}

def detect_language_all(file_path: str, ground_truth: Optional[str] = None):
    results = []

    # OpenAI (mock)
    results.append(run_connector(
        openai_connector.detect_language,
        "OpenAI",
        file_path,
        ground_truth
    ))

    # Google Gemini (mock)
    results.append(run_connector(
        gemini_connector.detect_language,
        "Google Gemini",
        file_path,
        ground_truth
    ))

    # SarvamAI (real)
    results.append(run_connector(
        sarvam_connector.detect_language,
        "SarvamAI",
        file_path,
        ground_truth
    ))

    # ElevenLabs (real)
    results.append(run_connector(
        elevenlabs_connector.detect_language,
        "ElevenLabs",
        file_path,
        ground_truth
    ))

    return results
