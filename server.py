from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import tempfile, os

app = Flask(__name__)

# Load TTS model once at startup (English Tacotron2-DDC + HiFi-GAN v2)
tts = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    vocoder_name="vocoder_models/en/ljspeech/hifigan_v2",
    progress_bar=True,
    gpu=False  # Set to False if not using GPU
)

@app.route("/api/tts", methods=["GET"])
def generate_tts():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Create a temporary file for the generated audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tts.tts_to_file(text=text, file_path=tmp.name)
            return send_file(tmp.name, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Port 5002 is typical for Render services
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))
