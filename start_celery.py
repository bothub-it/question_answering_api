import subprocess
from bothub_nlp_celery.actions import queue_name
from bothub_nlp_celery import settings

subprocess.run(
    [
        "celery",
        "-A",
        "app",
        "worker",
        "-O",
        "fair",
        "-c",
        "1",
        "-l",
        "INFO",
        "-E",
        "--pool",
        "solo",
        "-Q",
        'QA',
    ]
)
