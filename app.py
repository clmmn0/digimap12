from flask import Flask, flash, render_template, request, template_rendered, redirect, url_for
import os
import shutil
import argparse
import model
import tensorflow.compat.v1 as tf
import urllib.request
from werkzeug.utils import secure_filename


tf.compat.v1.disable_v2_behavior()
FLAGS = tf.app.flags.FLAGS

image_folder = os.path.join('static', 'images')

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = image_folder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_contents(image_folder):
    folder = "./static/images/" + image_folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route('/', methods=['GET'])
def show_index():
    delete_contents("input_images")
    delete_contents("input_images_res")
    args = parse_args()

    # set gpu id or leave it blank for cpu
    if args.gpu == 'cpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    # choose the model trained on default data or all data
    if args.model == 'default':
        model_path = os.path.join('checkpoints', 'default')
    else:
        model_path = os.path.join('checkpoints', 'alldata')

    global deblur
    deblur = model.DEBLUR(args)
    deblur.build(model_path)

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
        input_path = "./static/images/input_images/" + filename
        deblur.test()
        output_path = "./static/images/input_images_res/" + filename
        return render_template('deblur.html', sample_input=sample_input, sample_output=sample_output, input_image=input_path, output_image=output_path)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


def parse_args():
    parser = argparse.ArgumentParser(description='deblur arguments')
    parser.add_argument('--gpu', type=str, default='0', 
                        help='set gpu id or leave it blank for cpu')
    parser.add_argument('--model', type=str, default='default', 
                        help='choose the model trained on default data or all data')
    parser.add_argument('--input_path', type=str, default='./static/images/input_images',
                        help='path of testing folder or path of one testing image')
    parser.add_argument('--max_height', type=int, default=720,
                        help='max height for the input tensor, should be multiples of 16')
    parser.add_argument('--max_width', type=int, default=1280,
                        help='max width for the input tensor, should be multiples of 16')
    args = parser.parse_args()
    return args


def main(_):
    pass


if __name__ == '__main__':
    app.run(port=3000, debug=True)


import os, shutil
folder = '/path/to/folder'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))