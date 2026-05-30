from flask import Flask, render_template, request, send_file
from PIL import Image
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
        return render_template("index.html", error="Please upload an image")

    file = request.files["image"]

    if file.filename == "":
        return render_template("index.html", error="Please select an image")

    color = request.form.get("color", "white")

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(STATIC_FOLDER, "result.png")

    file.save(input_path)

    try:
        img = Image.open(input_path).convert("RGBA")

        background = Image.new("RGBA", img.size, color)
        background.paste(img, (0, 0), img)

        background.save(output_path)

        return render_template(
            "index.html",
            image="result.png",
            success="Image processed successfully!"
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error: {str(e)}"
        )

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
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
