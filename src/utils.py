import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn.base import clone

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for model_name, model in models.items():
            # Get parameters for current model
            para = param[model_name]
            
            if model_name in ["CatBoosting Regressor", "XGBRegressor"]:
                # For these models, manually try parameters
                best_score = float('-inf')
                best_params = None
                
                # Manual parameter search
                for p in ParameterGrid(para):
                    temp_model = clone(model)
                    temp_model.set_params(**p)
                    temp_model.fit(X_train, y_train)
                    score = r2_score(y_test, temp_model.predict(X_test))
                    
                    if score > best_score:
                        best_score = score
                        best_params = p
                
                # Train final model with best parameters
                model.set_params(**best_params)
                model.fit(X_train, y_train)
            else:
                # For other models, use GridSearchCV
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

            # Evaluate model
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)