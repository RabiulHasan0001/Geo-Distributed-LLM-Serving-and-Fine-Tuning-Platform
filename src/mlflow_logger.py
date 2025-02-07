import mlflow

mlflow.set_experiment("llm_experiment")

with mlflow.start_run():
    mlflow.log_params({"epochs": 3, "batch_size": 2})
    mlflow.log_metric("loss", 0.23)
    mlflow.log_artifact("../fine_tuned_model")
