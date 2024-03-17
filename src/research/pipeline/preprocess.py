import yaml
import os
from typing import Dict, Tuple
import pickle as pkl
import hashlib

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

import sys
sys.path.append(os.getcwd())

from src.research.utilities import StageNames, DvcStageParamsNames
from src.utils.config import ConfigLoader


def transform_dataset_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df_cp = df.copy()
    for column in df_cp.columns:
        column_new = column.lower()
        df_cp[column_new] = df_cp.pop(column)

    return df_cp


def preprocess_strings(
        df: pd.DataFrame,
        is_train: bool = True,
        encoders: Dict[str, OneHotEncoder] = None
    ) -> Tuple[pd.DataFrame, Dict[str, OneHotEncoder]]:
    """Function to preprocess strings

    Args:
        df (pd.DataFrame): Source dataset

    Returns:
        pd.DataFrame: Dataset with preprocessed strings
    """
    df_cp = df.copy()

    if is_train:
        encoders = {}

    for column in df_cp.copy().select_dtypes("object"):
        if is_train:
            encoders[column] = OneHotEncoder()
            encoders[column].fit(df_cp[column].values.reshape(-1, 1))
        transformed_data = encoders[column].transform(df_cp[column].values.reshape(-1, 1))

        for i, class_ in enumerate(encoders[column].categories_[0]):
            df_cp[column+"_"+class_] = transformed_data[:, i].toarray().reshape(-1, )

        df_cp = df_cp.drop(column, axis=1)

    return df_cp, encoders


def preprocess_numericals(
        df: pd.DataFrame,
        is_train: bool = True,
        scalers: Dict[str, MinMaxScaler] = None
    ) -> Tuple[pd.DataFrame, Dict[str, MinMaxScaler]]:
    df_cp = df.copy()

    int_types = [np.int8, np.int16, np.int32, np.int64]
    float_types = [np.float16, np.float32, np.float64, np.float128]
    double_types = [np.double]
    if is_train:
        scalers = {}

    for column in df_cp.select_dtypes(int_types + float_types + double_types):
        if is_train:
            scaler = MinMaxScaler()
            df_cp[column] = scaler.fit_transform(df_cp[column].values.reshape(-1, 1)).flatten()
            scalers[column] = scaler
        else:
            scaler = scalers.get(column)
            if scaler is None:
                raise Exception("scalers can not be None to numerical columns on test")

            df_cp[column] = scaler.transform(df_cp[column].values.reshape(-1, 1)).flatten()

    return df_cp, scalers


def preprocess_stage():
    pipeline_config = ConfigLoader.load()['pipeline.config']
    dataset_config = pipeline_config["dataset"]

    dvc_config = yaml.safe_load(open("dvc.yaml", 'r'))['stages']
    dvc_preprocess_stage = dvc_config[StageNames.PREPROCESS]

    file_save_paths = {}
    save_outs_directory = None
    for path in dvc_preprocess_stage[DvcStageParamsNames.OUTS]:
        file_name = os.path.basename(path)
        file_save_paths[file_name] = path

        if save_outs_directory is None:
            save_outs_directory = os.path.dirname(path)

    train_test_source_path = dvc_preprocess_stage[DvcStageParamsNames.DEPS]
    test_source_path, train_source_path = train_test_source_path[0], train_test_source_path[1]

    train_data = pd.read_csv(train_source_path)
    test_data = pd.read_csv(test_source_path)

    train_data = transform_dataset_column_names(train_data)
    test_data = transform_dataset_column_names(test_data)

    target = test_data.pop(dataset_config["target_column"])

    train_data, scalers = preprocess_numericals(train_data)
    test_data, scalers = preprocess_numericals(test_data, is_train=False, scalers=scalers)

    train_data, encoders = preprocess_strings(train_data)
    test_data, encoders = preprocess_strings(test_data, is_train=False, encoders=encoders)
    test_data = pd.concat((test_data, target), axis=1)

    os.makedirs(save_outs_directory, exist_ok=True)
    for file_name, file_path in file_save_paths.items():
        if file_name.count("train"):
            train_data.to_csv(file_path, index=False)
        elif file_name.count("test"):
            test_data.to_csv(file_path, index=False)

        elif file_name.count("scalers"):
            with open(file_path, 'wb') as f:
                pkl.dump(scalers, f)

        elif file_name.count("encoders"):
            with open(file_path, 'wb') as f:
                pkl.dump(scalers, f)


if __name__ == "__main__":
    preprocess_stage()