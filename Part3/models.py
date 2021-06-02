import sys
sys.path.insert(1, '../src')
from src import PROJECT_PATHS

import pandas as pd
import numpy as np
from collections import Counter

from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn import preprocessing

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
import re

class TopicsAnalyzer():
    def __init__(self, data):
        self.data = data
        self.X, self.y = data.drop(columns=['target']), data['target']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=0, stratify=self.y)
        
    def run_model(self, scaler, svc):
        pipe = Pipeline(
            [
                ('scaler', scaler),
                ('svc', svc)
            ]
        )
        pipe.fit(self.X_train, self.y_train)
        self.last_pipe = pipe
        
    def last_score(self):
        return self.last_pipe.score(self.X_test, self.y_test)
        
    def SVC(self):
        self.run_model(StandardScaler(), SVC())
        
    def LogisticRegression(self):
        self.run_model(StandardScaler(), LogisticRegression(max_iter=500))
        
    def LDA(self):
        self.run_model(StandardScaler(), LDA())
        
    def MakeTfIdf(self):
        def remove_stop_words(words_list):
            return [x for x in words_list if x not in sw]
        
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        sw = stopwords.words("russian")
        
        df = pd.read_csv(f"{PROJECT_PATHS.data}\\processed\\preprocessed.csv", index_col=0)
        df_oh = df.loc[:, ['TEXT', 'target']]
        mystem = Mystem() 
        df_oh['TEXT'] = df_oh['TEXT'].apply(lambda x: "".join(mystem.lemmatize(str(x))))
        df_oh['TEXT'] = df_oh.apply(lambda x: re.sub('\d+', '0', str(x["TEXT"])), axis=1)
        df_oh['TEXT'] = df_oh.apply(lambda x: " ".join(remove_stop_words(x["TEXT"].split())), axis=1)
        
        vectorizer = TfidfVectorizer()
        self.X_tf_idf = vectorizer.fit_transform(df_oh['TEXT'].tolist())
        self.vectorizer = vectorizer
        self.y_tf_idf = df_oh['target']
        
    def TopicModeling(self):
        lda = LatentDirichletAllocation(n_components=10, random_state=1)
        lda.fit(self.X_tf_idf)
        
        self.topics = lda.components_
        
    def Clustering(self, td_idf = False):
        data = self.X_tf_idf if td_idf else self.X
        target = self.y_tf_idf if td_idf else self.y
        
        kmeans = KMeans(n_clusters=10).fit(data)
        le = preprocessing.LabelEncoder().fit(target)
        self.clustering_score = metrics.adjusted_rand_score(kmeans.predict(data), le.transform(target))
        
    def LogisticRegressionGridSearch(self):
        random_search = {'penalty': ['none', 'l2'],
                         'C'      : [0.1, 0.5, 1.0]}
        
        df_results_data = {'score': [],
                           'C': [],
                           'penalty': []}

        for i in range(len(random_search['C'])):
            for j in range(len(random_search['penalty'])):
                pipe = Pipeline(
                    [
                        ('scaler', StandardScaler()),
                        ('svc', LogisticRegression(penalty=random_search['penalty'][j], C=random_search['C'][i]))
                    ]
                )
                pipe.fit(self.X_train, м.y_train)
                
                df_results_data['score'].append(pipe.score(self.X_test, self.y_test))
                df_results_data['C'].append(random_search['C'][i])
                df_results_data['penalty'].append(random_search['penalty'][j])
                
        pd.DataFrame(df_results_data)
    
        
    