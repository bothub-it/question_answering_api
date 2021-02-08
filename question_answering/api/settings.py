import argparse
from decouple import config

PARSER = argparse.ArgumentParser()

PARSER.add_argument("--model", type=str, default=None)

ARGUMENTS, _ = PARSER.parse_known_args()

model = ARGUMENTS.MODEL

if model is None:
    model = config(
        "MODEL", cast=str, default="pt_br"
    )







