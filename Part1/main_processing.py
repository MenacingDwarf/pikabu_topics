"""Main data preparation after crawling step."""
import os
import re

import pandas as pd

from regex import UNICODE, VERBOSE, compile

import sys
sys.path.insert(1, '../src')
from src import PROJECT_PATHS

def load_parsed(path=f"{PROJECT_PATHS.data}\\raw\\"):
    """Load bunch of csvs.

    Args:
        path (str, optional): Path to directory with crawled data.
            Defaults to PROJECT_PATHS.data/'raw'.

    Returns:
        pandas.DataFrame: Gathered data.
    """
    print("\n-----------------------------------------------\n \
           Loading data started...")
    df = pd.DataFrame()
    ENG_TAGS = PROJECT_PATHS.ENG_TAGS
    for tag in ENG_TAGS:
        print(f"Load {tag} data...")
        tag_df = pd.read_csv(path + f"date_{tag}.csv", index_col=0)
        tag_df['TAGS'] = tag_df['TAGS'].map(lambda tags: tags.split('|'))
        for n_tag in ENG_TAGS:
            value = 0
            if tag == n_tag:
                value = 1
            tag_df[n_tag] = value
        df = df.append(tag_df)
        
    print(f"End loading data. Dataframe shape: {df.shape}")
    return df


def remove_html_tags(df, text_col="TEXT", substitute=""):
    """Replace html tags with space.

    May cause texts removal such as <sample text>.
    """
    print("\n-----------------------------------------------\n \
           Remove html tags")
    regexp = re.compile(r"<[^<>]*>")
    
    df[text_col] = df[text_col].map(lambda x: regexp.sub(substitute, x))


def remove_urls(df, text_col="TEXT", substitute=""):
    """Replace urls with space."""

    def replace_url(string):
        sub = r"""
        (?<=^|[\s<"'(\([{])            # visual border
        (                             # RFC3986-like URIs:
            [A-z]+                    # required scheme
            ://                       # required hier-part
            (?:[^@]+@)?               # optional user
            (?:[\w-]+\.)+\w+          # required host
            (?::\d+)?                 # optional port
            (?:\/[^?\#\s'">)\]}]*)?   # optional path
            (?:\?[^\#\s'">)\]}]+)?    # optional query
            (?:\#[^\s'">)\]}]+)?      # optional fragment
        |                             # simplified e-Mail addresses:
            [\w.#$%&'*+/=!?^`{|}~-]+  # local part
            @                         # klammeraffe
            (?:[\w-]+\.)+             # (sub-)domain(s)
            \w+                       # TLD
        )(?=[\s>"')\)]}]|$)            # visual border
        """
        sub = compile(sub, UNICODE | VERBOSE)
        return sub.sub(substitute, string)

    print("\n-----------------------------------------------\n \
           Remove urls")
    df[text_col] = df[text_col].map(replace_url)


def remove_punctuation(df, text_col="TEXT", substitute=" "):
    def replace_punctuation(text):
        sub = r"""['!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~']+"""
        return re.sub(sub, substitute, text)
    
    print("\n-----------------------------------------------\n \
           Remove punctuation")
    df[text_col] = df[text_col].map(replace_punctuation)


if __name__ == "__main__":
    df = load_parsed()
    df.to_csv(f"{PROJECT_PATHS.data}\\processed\\peeled.csv")
