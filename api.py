# coding=utf8
import json
import time
import os

import settings
from download_model import download_model
from utils import model_info
from app import create_app
from app.models import AccessLog

from simpletransformers.question_answering import QuestionAnsweringModel
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


app = create_app()


@app.route("/access-logs", methods=["GET"])
def access_logs():
    return jsonify(AccessLog.list_all())


@app.route("/ask", methods=["POST"])
def ask_question():
    if request.method == "POST":
        json_string = request.get_json()
        data_dump = json.dumps(json_string)
        data = json.loads(data_dump)
        query = [
            {
                "context": data.get("context", ""),
                "qas": [{"id": "0", "question": data.get("question", "")},],
            }
        ]

        answer = model.predict(query)

        probability, answer = answer[1][0], answer[0][0]
        answer = {
            "answers": [
                {
                    "text": answer["answer"][i],
                    "confidence": probability["probability"][i],
                }
                for i in range(len(answer["answer"]))
            ],
            "id": answer["id"],
        }

        answer_json = answer

        response = jsonify(answer_json)

        access_log = AccessLog(request_body=data, response_body=response)
        access_log.save_to_db()

        return response


def setup_model():
    global model
    st = time.time()
    if not os.path.isdir(settings.model):
        print("You dont have the model, downloading model...")
        download_model(settings.model)
    print("Loading model...")
    model_dict = model_info.get(settings.model)
    try:
        model = QuestionAnsweringModel(
            model_dict.get("type"),
            settings.model,
            args=model_dict.get("args"),
            use_cuda=True,
        )
    except ValueError as err:
        print(err)
        model = QuestionAnsweringModel(
            model_dict.get("type"),
            settings.model,
            args=model_dict.get("args"),
            use_cuda=False,
        )

    print("loaded in: ", time.time() - st)


def main():
    setup_model()
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
