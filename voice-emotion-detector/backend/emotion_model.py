import torchaudio
import os
from pathlib import Path
from speechbrain.inference.classifiers import EncoderClassifier
import speechbrain.utils.fetching as fetching

# Fix for symlink issues on Windows
os.environ["SPEECHBRAIN_LOCAL_FETCH_STRATEGY"] = "copy"
original_fetch = fetching.fetch

def force_copy_strategy(*args, **kwargs):
    kwargs["local_strategy"] = "copy"
    return original_fetch(*args, **kwargs)

fetching.fetch = force_copy_strategy

# Ensure model path exists
model_path = os.path.join(os.getcwd(), "speechbrain_models")
os.makedirs(model_path, exist_ok=True)

# Load the SpeechBrain classifier
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    savedir=model_path
)

# Convert .webm to .wav (for browser recordings)
def convert_to_wav(input_path):
    try:
        waveform, sample_rate = torchaudio.load(input_path)
        wav_path = input_path.replace(".webm", ".wav")
        torchaudio.save(wav_path, waveform, sample_rate)
        return wav_path
    except Exception as e:
        print("⚠️ Conversion error:", e)
        return input_path

def detect_emotion(audio_path):
    if audio_path.endswith(".webm"):
        audio_path = convert_to_wav(audio_path)

    signal, fs = torchaudio.load(audio_path)
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)
    print(f"🎧 Emotion detected: {text_lab}")
    return text_lab
