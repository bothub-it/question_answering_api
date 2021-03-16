model_info = {
    'pt_br': {
        'args': {
            "n_best_size": 3,
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
        },
        'type': 'bert',
        'bucket_path': 'bert_neuralmind_portuguese/model/checkpoint-14248-epoch-2',
        'dir': 'pt_br'
    },
    'en': {
        'args': {
            "n_best_size": 3,
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
        },
        'type': 'roberta',
        'bucket_path': '',
        'dir': 'en'
    },
    'multilang': {
        'args': {
            "n_best_size": 3,
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
        },
        'type': 'bert',
        'bucket_path': 'bert_bert-base-multilingual-cased_squad-2_batch_large/model/best_model',
        'dir': 'multilang'
    },
}

language_to_model = {
    'en': 'en',
    'pt_br': 'pt_br',
    'pt': 'pt_br',
}
