# speech.py: speech-to-text (Whisper) + text-to-speech, 2 providers (Ep 22)
import requests
from settings import openai_client, STT, TTS, ELEVEN_URL, ELEVEN_KEY

def transcribe(path):                          # audio file -> text
    with open(path, "rb") as f:
        r = openai_client().audio.transcriptions.create(model=STT, file=f)
    return r.text

def openai_speak(text, out="reply_openai.mp3"):   # text -> audio file
    r = openai_client().audio.speech.create(
        model=TTS, voice="coral", input=text,
        instructions="Warm and friendly, like a helpful waiter.")
    r.write_to_file(out)
    return out

def eleven_speak(text, voice_id="JBFqnCBsd6RMkjVDRZzb",
                 out="reply_eleven.mp3"):
    r = requests.post(f"{ELEVEN_URL}/v1/text-to-speech/{voice_id}",
                      headers={"xi-api-key": ELEVEN_KEY},
                      json={"text": text, "model_id": "eleven_multilingual_v2"},
                      timeout=60)
    r.raise_for_status()
    open(out, "wb").write(r.content)
    return out

if __name__ == "__main__":
    heard = transcribe("order.wav")
    print("Whisper heard:", heard)
    reply = "Done. A table for two, tomorrow at 7:30 pm, by the window."
    for fn in (openai_speak, eleven_speak):
        path = fn(reply)
        size = len(open(path, "rb").read())
        print(f"{fn.__name__:13} -> {path} ({size:,} bytes)")
