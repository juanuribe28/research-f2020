local embedding_dim = 64;

{
    dataset_reader: {
        type: 'tsv-reader',
        token_indexers: {
            tokens: {
                type: 'single_id',
            },
        },
        tokenizer: {
            type: 'whitespace',
        },
    },
    model: {
        type: 'simple_classifier',
        embedder: {
            token_embedders: {
                tokens: {
                    type: 'embedding',
                    embedding_dim: embedding_dim,
                },
            },
        },
        encoder: {
            type: 'boe',  # WINNER
            embedding_dim: embedding_dim,
        },
    },
    train_data_path: './data/train_data.tsv',
    validation_data_path: './data/test_data.tsv',
    trainer: {
        cuda_device: -1,
        num_epochs: 100,
        optimizer: {
            type: 'adamax',  # WINNER
        },
        patience: 10,
    },
    data_loader: {
        batch_size: 32,
        shuffle: false,
        sampler: 'random',
    },
}
