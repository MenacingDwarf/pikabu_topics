# Import packages and read data

import json
import re
from ast import literal_eval
from string import punctuation

import pandas as pd
from regex import UNICODE, VERBOSE, compile
from segtok.tokenizer import word_tokenizer

from main_processing import (remove_html_tags, remove_punctuation, remove_urls, load_parsed)

import sys
sys.path.insert(1, '../src/data')
from src import PROJECT_PATHS

df = load_parsed()

# Text and title processing

remove_urls(df)
df["TEXT_PUNCT"] = df["TEXT"].copy()
df["TITLE_PUNCT"] = df["TITLE"].copy()
remove_punctuation(df, "TEXT")
remove_punctuation(df, 'TITLE')
df["TEXT"] = df['TEXT'].str.lower()
df['TEXT_PUNCT'] = df['TEXT_PUNCT'].str.lower()

df.drop(columns=['VIEWS'], inplace=True)

# Add target column

target_tags = PROJECT_PATHS.ENG_TAGS
numered_tags = list(enumerate(sorted(target_tags)))
df['target'] = sum([df[tag].map(lambda z: x if z else 0) for x, tag in numered_tags])
numered_tags
for x in target_tags:
    del df[x]
    
df.to_csv(f"{PROJECT_PATHS.data}\\processed\\preprocessed.csv")