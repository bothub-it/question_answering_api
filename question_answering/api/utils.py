import settings


def get_model_info():
    if settings.model == 'pt_br':
        train_args = {
            "num_train_epochs": 2,
            "max_seq_lenght": 384,
            "train_batch_size": 16,
            "gradient_accumulation_steps": 1,
            "eval_batch_size": 16,
            "save_steps": -1,
            "save_model_every_epoch": True,
            "evaluate_during_training_steps": -1,
            "evaluate_during_training": True,
            "evaluate_during_training_verbose": True,
            "use_cached_eval_features": True
        }
        model_dir = 'checkpoint-7124-epoch-1'
        model_type = 'bert'
    elif settings.model == 'bert_multi':
        train_args = {
            "num_train_epochs": 2,
            "max_seq_lenght": 384,
            "train_batch_size": 16,
            "gradient_accumulation_steps": 1,
            "eval_batch_size": 16,
            "save_steps": -1,
            "save_model_every_epoch": True,
            "evaluate_during_training_steps": -1,
            "evaluate_during_training": True,
            "evaluate_during_training_verbose": True,
            "use_cached_eval_features": True
        }
        model_dir = 'bert_bert-base-multilingual-cased_squad-2_batch_large/best_model'
        model_type = 'bert'
    elif settings.model == 'bert_multi2':
        train_args = {
            "num_train_epochs": 2,
            "max_seq_lenght": 384,
            "train_batch_size": 16,
            "gradient_accumulation_steps": 1,
            "eval_batch_size": 16,
            "save_steps": -1,
            "save_model_every_epoch": True,
            "evaluate_during_training_steps": -1,
            "evaluate_during_training": True,
            "evaluate_during_training_verbose": True,
            "use_cached_eval_features": True
        }
        model_dir = 'bert_bert-base-multilingual-cased_train_tydiqa-train-formatted_batch_large/best_model'
        model_type = 'bert'

    return model_type, model_dir, train_args

