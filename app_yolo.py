from flask import Flask, render_template, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path setup
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    video = request.files.get("video")
    if not video:
        return "No video uploaded", 400
    
    # Save the uploaded video
    filename = secure_filename(video.filename)
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(video_path)

    # YOLOv5 detection
    output_dir = os.path.join(PROCESSED_FOLDER, filename.split('.')[0])
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run([
        "python", "yolov5/detect.py",
        "--source", video_path,
        "--weights", "yolov5s.pt",
        "--project", output_dir,
        "--name", "results"
    ])

    # Locate processed video or images
    processed_path = os.path.join(output_dir, "results")
    if os.path.exists(processed_path):
        return f"Detection complete. Check the processed results in {processed_path}", 200
    else:
        return "Detection failed. Please check logs.", 500

if __name__ == "__main__":
    app.run(debug=True)
