import json
import pathlib

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from compress_fasttext.models import CompressedFastTextKeyedVectors
import fasttext


import sys
sys.path.insert(1, '../src')
from src import PROJECT_PATHS

def make_cos_list(list_, period=24):
    def make_cos(value, period=period):
        return np.cos(value*2*np.pi/period)
    return [make_cos(x) for x in list_]
    
def make_sin_list(list_, period=24):
    def make_sin(value, period=period):
        return np.sin(value*2*np.pi/period)
    return [make_sin(x) for x in list_]

def data_additional_processing(df):
    df["HOUR"] = df["TIMESTAMP"].map(lambda x: x.hour)
    df["YEAR"] = df["TIMESTAMP"].map(lambda x: x.year)
    df["MONTH"] = df["TIMESTAMP"].map(lambda x: x.month)
    df["WEEKDAY"] = df["TIMESTAMP"].map(lambda x: x.weekday())
    df["WEEK"] = df["TIMESTAMP"].map(lambda x: x.week)
    
    df['sin_hour'] = make_sin_list(df['HOUR'])
    df['cos_hour'] = make_cos_list(df['HOUR'])

    df['cos_month'] = make_cos_list(df['MONTH'], 12)
    df['sin_month'] = make_sin_list(df["MONTH"], 12)

    df['cos_weekday'] = make_cos_list(df['WEEKDAY'], 7) 
    df['sin_weekday'] = make_sin_list(df['WEEKDAY'], 7)

    df.drop(columns=['HOUR', 'MONTH', 'WEEKDAY'], inplace=True)
    
    return df
    
def download_fasttext():
    fasttext.util.download_model('ru', if_exists='ignore')
    ft = fasttext.load_model('cc.ru.300.bin')
    
def embed(tokens, default_size=300):
    if not tokens:
        return np.zeros(default_size)
    embs = [embeddings[_normalize_string(x)] for x in tokens]
    return sum(embs) / len(tokens)

def _normalize_string(text):
    return text.replace('ё', 'е')

def remove_stop_words(words_list):
    return [x for x in words_list if x not in sw]
    
def process_record(record):
    return embed(remove_stop_words(record.split()))
    
def text_additional_processing(df):
    df.drop(df[df['TITLE'] == 'удалено'].index, inplace=True)
    df["TITLE"][df['TITLE'].isnull()] = ''
    df['LIKES'] = df['LIKES'].fillna(0)
    df.drop(columns=["TAGS", "NICKNAME", "TEXT_PUNCT", "TITLE_PUNCT", "YEAR", "WEEK", "TIMESTAMP", "TIME_GAP"], inplace=True)
    df.drop(index = df.loc[~(df['TITLE'].str.len() > 0)].index, inplace=True)
    
    nltk.download('stopwords')
    sw = stopwords.words("russian")
    cur_path = pathlib.Path().absolute()
    embs = f"{cur_path}\\cc.ru.300.bin"
    embeddings = fasttext.load_model(embs)
    
    df['emb_title'] = df['TITLE'].map(process_record)
    df['emb_text'] = df['TEXT'].map(str).map(process_record)
    df.drop(columns=['TITLE', 'TEXT'], inplace=True)
    df['emb_title'] = df['emb_title'].map(lambda x: json.dumps([float(y) for y in x]))
    df['emb_text'] = df['emb_text'].map(lambda x: json.dumps([float(y) for y in x]))
    emb_text = pd.DataFrame(df['emb_text'].map(json.loads).to_list(), 
                            columns=[f"emb_text_{i}" for i in range(300)])
    emb_title = pd.DataFrame(np.array(df['emb_title'].map(json.loads).to_list()), 
                             columns=[f"emb_title_{i}" for i in range(300)])
    df_embedded = pd.concat([df.drop(columns=['emb_title', 'emb_text']).reset_index(drop=True),
                         emb_text, emb_title], axis=1)
                         
    return df_embedded
    
if __name__ == "__main__":
    # download_fasttext()
    df = pd.read_csv(f"{PROJECT_PATHS.data}\\processed\\preprocessed.csv", index_col=0)
    df = data_additional_processing(df)
    df = text_additional_processing(df)
    df_embedded.to_csv(f"{PROJECT_PATHS.data}\\processed\\final_embeded.csv")
    
    