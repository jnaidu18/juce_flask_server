# server.py or app.py

from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------- Add your upload route here ---------
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_data()
    if data:
        with open(os.path.join(UPLOAD_FOLDER, "latest.wav"), 'wb') as f:
            f.write(data)
        print("✅ Received raw upload, saved as latest.wav")
        return "File uploaded", 200
    return "No data received", 400
# ---------------------------------------------

@app.route('/latest')
def serve_latest():
    file_path = os.path.join(UPLOAD_FOLDER, "latest.wav")
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, "latest.wav")
    return "No file yet", 404

@app.route('/')
def index():
    return """
    <html>
      <head><title>JUCE Audio Stream</title></head>
      <body style='background:#111;color:#fff;text-align:center;font-family:sans-serif;'>
        <h2>JUCE Recorded Audio</h2>
        <audio id="player" controls autoplay></audio>
        <script>
          const player = document.getElementById('player');
          async function refreshAudio() {
            player.src = '/latest?cache=' + Date.now();
            player.play().catch(()=>{});
          }
          setInterval(refreshAudio, 5000);
          refreshAudio();
        </script>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
