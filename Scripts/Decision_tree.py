import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging
from sklearn.tree import DecisionTreeClassifier 
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

def loss_function(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    return rmse

class handler:

  def __init__(self, file_name: str, basic_level=logging.INFO):
    # Gets or creates a logger
    logger = logging.getLogger(__name__)  

    # set log level
    logger.setLevel(basic_level)

    # define file handler and set formatter
    file_handler = logging.FileHandler(file_name)
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    self.logger = logger
  
  def  get_app_logger(self) -> logging.Logger:
    return self.logger

class DecisionTreesModel:
    
    def __init__(self, X_train, X_test, y_train, y_test, max_depth=5):
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        self.clf = DecisionTreeClassifier(max_depth=4)
        self.logger = handler("models.log").get_app_logger()

        
    def train(self, folds=1):
        
        kf = KFold(n_splits = folds)
        
        iterator = kf.split(self.X_train)
        
        loss_arr = []
        acc_arr = []
        self.logger.info(f"Model DecisionTreesModel training started")

        for i in range(folds):
            train_index, valid_index = next(iterator)
            
            X_train, y_train = self.X_train.iloc[train_index], self.y_train.iloc[train_index]
            X_valid, y_valid = self.X_train.iloc[valid_index], self.y_train.iloc[valid_index]
                        
            self.clf = self.clf.fit(X_train, y_train)
            
            vali_pred = self.clf.predict(X_valid)
            
            accuracy = self.calculate_score(y_valid
                                              , vali_pred)
            
            loss = loss_function(y_valid, vali_pred)
            
            self.__printAccuracy(accuracy, i, label="Validation")
            self.__printLoss(loss, i, label="Validation")
            print()
            
            acc_arr.append(accuracy)
            loss_arr.append(loss)

            
        return self.clf, acc_arr, loss_arr



