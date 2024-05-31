from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import pandas as pd
import numpy as np
import math
import csv, json

class Files:

    def __init__(self,funct,args=None):
        self.instancied = True
        
        self.mapped = {
            "make_json":self.make_json
        }

        if funct and args != None: self.mapped[funct](args)

    def make_json(self,args): # Função para conversão de csv em json, baseado em uma primary key
        
        #csvFilePath, jsonFilePath,primaryKey
        csvFilePath = args[0]
        jsonFilePath = args[1]
        primaryKey = args[2]

        data = {}
        
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            
            for rows in csvReader:
                
                key = rows[primaryKey]
                data[key] = rows

        self.export_json(jsonFilePath,data)
        self.jsonFile = self.load_json(jsonFilePath)

    def load_json(self,jsonFilePath):
        
        with open(jsonFilePath,"r") as file:
            datasset = json.load(file)

        return datasset
    
    def export_json(self,jsonFilePath,data):

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
  

class Modeling:
    def __init__(self,datasset,targets,drops=None) -> None: #features
        
        dataframe = pd.DataFrame(datasset)
        self.dataframe = dataframe.dropna()

        if drops is not None:
            self.dataframe = self.dataframe.drop(drops, axis=1)

        self.target = self.dataframe[targets]
        self.features = self.dataframe.drop(targets,axis=1)

        self.uniqueTargetsCount= {i:{"UniqueValues":self.calc_uniqueValues(self.dataframe[i]),"UniqueProbability":self.calc_uniqueProbability(self.dataframe[i]),"informationGain":{}} for i in targets}
    
        
        self.loop_information_gain(self.features,self.uniqueTargetsCount)

        self.Encoder_X=LabelEncoder() # Cria uma instância de codificação para posterioridade em novos dados

        self.encoded_features = self.label_encoder(self.features)
        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test(self.encoded_features,self.target)
    
    def calc_entropy(self,column,UniqueProbability):
        
        # Calcula a probabilidade de cada valor dividindo pela quantidade total de elementos na coluna
        probabilities = UniqueProbability / len(column)
        
        entropy = 0  # Valor inicial da entropia
        
        # Loop para calcular a entropia de cada valor único
        for prob in probabilities:
            if prob > 0:
                entropy += prob * math.log(prob, 2)  # Calcula a entropia de cada valor e soma ao total

        return -entropy  # Retorna o negativo da entropia conforme a fórmula
    
    def loop_information_gain(self,features,probsDataframe): # Preenche o campo de ganho de informação pra cada feature em relação a um target

        for k in probsDataframe:

            for j in features:

                probsDataframe[k]["informationGain"][j] = self.information_gain(self.dataframe,j,k,probsDataframe[k]["UniqueProbability"])
    
    def information_gain(self,data, split,target,UniqueProbability): # Calcula de fato o ganho de informação para cada feature em relação ao target

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
    
    def label_encoder(self,X): # Realiza uma codificação para int das features de texto no datasset, utilizando label_encoder
        
        seed = 42
        np.random.seed(seed)

        for col in X.columns:
            X[col]=self.Encoder_X.fit_transform(X[col])
        
        return X
    
    def train_test(self,X,y): # Divide os dados em treino e teste

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        return X_train, X_test, y_train, y_test
    
    def calc_uniqueValues(self,data): # calcula os valores unicos
        return np.bincount(data)
    
    def calc_uniqueProbability(self,data): # calcula a probabilidade de cada elemento unico de ocorrência 
        return self.calc_uniqueValues(data)/(len(data))

    