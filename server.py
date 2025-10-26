# from flask import Flask, request, send_file, jsonify
# from TTS.api import TTS
# import tempfile, os

# app = Flask(__name__)

# # Initialize TTS once (LJSpeech Tacotron2 + HiFi-GAN)
# tts = TTS(
#     model_name="tts_models/en/ljspeech/tacotron2-DDC",
#     progress_bar=False,
#     gpu=False
# )

# @app.route("/api/tts", methods=["GET"])
# def generate_tts():
#     text = request.args.get("text", "")
#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     try:
#         # Create a temporary file for the generated audio
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
#             tts.tts_to_file(text=text, file_path=tmp.name)
#             return send_file(tmp.name, mimetype="audio/wav")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     # Port 5002 is typical for Render services
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))

from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import tempfile, os

app = Flask(__name__)

tts = TTS(
    model_name="tts_models/en/vctk/vits",
    progress_bar=False,
    gpu=False
)
print(tts.speakers)

@app.route("/api/tts", methods=["GET"])
def generate_tts():
    text = request.args.get("text", "")
    speaker = request.args.get("speaker", "p225")  # default male speaker
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tts.tts_to_file(text=text, file_path=tmp.name, speaker=speaker)
            return send_file(tmp.name, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))


