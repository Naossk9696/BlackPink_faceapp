import os
import base64
import numpy as np
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.preprocessing import image


classes = ['Jennie', 'Jisoo', 'Lisa', 'Rose']
image_size = 150

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


model =  load_model('./model.h5',compile=False)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            print(filepath)

            img = image.load_img(filepath, target_size=(image_size, image_size))
            img = image.img_to_array(img)
            data = np.array([img])

            result = model.predict(data)[0]
            predicted = result.argmax()

            pred_answer = 'This member is  ' + classes[predicted] + '.'

            #with open(filepath, 'rb') as f:
            #   img_base64 = base64.b64encode(f.read())

            #return render_template('index.html', answer=pred_answer, img=img_base64)
        return render_template('index.html',answer=pred_answer,imagefile=filepath)

    return render_template('index.html',answer='', img='')
    #return render_template('index.html',answer='')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)
