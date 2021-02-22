import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import pickle


# functions for preprocessing data and predicting value

def process_origin(df):
    df['Origin'] = df['Origin'].map({1: ' India', 2: 'USA', 3: 'Germany'})
    return df


def numerical_transform_pipeline(data):

    numerics = ['float64', 'int64']

    num_attrs = data.select_dtypes(include=numerics)

    num_pipeline = Pipeline([
        ('std_scaler', RobustScaler()),
    ])
    return num_attrs, num_pipeline



def pipeline_transformer(data):
    cat_attrs = ["Origin"]

    numerical_col_names, numerical_transformer = numerical_transform_pipeline(data)
    preprocessor = ColumnTransformer(
        [('numeric', numerical_transformer, list(numerical_col_names)), ('categorical', OneHotEncoder(), cat_attrs)])
    preprocessor.fit_transform(data)
    return preprocessor


def predict_mpg(config, model):
    if type(config) == dict:
        df = pd.DataFrame(config)
    else:
        df = config
    # preprocess the data
    df = process_origin(df)
    pipeline = pipeline_transformer(df)
    prepared_df = pipeline.transform(df)

    pred = model.predict(prepared_df)
    return pred
