import subprocess
from bothub_nlp_celery.actions import queue_name
from bothub_nlp_celery import settings

subprocess.run(
    [
        "celery",
        "worker",
        "-O",
        "fair",
        "--workdir",
        ".",
        "-A",
        "app",
        "-l",
        "INFO",
        "-E",
        "-c",
        "1",
        "--pool",
        "solo",
        "-Q",
        queue_name(
            settings.BOTHUB_NLP_LANGUAGE_QUEUE,
            model_name=settings.BOTHUB_LANGUAGE_MODEL,
        ),
    ]
)
