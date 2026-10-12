from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from process_video import process_video

# Preload YOLO once (optional) - prevents first request delay
try:
    from detector import model  # noqa: F401
except Exception:
    pass

# Make sure backend/ local imports work when running from different cwd
import sys
sys.path.insert(0, os.path.dirname(__file__))


app = Flask(
    __name__,
    template_folder="..",  # templates are in project root
    static_folder=None,
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_FOLDER = os.path.join(PROJECT_ROOT, "css")
JS_FOLDER = os.path.join(PROJECT_ROOT, "js")
VIDEOS_FOLDER = os.path.join(PROJECT_ROOT, "videos")
IMAGES_FOLDER = os.path.join(PROJECT_ROOT, "images")

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(CSS_FOLDER, filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(JS_FOLDER, filename)

@app.route('/videos/<path:filename>')
def serve_videos(filename):
    return send_from_directory(VIDEOS_FOLDER, filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(IMAGES_FOLDER, filename)


CORS(app)

# Paths are relative to this file's working directory.
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# 🌐 HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload.html")
def upload_page():
    return render_template("upload.html")


@app.route("/processing.html")
def processing_page():
    return render_template("processing.html")


@app.route("/result.html")
def result_page():
    return render_template("result.html")



@app.route("/process", methods=["POST"])
def process_route():
    """API used by js/upload.js

    Expects multipart/form-data:
    - video: video file
    - reference: optional image file (not used in baseline)
    - command: text
    - blur: blur style
    """
    if "video" not in request.files:
        return jsonify({"success": False, "error": "No video uploaded"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"success": False, "error": "Empty video filename"}), 400

    command = request.form.get("command", "")
    blur_style = request.form.get("blur", "Gaussian Blur")

    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)

    # Read file back to ensure it was uploaded correctly
    try:
        saved_size = os.path.getsize(video_path)
    except OSError:
        saved_size = -1

    if saved_size <= 0:
        return jsonify({"success": False, "error": "Uploaded video saved but empty/invalid. Re-upload a working mp4 file."}), 400

    video_path = os.path.abspath(video_path)

    # Ensure absolute path is passed to OpenCV (prevents cwd/rel-path issues)
    video_path = os.path.abspath(video_path)

    # Debug helpful for upload failures
    try:
        saved_size = os.path.getsize(video_path)
    except OSError:
        saved_size = -1

    # Optional: save reference to disk (not used yet)

    if "reference" in request.files and request.files["reference"].filename:
        ref_file = request.files["reference"]
        ref_path = os.path.join(UPLOAD_FOLDER, ref_file.filename)
        ref_file.save(ref_path)

    try:
        output_filename = process_video(
            input_path=video_path,
            output_dir=OUTPUT_FOLDER,
            blur_style=blur_style,
        )
    except Exception as e:
        return jsonify({"success": False, "error": f"Processing failed: {e}"}), 500

    # Frontend expects data.video to be a URL path appended to base.
    return jsonify({
        "success": True,
        "video": f"/outputs/{output_filename}",
        "command": command,
        "blur": blur_style,
    })


# 📂 SERVE OUTPUT FILES
@app.route("/outputs/<filename>")
def get_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    import webbrowser
    import threading

    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")

    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)

