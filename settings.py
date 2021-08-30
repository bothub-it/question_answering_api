import environ

environ.Env.read_env(env_file=(environ.Path(__file__)-1)(".env"))

env = environ.Env(
    # set casting, default value
    BOTHUB_ENGINE_URL=(str, "https://api.bothub.it"),
    MAX_SEQ_LENGTH=(int, 384),
    LISTENING_QUEUES=(str, "pt_br-QA,en-QA,multilang-QA"),
)

BOTHUB_ENGINE_URL = env.str("BOTHUB_ENGINE_URL")
MAX_SEQ_LENGTH = env.int("MAX_SEQ_LENGTH")
LISTENING_QUEUES = env.str("LISTENING_QUEUES")
