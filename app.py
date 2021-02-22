from flask import Flask, request, jsonify
import pickle
from model_files.ML_model import predict_mpg
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    vehicle = request.get_json()
    print(vehicle)
    # open model
    with open('./model_files/model.bin', 'rb') as fin:
        model = pickle.load(fin)
        fin.close()

    predictions = predict_mpg(vehicle, model)
    print(predictions)
    result = {
       'mpg_prediction': list(predictions)
    }
    return jsonify(result)



