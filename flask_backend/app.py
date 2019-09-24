import os
from flask import Flask, render_template, request
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
#from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.vgg19 import VGG19
from keras.models import Sequential, load_model
from PIL import Image
from watson_machine_learning_client import WatsonMachineLearningAPIClient
import numpy as np
from flask import jsonify

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model('./model/train_model.h5')

creds = {
  "apikey": ,
  "iam_apikey_description": 
  "iam_apikey_name": 
  "iam_role_crn": 
  "iam_serviceid_crn":
  "instance_id": 
  "password": 
  "url": 
  "username": 
}

client = WatsonMachineLearningAPIClient(creds)

scoring_url = 'https://us-south.ml.cloud.ibm.com/v3/wml_instances/455fe1c1-4c6d-4ead-aa98-fee55eb73129/deployments/ad0d5026-6e9d-4780-b6a1-72bad5222e24/online'
# scoring_payload = {'values': image.tolist()}
# predictions = client.deployments.score(scoring_url, scoring_payload)
# print(predictions)

model._make_predict_function()
print('model loaded')

@app.route('/')
def my_index():
    return '';

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Line 33 ======")
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    return jsonify(file.filename)


@app.route('/predict', methods=['GET'])
def get_file():

    usfileNameername = request.args.get('fileName')


    filepath = './uploads/' + usfileNameername

    img = Image.open(filepath)

    img = img.resize((64,64))
    img = np.array(img)
    img = img / 255.0
    img = img.reshape(1,64,64,3)
    # preds = model.predict(img)
    print('scoring URL')
    scoring_payload = {'values': img.tolist()}
    predictions = client.deployments.score(scoring_url, scoring_payload)
    print('Predictions', predictions)

    # print('Predicted: ', preds)

    result = []
    print (predictions["values"][0][0])
    if predictions["values"][0][0]>0.5:
        diag = "Malaria"
        confidence = predictions["values"][0][0]
    else:
        diag = "Not Malaria"
        confidence = predictions["values"][0][0]
    return jsonify({"diagnosis":diag,"confidence":str(confidence)})
    return predictions


if __name__ == "__main__":
    app.run()
