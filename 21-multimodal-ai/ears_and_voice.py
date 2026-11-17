# ears_and_voice.py: text-to-speech, then speech-to-text, on your CPU
# Voice: Kokoro (TTS). Ears: Whisper tiny (STT). No API key. (Episode 21)
import time
import soundfile as sf
from scipy.signal import resample_poly
import sherpa_onnx
from kokoro_onnx import Kokoro

W = "models/whisper-tiny.en/tiny.en-"

def speak(text, out="order.wav"):              # TTS: text -> audio
    tts = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
    audio, sr = tts.create(text, voice="hm_psi", speed=0.95, lang="en-us")
    sf.write(out, audio, sr)
    return out, len(audio) / sr                # file, seconds of speech

def listen(path):                              # STT: audio -> text
    ears = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=W + "encoder.int8.onnx", decoder=W + "decoder.int8.onnx",
        tokens=W + "tokens.txt", num_threads=2)
    audio, sr = sf.read(path, dtype="float32")
    if sr != 16000:                            # Whisper wants 16 kHz
        audio, sr = resample_poly(audio, 16000, sr).astype("float32"), 16000
    s = ears.create_stream()
    s.accept_waveform(sr, audio)
    ears.decode_stream(s)
    return s.result.text.strip()

if __name__ == "__main__":
    said = "Book a table for two at seven thirty tomorrow, near the window."
    t = time.time(); wav, secs = speak(said)
    print(f"TTS  {time.time() - t:4.1f}s  -> {wav} ({secs:.1f}s of speech)")
    t = time.time(); heard = listen(wav)
    print(f"STT  {time.time() - t:4.1f}s  -> {heard!r}")
