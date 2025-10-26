from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import tempfile, os

app = Flask(__name__)

# Initialize TTS model once
tts = TTS(
    model_name="tts_models/en/vctk/vits",
    progress_bar=False,
    gpu=False
)

print("Available speakers:", tts.speakers)

@app.route("/api/tts", methods=["GET"])
def generate_tts():
    text = request.args.get("text", "")
    speaker = request.args.get("speaker", "p225")  # default speaker
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tts.tts_to_file(text=text, file_path=tmp.name, speaker=speaker)
            tmp_path = tmp.name

        # Send file and then delete
        response = send_file(tmp_path, mimetype="audio/wav")
        os.unlink(tmp_path)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
