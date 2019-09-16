import io
import logging
import os
from typing import Dict, Union, List, Iterable

import featuretools as ft
import numpy as np
import pandas as pd
from boto3 import resource
from botocore.client import Config
from featuretools.feature_base.feature_base import DirectFeature, TransformFeature

import ana

logger = logging.getLogger(__name__)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 50)


class Transform:
    def __init__(self):
        logger.info("Initializing...")
        experiment_id = os.getenv("EXPERIMENT_ID")
        bucket = os.getenv("BUCKET")
        self.target = os.getenv("TARGET")
        self.date = os.getenv("DATE")
        self.date_format = os.getenv("DATE_FORMAT")
        self.group = os.getenv("GROUP")
        s3 = resource("s3",
                      endpoint_url="http://minio-service.kubeflow:9000",
                      aws_access_key_id="minio",
                      aws_secret_access_key="minio123",
                      config=Config(signature_version="s3v4"),
                      region_name="us-east-1")

        # Reads CSV used for feature creation
        logger.info("Reading CSV used for feature creation...")
        key = "{}/pre-selection-1.csv".format(experiment_id)
        obj = s3.Object(bucket, key)
        self.in_data = pd.read_csv(io.BytesIO(obj.get()["Body"].read()), sep=";")
        self.in_columns = self.in_data.columns.values.tolist()
        logger.info(self.in_columns)

        # Reads CSV outputed by Featuretools
        logger.info("Reading CSV outputed by Featuretools...")
        key = "{}/feature-tools.csv".format(experiment_id)
        obj = s3.Object(bucket, key)
        out_data = pd.read_csv(io.BytesIO(next(obj.get()["Body"].iter_lines())), sep=";")

        self.class_names = out_data.columns.values.tolist()
        self.class_names.remove(self.target)
        logger.info(self.class_names)
        logger.info("DONE!")

    def transform_input(self, X: np.ndarray, names: Iterable[str], meta: Dict = None) -> Union[np.ndarray, List, str, bytes]:
        # Samples for Inference (as outputted by previous step)
        df = pd.DataFrame(X, columns=names)
        logger.info(df)

        # Appends newdata to local CSV
        csv = "original.csv"
        if os.path.exists(csv):
            df.to_csv(csv, mode="a", header=False, sep=";", index=None, index_label=None)
        else:
            df.to_csv(csv, mode="w", header=True, sep=";", index=None, index_label=None)

        # Workaround to read numeric columns as int/float
        # Also retrieves previous production data
        df = pd.read_csv(csv, sep=";")

        # Removes extra columns (dropped by pre-selection)
        df = df[self.in_columns]

        # Prepend training samples, necessary for feature computation
        df = self.in_data[self.in_columns].append(df).reset_index(drop=True)

        # Copies Target column
        dftarget = df[self.target]

        df.drop(self.target, axis=1, inplace=True)

        # Gets months from received data
        months = pd.to_datetime(df.iloc[-X.shape[0]:]['Data']).dt.strftime("%Y-%m").tolist()
        logger.info(months)
        # Selects all data (training+production) from given months
        df = df[pd.to_datetime(df[self.date]).dt.strftime("%Y-%m").isin(months)]
        logger.info(df.shape)

        # Copies Date column
        dfdate = df[self.date]

        # Compute and Concat Aggregate and Transform Features
        _, es = ana.feat(df, index="index", date=self.date, agrupada=self.group)
        df3, _ = ana.agg_features(es)
        df4, _ = ana.transf_features(es)

        df = pd.concat([df3.sort_index(), df4.sort_index()], axis=1, copy=False)
        df = df.loc[:, ~df.columns.duplicated()]

        # Adds Date column
        df[self.date] = dfdate

        # Adds Target column
        df[self.target] = dftarget

        # Selects the columns Featuretools outputted when training
        features = df[-X.shape[0]:][self.class_names]
        logger.info(features)
        return features.to_numpy()
