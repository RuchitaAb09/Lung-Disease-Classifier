from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


# Define a flask app
app = Flask(__name__)

model=load_model("Lung disease classifier.h5")


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(244, 244))

    # Preprocessing the image
    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)



    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=""
        val=np.argmax(preds,axis=1)
        if val==0:
            result=" Covid"
        elif val==1:
            result=" Healthy"
        elif val==2:
            result=" Pneumonia"

        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

