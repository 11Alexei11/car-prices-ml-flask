import yaml
import os
import pickle as pkl
import json
import sys
sys.path.append(os.getcwd())

import pandas as pd
from dvclive import Live

from src.utils.config import ConfigLoader
from src.research.utilities import StageNames, DvcStageParamsNames
from src.research.utilities import compute_metrics


def evaluate():
    dvc_config = yaml.safe_load(open("dvc.yaml"))
    dvc_evaluate_config = dvc_config['stages'][StageNames.EVALUATE]

    dataset_config = ConfigLoader.load()['pipeline.config']['dataset']

    for file_path in dvc_evaluate_config[DvcStageParamsNames.DEPS]:
        file_name_with_ext = os.path.basename(file_path)
        file_name, ext = os.path.splitext(file_name_with_ext)

        if ext == '.pkl':
            if file_name.count("scaler"):
                with open(file_path, 'rb') as f:
                    scalers = pkl.load(f)
            else:
                with open(file_path, 'rb') as f:
                    model = pkl.load(f)

        elif ext == '.csv':
            test_data = pd.read_csv(file_path)
            target_descaled = test_data.pop(dataset_config['target_column']).values.reshape(-1, 1)

    predictions_descaled = scalers[dataset_config['target_column']].inverse_transform(model.predict(test_data).reshape(-1, 1))
    metrics = compute_metrics(predict=predictions_descaled, target=target_descaled)

    save_folder = os.path.dirname(dvc_evaluate_config[DvcStageParamsNames.OUTS][0])
    os.makedirs(save_folder, exist_ok=True)
    with Live(dir=save_folder, save_dvc_exp=True) as live:
        for metric_name, metric_value in metrics.items():
            live.log_metric(name=metric_name, val=metric_value)

        with open(dvc_evaluate_config[DvcStageParamsNames.OUTS][0], 'w') as f:
            json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    evaluate()
