import argparse
import environ
from decouple import config

PARSER = argparse.ArgumentParser()

PARSER.add_argument("--model", type=str, default=None)

ARGUMENTS, _ = PARSER.parse_known_args()

model = ARGUMENTS.model

if model is None:
    model = config(
        "MODEL", cast=str, default="pt_br"
    )

environ.Env.read_env(env_file=(environ.Path(__file__)-1)(".env"))

env = environ.Env(
    # set casting, default value

    # ENVIRONMENT=(str, "production"),
    # BOTHUB_NLP_API_HOST=(str, "0.0.0.0"),
    # BOTHUB_NLP_API_PORT=(int, 2657),
    # BOTHUB_NLP_API_WEB_CONCURRENCY=(int, None),
    # BOTHUB_NLP_API_WORKERS_PER_CORE=(float, 3),
    # BOTHUB_NLP_API_LOG_LEVEL=(str, "info"),
    # BOTHUB_NLP_API_KEEPALIVE=(int, 120),
    BOTHUB_GOOGLE_PROJECT_ID=(str, None),
    BOTHUB_GOOGLE_CREDENTIALS_REFRESH_TOKEN=(str, None),
    BOTHUB_GOOGLE_CREDENTIALS_TOKEN_URI=(str, None),
    BOTHUB_GOOGLE_CREDENTIALS_CLIENT_ID=(str, None),
    BOTHUB_GOOGLE_CREDENTIALS_CLIENT_SECRET=(str, None),
)

# ENVIRONMENT = env.str("ENVIRONMENT")
# BOTHUB_NLP_API_HOST = env.str("BOTHUB_NLP_API_HOST")
# BOTHUB_NLP_API_PORT = env.int("BOTHUB_NLP_API_PORT")
# BOTHUB_NLP_API_WEB_CONCURRENCY = env.int("BOTHUB_NLP_API_WEB_CONCURRENCY")
# BOTHUB_NLP_API_WORKERS_PER_CORE = env.float("BOTHUB_NLP_API_WORKERS_PER_CORE")
# BOTHUB_NLP_API_LOG_LEVEL = env.str("BOTHUB_NLP_API_LOG_LEVEL")
# BOTHUB_NLP_API_KEEPALIVE = env.int("BOTHUB_NLP_API_KEEPALIVE")

# Google Credentials Ai Platform
BOTHUB_GOOGLE_PROJECT_ID = env.str("BOTHUB_GOOGLE_PROJECT_ID")
BOTHUB_GOOGLE_CREDENTIALS_REFRESH_TOKEN = env.str(
    "BOTHUB_GOOGLE_CREDENTIALS_REFRESH_TOKEN"
)
BOTHUB_GOOGLE_CREDENTIALS_TOKEN_URI = env.str("BOTHUB_GOOGLE_CREDENTIALS_TOKEN_URI")
BOTHUB_GOOGLE_CREDENTIALS_CLIENT_ID = env.str("BOTHUB_GOOGLE_CREDENTIALS_CLIENT_ID")
BOTHUB_GOOGLE_CREDENTIALS_CLIENT_SECRET = env.str(
    "BOTHUB_GOOGLE_CREDENTIALS_CLIENT_SECRET"
)
