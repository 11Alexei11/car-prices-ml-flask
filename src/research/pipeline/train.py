import yaml
import os
import pickle as pkl

import sys
sys.path.append(os.getcwd())

from src.utils.config import ConfigLoader
from src.research.utilities import DvcStageParamsNames
from src.research.utilities import StageNames
from src.research.utilities import load_data


def train():
    dvc_train_config = yaml.safe_load(open("dvc.yaml", 'r'))
    dataset_config = ConfigLoader.load()['pipeline.config']["dataset"]

    dataset = {}
    for file in dvc_train_config['stages'][StageNames.TRAIN][DvcStageParamsNames.DEPS]:
        file_name_path, ext = os.path.splitext(file)
        file_name = os.path.basename(file_name_path)

        if not file_name.count('train') or ext != ".csv":
            continue

        dataset['train'] = {
            'x': load_data(file)
        }
        dataset['train']['y'] = dataset['train']['x'].pop(dataset_config['target_column'])

    # hashlib.sha256()
    model = ...
    model.fit(dataset['train']['x'], dataset['train']['y'])

    model_save_path = dvc_train_config['stages'][StageNames.TRAIN][DvcStageParamsNames.OUTS][0]
    model_directory = os.path.dirname(model_save_path)

    os.makedirs(model_directory, exist_ok=True)
    with open(model_save_path, 'wb') as f:
        pkl.dump(model, f)


if __name__ == "__main__":
    train()
