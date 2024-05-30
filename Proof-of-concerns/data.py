from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import pandas as pd
import numpy as np
import math

class Modeling:
    def __init__(self,datasset,targets,drops=None) -> None: #features
        
        dataframe = pd.DataFrame(datasset)
        self.dataframe = dataframe.dropna()

        if drops != None:
            for i in drops:
                self.dataframe = self.dataframe.drop(i,axis=1)

        self.target = self.dataframe[targets]
        self.features = self.dataframe.drop(targets,axis=1)

        self.uniqueTargetsCount= {i:{"UniqueValues":np.bincount(self.dataframe[i]),"UniqueProbability":np.bincount(self.dataframe[i])/(len(self.dataframe[i])),"informationGain":{}} for i in targets}
    
        for k in self.uniqueTargetsCount:

            for j in self.features:

                self.uniqueTargetsCount[k]["informationGain"][j] = self.information_gain(self.dataframe,j,k,self.uniqueTargetsCount[k]["UniqueProbability"])

        self.encoded_features = self.label_encoder(self.features)
        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test(self.encoded_features,self.target)
    
    def calc_entropy(self,column,UniqueProbability):
        # Conta o número de ocorrências de cada valor único na coluna
        #UniqueProbability
        
        # Calcula a probabilidade de cada valor dividindo pela quantidade total de elementos na coluna
        probabilities = UniqueProbability / len(column)
        
        entropy = 0  # Valor inicial da entropia
        
        # Loop para calcular a entropia de cada valor único
        for prob in probabilities:
            if prob > 0:
                entropy += prob * math.log(prob, 2)  # Calcula a entropia de cada valor e soma ao total

        return -entropy  # Retorna o negativo da entropia conforme a fórmula
    
    def information_gain(self,data, split,target,UniqueProbability):

        original_entropy=self.calc_entropy(data[target],UniqueProbability)

        values=data[split].unique()

        if len(values) < 2:
            # Se houver menos de dois valores únicos, não é possível dividir, então o ganho de informação é 0
            return 0

        left_split=data[data[split]==values[0]]

        right_split=data[data[split]==values[1]]

        subract=0

        for subset in [left_split,right_split]:
            
            prob=(subset.shape[0])/data.shape[0]
            subract += prob * self.calc_entropy(subset[target],UniqueProbability)

        return  original_entropy - subract
    
    def label_encoder(self,X):
        Encoder_X=LabelEncoder()

        for col in X.columns:
            X[col]=Encoder_X.fit_transform(X[col])
        
        return X
    
    def train_test(self,X,y):

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        return X_train, X_test, y_train, y_test