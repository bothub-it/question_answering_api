# coding=utf8
from bothub_nlp_celery.app import celery_app
from bothub_nlp_celery.tasks import TASK_NLU_QUESTION_ANSWERING

import json

model = celery_app.qa_model


@celery_app.task(name=TASK_NLU_QUESTION_ANSWERING)
def ask_question(context, question):

    query = [
        {
            'context': context,
            'qas': [
                {'id': '0', 'question': question},
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
    print(json.dumps(answer_json, indent=2))
    return answer_json
