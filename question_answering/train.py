import json
import argparse
import posixpath
import os
import subprocess
from question_answering.utils import upload_folder_to_bucket, connect_to_storage, download_folder_structure_from_bucket


def train():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--job-id',
        help='Training file name')
    parser.add_argument(
        '--model-type',
        default='bert',
        help='Type of model, eg: BERT, XLM, ROBERTA')
    parser.add_argument(
        '--model-name',
        default='bert-base-cased',
        help='If true will not use cross validation')

    arguments, _ = parser.parse_known_args()

    bucket = connect_to_storage('question_answering')
    download_folder_structure_from_bucket(bucket, arguments.job_id, arguments.job_id)

    with open(posixpath.join(arguments.job_id, 'train_data.json'), 'r') as f:
        train_data = json.load(f)

    with open(posixpath.join(arguments.job_id, 'eval_data.json'), 'r') as f:
        eval_data = json.load(f)

    if os.path.isfile(posixpath.join(arguments.job_id, 'config.json')):
        with open(posixpath.join(arguments.job_id, 'config.json'), 'r') as f:
            args = json.load(f)
    else:
        args = None

    output_dir = posixpath.join(arguments.job_id, 'model')
    os.makedirs(output_dir, exist_ok=True)

    from simpletransformers.question_answering import QuestionAnsweringModel

    model = QuestionAnsweringModel(arguments.model_type, arguments.model_name, args=args, use_cuda=True)
    model.train_model(train_data, eval_data=eval_data)

    upload_folder_to_bucket(bucket, 'outputs', output_dir, recursive_upload=True)
    upload_folder_to_bucket(bucket, 'runs', output_dir, recursive_upload=True)


if __name__ == '__main__':
    subprocess.run(["pip", "install", "torch==1.7.1+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"])
    train()
