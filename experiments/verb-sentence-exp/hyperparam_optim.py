import optuna

def objective(trial: optuna.Trial) -> float:
    trial.suggest_int('s_embedding_dim', 16, 512)
    trial.suggest_int('v_embedding_dim', 16, 512)
    trial.suggest_float('s_dropout', 0.0, 0.9)
    trial.suggest_float('v_dropout', 0.0, 0.9)
    trial.suggest_float('lr', 5e-3, 5e-1, log=True)
    
    executor = optuna.integration.allennlp.AllenNLPExecutor(
        trial=trial,
        config_file="./training_config/config.jsonnet",  # path to jsonnet
        serialization_dir=f"./results/optuna-test/{trial.number}",
        metrics="best_validation_accuracy"
    )
    return executor.run()

if __name__ == '__main__':
    study = optuna.create_study(
        storage="sqlite:///results/test.db",  # save results in DB
        sampler=optuna.samplers.TPESampler(seed=24),
        study_name="optuna_allennlp",
        direction="maximize",
        pruner=optuna.pruners.HyperbandPruner()
    )

    timeout = 60 * 60 * 10  # timeout (sec): 60*60*10 sec => 10 hours
    study.optimize(
        objective,
        n_jobs=1,  # number of processes in parallel execution
        n_trials=100,  # number of trials to train a model
        timeout=timeout,  # threshold for executing time (sec)
    )

