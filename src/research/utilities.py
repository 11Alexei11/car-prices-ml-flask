from typing import Any, Dict
import pickle as pkl
import os

import numpy as np
from sklearn.metrics import (
    mean_absolute_error as mae, mean_absolute_percentage_error as mape, explained_variance_score as evs,
    r2_score as r2
)

import pandas as pd


class StageNames:
    PREPROCESS = "preprocess"
    TRAIN = "train"
    EVALUATE = "evaluate"


class DvcStageParamsNames:
    OUTS = "outs"
    DEPS = "deps"
    CMD = "cmd"


def load_pkl(path) -> Any:
    with open(path, 'rb') as f:
        return pkl.load(f)


def load_csv(path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_data(path: str):
    path_without_ext, ext = os.path.splitext(path)
    if ext == '.csv':
        return load_csv(path)

    elif ext == '.pkl':
        return load_pkl(path)


def save_artifacts():
    pass

def compute_mean_waste(target: np.ndarray, predict: np.ndarray) -> float:
    diff = predict - target
    return diff[diff > 0].mean()

def compute_mean_stockout(target: np.ndarray, predict: np.ndarray) -> float:
    diff = predict - target
    return diff[diff < 0].mean()

def compute_metrics(predict: np.ndarray, target: np.ndarray) -> Dict[str, float]:
    metrics = {}
    for error_func_name, error_func in zip(
        ['mae', 'mape', 'evs', 'r2', 'mean_waste', 'mean_stockout'],
        [mae, mape, evs, r2, compute_mean_waste, compute_mean_stockout]
    ):
        metrics.update({error_func_name: error_func(target, predict)})

    return metrics