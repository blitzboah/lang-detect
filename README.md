# Language Detective Service

A FastAPI-based service that detects spoken languages in audio files using multiple AI providers for comparison and accuracy.

## Overview

This service integrates with 4 major AI providers to detect languages in audio files:
- **OpenAI Whisper** (Mock implementation)
- **Google Gemini** (Mock implementation)
- **Sarvam AI** (Full implementation)
- **ElevenLabs** (Full implementation)

## Requirements

- Python 3.10+
- UV package manager
- API keys for SarvamAI and ElevenLabs

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd language-detective-service
```

### 2. Install dependencies using UV
```bash
uv sync
```

### 3. Set up environment variables
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:
```env
SARVAM_API_KEY=your_sarvam_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 4. Create samples directory
```bash
mkdir samples
# Add your audio files to the samples/ directory
```

## Running the Service

### Start the FastAPI server
```bash
uvicorn main:app --reload
```

The service will be available at `http://127.0.0.1:8000`

### API Documentation
- Interactive docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Usage

### Endpoint: POST /detect/language

**Request:**
```json
{
    "audio_file_path": "samples/gujarati_sample.mp3",
    "ground_truth_language": "ta"
}
```

**Response:**
```json
[
  {
    "provider": "OpenAI",
    "language_raw": "mock",
    "language_normalized": "mock",
    "time_taken": "0.0s",
    "cost_usd": 0,
    "status": "success",
    "error": null,
    "accuracy": "incorrect",
    "ground_truth_normalized": "gu"
  },
  {
    "provider": "Google Gemini",
    "language_raw": "mock",
    "language_normalized": "mock",
    "time_taken": "0.0s",
    "cost_usd": 0,
    "status": "success",
    "error": null,
    "accuracy": "incorrect",
    "ground_truth_normalized": "gu"
  },
  {
    "provider": "SarvamAI",
    "language_raw": "gu",
    "language_normalized": "gu",
    "time_taken": "1.08s",
    "cost_usd": 0.0001,
    "status": "success",
    "error": null,
    "accuracy": "correct",
    "ground_truth_normalized": "gu"
  },
  {
    "provider": "ElevenLabs",
    "language_raw": "hin",
    "language_normalized": "hi",
    "time_taken": "2.12s",
    "cost_usd": 0.0002,
    "status": "success",
    "error": null,
    "accuracy": "incorrect",
    "ground_truth_normalized": "gu"
  }
]
```

### Example cURL command:
```bash
curl -X POST "http://127.0.0.1:8000/detect/language" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_file_path": "samples/tamil_sample.mp3",
    "ground_truth_language": "ta"
  }'
```

## Project Structure

```
├── connectors
│   ├── elevenlabs_connector.py
│   ├── gemini_connector.py
│   ├── openai_connector.py
│   └── sarvam_connector.py
├── coordinator.py
├── main.py
├── pyproject.toml
├── README.md
├── samples
│   ├── english_sample.mp3
│   ├── gujarati_sample.mp3
│   └── tamil_sample.mp3
└── uv.lock
```

## Testing

### Add sample audio files
Place your audio files in the `samples/` directory:
```
samples/
├── tamil_sample.mp3
├── gujarati_sample.mp3
├── english_sample.mp3
```

### Test with different languages audio that are under 30 seconds
```bash
# Tamil audio test
curl -X POST "http://127.0.0.1:8000/detect/language" \
  -H "Content-Type: application/json" \
  -d '{"audio_file_path": "samples/tamil_sample.mp3", "ground_truth_language": "ta"}'
```

## Configuration

### Environment Variables
- `SARVAM_API_KEY`: Your Sarvam AI API subscription key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
