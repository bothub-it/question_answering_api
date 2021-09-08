import environ
from decouple import config

environ.Env.read_env(env_file=(environ.Path(__file__)-1)(".env"))

MODEL_BASE_PATH = config("MODEL_BASE_PATH", cast=str, default=".")
MODEL_NAME = config("MODEL_NAME", cast=str, default="QA")
MODEL_LANGUAGE = config("MODEL_LANGUAGE", cast=str, default="pt_br")
