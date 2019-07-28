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
  "apikey": "i2xzr3QtHkfny2iekPlN5T0-qONn4qkHYSUaUPU0tG0F",
  "iam_apikey_description": "Auto-generated for key c31f0652-8c5f-4380-88b5-3be09b78165e",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/c1c3c0533ace4b1eba3de3385814b16a::serviceid:ServiceId-794c42cb-ed67-4a2c-8027-7c6b31aa974f",
  "instance_id": "455fe1c1-4c6d-4ead-aa98-fee55eb73129",
  "password": "5db5cd15-199a-43af-99dc-357e3bae69d1",
  "url": "https://us-south.ml.cloud.ibm.com",
  "username": "c31f0652-8c5f-4380-88b5-3be09b78165e"
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
