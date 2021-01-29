import os
import posixpath
import json
from googleapiclient import discovery
from googleapiclient import errors
from utils import connect_to_storage, get_job_id
from datetime import datetime


def split_train_test(train_file_name, eval_percentage=0.15, format_data=True):
    with open(posixpath.join('data', train_file_name), 'r') as f:
        data = json.load(f)

    if format_data:
        data = [item for topic in data['data'] for item in topic['paragraphs']]
    test_size = int(eval_percentage * len(data))
    eval_data = data[:test_size]
    train_data = data[test_size:]

    train_split_file_name = posixpath.join('data', 'train_{}_{}_split.json'.format(train_file_name, eval_percentage))
    with open(train_split_file_name, 'w') as f:
        json.dump(train_data, f, indent=2)
    eval_split_file_name = posixpath.join('data', 'eval_{}_{}_split.json'.format(train_file_name, eval_percentage))
    with open(eval_split_file_name, 'w') as f:
        json.dump(eval_data, f, indent=2)

    return train_split_file_name, eval_split_file_name


def send_job_train_ai_platform(train_data, model_type, model_name, config_data=None, eval_data=None, eval_percentage=0.15, format_data=True):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bothub-273521-b2134fc6b1df.json"
    package_uris = ["gs://question_answering/question_answering-1.0.0.tar.gz"]

    job_id = get_job_id(train_data, model_type, model_name, config_data)
    print(job_id)
    train_path = posixpath.join('data', train_data)
    if eval_data is not None:
        eval_path = posixpath.join('data', eval_data)
    if config_data is not None:
        config_path = posixpath.join('configs', config_data)

    bucket = connect_to_storage('question_answering')

    if not bucket.blob(posixpath.join(job_id, 'train_data.json')).exists():
        if eval_data is None:
            train_path, eval_path = split_train_test(train_path, eval_percentage, format_data)
            bucket.blob(posixpath.join(job_id, 'train_data.json')).upload_from_filename(train_path)
            bucket.blob(posixpath.join(job_id, 'eval_data.json')).upload_from_filename(eval_path)
        else:
            bucket.blob(posixpath.join(job_id, 'train_data.json')).upload_from_filename(train_path)
            bucket.blob(posixpath.join(job_id, 'eval_data.json')).upload_from_filename(eval_path)
        if config_data:
            bucket.blob(posixpath.join(job_id, 'config.json')).upload_from_filename(config_path)
    else:
        print('a folder with {} already exist in the storage so the the data is not going to be uploaded'.format(job_id))

    training_inputs = {
        "scaleTier": "CUSTOM",
        "masterType": "standard_p100",
        "package_uris": package_uris,
        "pythonModule": "question_answering.train",
        "args": [
            '--job-id',
            job_id,
            '--model-type',
            model_type,
            '--model-name',
            model_name
        ],
        "region": "us-east1",
        "jobDir": "gs://question_answering",
        "runtimeVersion": "2.2",
        "pythonVersion": "3.7",

    }
    job_spec = {"jobId": job_id.replace('-', '_').replace('/', '_') + datetime.now().strftime("_%d_%m_%Y_%H_%M"), "trainingInput": training_inputs}
    project_id = "projects/bothub-273521"
    cloudml = discovery.build("ml", "v1")
    request = cloudml.projects().jobs().create(body=job_spec, parent=project_id)

    try:
        request.execute()
    except errors.HttpError as err:
        raise Exception(err)
    print(f'{job_id} benchmark job sent')


if __name__ == '__main__':
    train_data = 'train_data_pt.json'
    model_type = 'bert'
    model_name = 'xlm-roberta-base'
    config_data = 'batch_large.json'
    # split_train_test('tydiqa-train-formatted.json', format_data=False)
    # send_job_train_ai_platform(train_data, model_type, model_name, config_data=config_data)

    # xlm + multilang dataset
    send_job_train_ai_platform(train_data='train_tydiqa-train-formatted.json_0.15_split.json',
                               model_type='xlmroberta',
                               model_name='xlm-roberta-large',
                               config_data='batch_large.json',
                               eval_data='eval_tydiqa-train-formatted.json_0.15_split.json')

    # bert_multilang + multilang dataset
    # send_job_train_ai_platform(train_data='train_tydiqa-train-formatted.json_0.15_split.json',
    #                            model_type='bert',
    #                            model_name='bert-base-multilingual-cased',
    #                            config_data='batch_large.json',
    #                            eval_data='eval_tydiqa-train-formatted.json_0.15_split.json')
    #
    # # bert_multilang + english_dataset
    # send_job_train_ai_platform(train_data='squad-2.0-train-formatted.json',
    #                            model_type='bert',
    #                            model_name='bert-base-multilingual-cased',
    #                            config_data='batch_large.json',
    #                            eval_data='eval_tydiqa-train-formatted.json_0.15_split.json')
