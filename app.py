# coding=utf8
import bothub_backend
import settings
from bothub_nlp_celery.app import celery_app
from bothub_nlp_celery.tasks import TASK_NLU_QUESTION_ANSWERING

model = celery_app.qa_model

backend = bothub_backend.get_backend(
    "bothub_backend.bothub.BothubBackend",
    settings.BOTHUB_ENGINE_URL
)


@celery_app.task(name=TASK_NLU_QUESTION_ANSWERING)
def ask_question(knowledge_base_id, question, language, authorization):

    request = backend.request_backend_knowledge_bases(authorization, knowledge_base_id, language)
    context = request.get("text")

    if len(context) == 0 or len(context) > 25000:
        return {"detail": f"Invalid context size({len(context)} characters)"}
    if context is None:
        return {"detail": "Something went wrong"}
    if request.get("language") != language:
        return {"detail": "Something went wrong"}

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
        ]
    }

    # TODO: save question+answer log
    # backend.save_question_answer(question + answer, base_id, language, authorization)

    answer_json = answer
    return answer_json
