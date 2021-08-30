import subprocess
from bothub_nlp_celery import settings

QUEUES = ",".join([model + "-QA" for model in settings.AVAILABLE_QA_MODELS])

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
        QUEUES,
    ]
)
