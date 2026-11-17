# Episode 21: Multimodal AI (AI Engineer Roadmap) · code

Everything here runs on your own CPU. No API key, no internet after setup.

| File | What it shows |
|---|---|
| `make_samples.py` | Draws `receipt.png`, a small cafe receipt to test with |
| `see_image.py` | How a vision model "sees": cuts the image into 32x32 patches, then estimates the tokens an image or a video costs |
| `ears_and_voice.py` | Text-to-speech with Kokoro, then speech-to-text with Whisper tiny |
| `voice_agent.py` | A tiny voice agent: hear (STT) → think → speak (TTS), with the time of every stage. The "think" step is a **demo stand-in with fixed rules**, not a real LLM |

## Setup (Windows, macOS or Linux, Python 3.10+)

```bash
pip install -r requirements.txt
mkdir models
```

Download the model files from GitHub into `models/`:

* Kokoro voice: `kokoro-v1.0.onnx` and `voices-v1.0.bin` from https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
* Whisper tiny (English): `sherpa-onnx-whisper-tiny.en.tar.bz2` from https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models, unpack it and rename the folder to `models/whisper-tiny.en`

## Run

```bash
python make_samples.py
python see_image.py
python ears_and_voice.py
python voice_agent.py
```

Output we got (2026-11-11, 4-core CPU):

```
patches: 196 | numbers per patch: 3072
receipt 600x800        openai high   765 | low  85 | claude   640
phone photo 4032x3024  openai high   765 | low  85 | claude  1533
video  1 min  ~   15,780 tokens
video 10 min  ~  157,800 tokens
video 60 min  ~  946,800 tokens

TTS   2.6s  -> order.wav (4.1s of speech)
STT   0.8s  -> 'Book a table for two at 730 tomorrow near the window.'

heard : Book a table for two at 730 tomorrow near the window.
reply : Done. A table for two, tomorrow at 7:30 pm, by the window.
hear 1.02s | think 0.00s | speak 2.60s | total 3.62s
```

Notes:
* Token rules are estimates from the providers' docs at the time of recording (OpenAI GPT-4o style 512 px tiles: 85 + 170 per tile, low detail 85; Claude about width x height / 750 after resizing; Gemini video about 263 tokens per second). Rules differ per model and change, so check the current docs.
* Tiny Whisper wrote "seven thirty" as "730". Real apps clean up what speech-to-text gives them before they act on it.
* Most of the TTS time is loading the model. A real voice agent loads models once and streams audio.
