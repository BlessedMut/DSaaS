import base64

from io import StringIO
import io

import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn import linear_model
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import pickle
import matplotlib.pyplot as plt
import seaborn as sns


class OrionAI:
    # def __init__(self, path):
    #     self.path = path

    def load_dataset(self):
        try:
            filename, file_extension = os.path.splitext(self.path)
            if file_extension == '.csv':
                df = pd.read_csv(self.path, low_memory=False)
                return df
            elif file_extension == '.xlsx':
                df = pd.read_excel(self.path, low_memory=False)
                return df
        except FileNotFoundError as e:
            print(f"File not found Error!\n\nReason\n{'-' * 100}\n{e}\n{'-' * 100}")

    def exploratory_data_analysis(self, df):
        """:cvar df
        """
        print("Columns in datasets")
        print(df.columns)

        print("*" * 50)

        print("Dataset statistics")
        print(df.describe(include="all"))

    def encode_dataframe(self, df):
        """
            The encode_dataframe one hot encodes columns that are either in categorical form or object dtypes.
        """
        try:
            df = self.load_dataset()
        except:
            df = df

        columnsToEncode = list(df.select_dtypes(include=['category', 'object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                df[feature] = le.fit_transform(df[feature])
            except:
                print('Error encoding ' + feature)
        return df

    def ind_dep_columns(self, col):
        """
            The ind_dep_columns extracts the dependent as well as the dependent columns which will be used in the train test split func.
        """
        df = self.encode_dataframe()
        independent_columns = df.loc[:, df.columns != col]
        dependent_columns = df[col]
        return independent_columns, dependent_columns

    def correlation_of_features(dataframe):
        try:
            img = StringIO()
            # get correlations of each features in dataset
            corrmat = dataframe.corr()
            top_corr_features = corrmat.index
            # plot heat map
            g = sns.heatmap(dataframe[top_corr_features].corr(), annot=True, cmap="RdYlGn")
            plt.savefig(img, format="png")
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue())
            return plot_url
        except ValueError:
            df = OrionAI().encode_dataframe(dataframe)
            print(df)
            img = StringIO()
            # get correlations of each features in dataset
            corrmat = df.corr()
            top_corr_features = corrmat.index
            # plot heat map
            g = sns.heatmap(df[top_corr_features].corr(), annot=True, cmap="RdYlGn")
            plt.savefig(img, format="png")
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue())
            return plot_url

    def feature_extraction_selection(self, dependant_col):
        """
        Given a dataset, it extracts the most best n (sel_cols) of the independent features.
        """
        X, Y = self.ind_dep_columns(dependant_col)
        model = ExtraTreesRegressor()
        model.fit(X, Y)
        feat_importances = pd.Series(model.feature_importances_, index=X.columns)
        X = X[feat_importances.nlargest(
            10).index.to_list()]  # Filter the features with the top 10 most important features
        return X, Y

    def split_data(self, test_size, X, Y):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size)
        return X_train, X_test, Y_train, Y_test

    def save_model(self, model_name, folder_name):
        if os.path.exists(str(folder_name)):
            with open(str(model_name), mode="wb") as model:
                pickle.dump(str(model_name), model)
        else:
            os.mkdir(folder_name)
            with open(str(model_name), mode="wb") as model:
                pickle.dump(str(model_name), model)
