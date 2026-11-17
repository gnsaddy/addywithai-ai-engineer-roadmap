# Episode 22: Multimodal APIs (AI Engineer Roadmap) · code

Call vision, speech, image and video APIs from Python.

| File | What it does |
|---|---|
| `settings.py` | Keys, endpoints and model names in one place (`--demo` points everything at the local stand-in) |
| `vision.py` | Sends `receipt.png` to OpenAI (detail low and high) and to Gemini, asks for JSON, prints the tokens used |
| `speech.py` | Speech-to-text with Whisper (`order.wav`), text-to-speech with OpenAI and with ElevenLabs |
| `generate.py` | Makes an image (OpenAI image API) and a video (Google Veo on Vertex AI, a slow job you poll) |
| `stand_in_server.py` | **Demo only.** A local fake API with the same HTTP shapes as OpenAI, Gemini, Vertex AI and ElevenLabs. It returns **fixed answers** (no model, no thinking): a fixed receipt JSON, a fixed transcript, a beep instead of a voice, a blank demo image and a tiny demo clip |

## Setup

```bash
pip install -r requirements.txt
```

## Demo run (offline, no keys)

```bash
python stand_in_server.py        # terminal 1, leave it running
python vision.py --demo          # terminal 2
python speech.py --demo
python generate.py --demo
```

Output we got (2026-11-11):

```
OpenAI (low )  105 tokens -> {'shop': 'UDUPI CAFE', 'total': 273.0, 'items': 4}
OpenAI (high)  785 tokens -> {'shop': 'UDUPI CAFE', 'total': 273.0, 'items': 4}
Gemini         282 tokens -> {'shop': 'UDUPI CAFE', 'total': 273.0, 'items': 4}

Whisper heard: Book a table for two at 7:30 tomorrow, near the window.
openai_speak  -> reply_openai.mp3 (32,044 bytes)
eleven_speak  -> reply_eleven.mp3 (32,044 bytes)

image -> poster.png
  job veo_demo1: still rendering...
  job veo_demo1: still rendering...
  job veo_demo1: still rendering...
video -> clip.mp4
```

The token numbers in demo mode come from the stand-in using the published tile rule (low detail 85, high detail 85 + 170 per 512 px tile, plus about 20 text tokens; Gemini about 258 per image), not from a real model.

## Real run

Copy `.env.example`, fill in the keys you have (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `VERTEX_API_KEY` for Veo with Vertex AI express mode) and run the files without `--demo`. Each call costs money on your account. Model names change often: check each provider's docs and set the names in `.env`.

Things we found while making this episode (2026-11-11, from the SDKs' own notices):
* `openai` 3.49.0 says the Sora video API was shut down on 24 September 2026, so the video example uses Google Veo.
* `openai` 3.49.0 says the `tts-1`, `tts-1-hd` and `gpt-4o-mini-tts` speech models are scheduled to shut down on 6 January 2027 (move to the Realtime API). `speech.py` still works today; swap the model when you migrate.
* `google-genai` 3.1.0 runs `generate_videos` only in Vertex AI mode, so `video_client()` uses `vertexai=True`.
