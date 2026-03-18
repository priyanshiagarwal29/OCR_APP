from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""

    if request.method == 'POST':
        file = request.files['image']

        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

            # OCR
            text = pytesseract.image_to_string(Image.open(path))

            # Save text to file
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(text)

    return render_template('index.html', text=text)


@app.route('/download')
def download():
    return send_file("output.txt", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
