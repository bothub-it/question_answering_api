# coding=utf8
from simpletransformers.question_answering import QuestionAnsweringModel
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import model_info
from download_model import download_models
import json
import time
import os
import settings


app = Flask(__name__)
model = None
CORS(app)


@app.route('/ask', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        json_string = request.get_json()
        data_dump = json.dumps(json_string)
        data = json.loads(data_dump)
        query = [
            {
                'context': data.get('context', ''),
                'qas': [
                    {'id': '0', 'question': data.get('question', '')},
                ]
            }
        ]

        answer = model.predict(query)

        probability, answer = answer[1][0], answer[0][0]
        answer = {
            "answers": [
                {
                    "text": answer['answer'][i],
                    "confidence": probability["probability"][i]
                } for i in range(len(answer['answer']))
            ],
            "id": answer['id']
        }

        answer_json = answer
        response = jsonify(answer_json)
        return response


def setup_model():
    global model
    st = time.time()
    model_path = os.path.join(settings.MODEL_BASE_PATH, settings.MODEL_NAME, settings.MODEL_LANGUAGE)
    while not os.path.isdir(model_path):
        print('You dont have the model...')
        model_url = input("Insert model url")
        download_models(model_url)

    print(f"Loading {settings.MODEL_LANGUAGE} model...")
    model_dict = model_info.get(settings.MODEL_LANGUAGE)
    try:
        model = QuestionAnsweringModel(
            model_dict.get('type'), model_path, args=model_dict.get('args'), use_cuda=True
        )
    except ValueError as err:
        print(err)
        model = QuestionAnsweringModel(
            model_dict.get('type'), model_path, args=model_dict.get('args'), use_cuda=False
        )

    print('loaded in: ', time.time() - st)


def main():
    setup_model()
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
