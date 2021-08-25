import settings

config_args = {
    "n_best_size": 3,
    "num_train_epochs": 2,
    "max_seq_length": settings.MAX_SEQ_LENGTH,
    "doc_stride": int(settings.MAX_SEQ_LENGTH*0.8),
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

model_info = {
    'pt_br': {
        'args': config_args,
        'type': 'bert',
        'dir': 'pt_br'
    },
    'en': {
        'args': config_args,
        'type': 'roberta',
        'dir': 'en'
    },
    'multilang': {
        'args': config_args,
        'type': 'bert',
        'dir': 'multilang'
    },
}

language_to_model = {
    'en': 'en',
    'pt_br': 'pt_br',
    'pt': 'pt_br',
}
