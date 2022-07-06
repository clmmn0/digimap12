from flask import Flask, flash, render_template, request, template_rendered, redirect, url_for
import os
import urllib.request
from werkzeug.utils import secure_filename
import run_model
import argparse
import tensorflow.compat.v1 as tf
import model


image_folder = os.path.join('static', 'images')

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = image_folder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def show_index():
    sample_input = os.path.join(app.config['UPLOAD_FOLDER'], 'sampleinput.png')
    sample_output = os.path.join(app.config['UPLOAD_FOLDER'], 'sampleoutput.png')
    return render_template("index.html", sample_input=sample_input, sample_output=sample_output)

@app.route('/', methods=['POST'])
def upload_image():
    sample_input = os.path.join(app.config['UPLOAD_FOLDER'], 'sampleinput.png')
    sample_output = os.path.join(app.config['UPLOAD_FOLDER'], 'sampleoutput.png')

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = "./static/images/input_images/" + filename
        file.save(image_path)
        flash('Image successfully uploaded')
        exec(open('run_model.py').read())
        return render_template('index.html', sample_input=sample_input, sample_output=sample_output, filename=filename)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    flash('IMAGE IS DISPLAYED')
    return redirect(url_for('static', filename='images/' + filename), code=301)


if __name__ == '__main__':
    app.run(port=3000, debug=True)