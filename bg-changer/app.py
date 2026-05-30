from flask import Flask, render_template, request, send_file
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    color = request.form['color']

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "result.png")

    file.save(input_path)

    img = Image.open(input_path)

    removed = remove(img)

    bg = Image.new("RGBA", removed.size, color)
    final = Image.alpha_composite(bg, removed)

    final.save(output_path)

    return render_template("index.html", image="result.png")

@app.route('/download')
def download():
    return send_file("output/result.png", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)