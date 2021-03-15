import environ

environ.Env.read_env(env_file=(environ.Path(__file__)-1)(".env"))

env = environ.Env(
    # set casting, default value
    BOTHUB_ENGINE_URL=(str, "https://api.bothub.it")
)

BOTHUB_ENGINE_URL = env.str("BOTHUB_ENGINE_URL")
