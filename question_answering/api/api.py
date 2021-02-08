# coding=utf8
from simpletransformers.question_answering import QuestionAnsweringModel
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from . import settings
from .utils import get_model_info
from .download_model import download_model
import json
import time
import os
import plac


app = Flask(__name__)
model = None
CORS(app)


@app.route('/ask_question', methods=['POST'])
def ask_paper():
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
        answer_json = {'answer': answer[0]}
        response = jsonify(answer_json)
        return response


def setup_model():
    global model
    st = time.time()
    if os.path.isdir('new_folder'):
        print('You dont have the model, downloading model...')
        plac.call(download_model, settings.model)
    print("Loading model...")
    model_type, model_dir, train_args = get_model_info()
    model = QuestionAnsweringModel(model_type, model_dir, args=train_args, use_cuda=True)
    print('loaded in: ', time.time() - st)


def main():
    setup_model()
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
