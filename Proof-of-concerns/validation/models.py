from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split, GridSearchCV
from scipy.stats import randint
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
#=================================================================================================
import pandas as pd
import numpy as np
import json
import math
#==================================================================================================
from joblib import dump, load


class RandomForest:
    def __init__(self,X_train,y_train,X_test,y_test) -> None:
        
        self.rf_classifier = RandomForestClassifier(random_state=42)

        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        # Definir o espaço de pesquisa dos hiperparâmetros
        self.param_grid = {
            'n_estimators': [100, 200, 300, 400, 500],
            'max_features': ['auto', 'sqrt', 'log2'],
            'max_depth': [None, 10, 20, 30, 40, 50],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'bootstrap': [True, False]
        }

        self.gridSearchObj = self.gridSearch() #Utiliza o metodo de grid search para otimização de hiperparâmetros para a random forest
        self.metricsObj = self.acurracy_metrics(self.gridSearchObj["best_estimator"], self.gridSearchObj["y_pred"],self.y_test) # Realiza os testes de metricas, em cima do melhor estimador gerado pelo grid search

    def gridSearch(self): # Realiza o grid search e ja testa o modelo com os dados X_test 

        # Implementar GridSearchCV
        grid_search = GridSearchCV(estimator=self.rf_classifier, param_grid=self.param_grid, cv=3, n_jobs=-1, verbose=2)
        grid_search.fit(self.X_train, self.y_train)

        best_rf = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_scores = grid_search.best_score_
        y_pred = best_rf.predict(self.X_test)

        return {"y_pred":y_pred,"grid":grid_search,"best_estimator":best_rf,"best_params":best_params,"best_scores":best_scores}

    def acurracy_metrics(self,best_estimator,y_pred,y_test):

        # Avaliar desempenho no conjunto de treino
        train_predictions = best_estimator.predict(self.X_train)
        train_accuracy = accuracy_score(self.y_train, train_predictions)

        # Avaliar desempenho no conjunto de teste
        test_accuracy = accuracy_score(y_test, y_pred)

        # Comparar as métricas
        if train_accuracy > test_accuracy + 0.05:
           obs = "O modelo pode estar sofrendo de overfitting."
        else:
            obs = "O modelo não parece estar sofrendo de overfitting."

        return {"TrainAccuracy":train_accuracy,"TestAccuracy":test_accuracy,"obs":obs}
    
class Utils:
    def __init__(self,model,func,args) -> None:
        
        funcs = {
            "dump":self.dump_model,
            "load":self.load_model
        }

        self.instance = funcs[func](model,args)

    def dump_model(self,model,args):        
        # Para salvar o modelo
        
        if dump(model, args[0]): return True#'random_forest_model.joblib'


    def load_model(self,model,args):
        # Para carregar o modelo
        rf_classifier = load(args[0])#'random_forest_model.joblib'
        
        return rf_classifier