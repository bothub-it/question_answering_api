# coding=utf8
from utils import language_to_model
from bothub_nlp_celery.app import celery_app
from bothub_nlp_celery.tasks import TASK_NLU_QUESTION_ANSWERING

models = celery_app.qa_model


@celery_app.task(name=TASK_NLU_QUESTION_ANSWERING)
def ask_question(context, question, language):

    query = [
        {
            'context': context,
            'qas': [
                {'id': '0', 'question': question},
            ]
        }
    ]
    model = language_to_model.get(language, "multilang")
    answer = models.get(model).predict(query)
    probability, answer = answer[1][0], answer[0][0]
    formatted_answer = {
        "answers": [
            {
                "text": answer['answer'][i],
                "confidence": "{:.8f}".format(probability["probability"][i])
            } for i in range(len(answer['answer'])) if answer['answer'][i] and answer['answer'][i] != 'empty'
        ],
        "id": answer['id']
    }

    return formatted_answer
