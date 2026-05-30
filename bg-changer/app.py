from flask import Flask, render_template, request, send_file
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():

    if "image" not in request.files:
        return "No image uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No file selected"

    color = request.form.get("color", "white")

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(STATIC_FOLDER, "result.png")

    file.save(input_path)

    try:
        img = Image.open(input_path).convert("RGBA")

        removed = remove(img)

        bg = Image.new("RGBA", removed.size, color)

        final = Image.alpha_composite(bg, removed)

        final.save(output_path)

        return render_template(
            "index.html",
            image="result.png"
        )

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/download")
def download():

    file_path = os.path.join(STATIC_FOLDER, "result.png")

    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name="background_changed.png"
        )

    return "No image available"

@app.route("/health")
def health():
    return "Website Working Successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
