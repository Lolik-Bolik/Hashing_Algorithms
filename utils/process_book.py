import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import multiprocessing as mp
import string
import spacy
from sklearn.base import TransformerMixin, BaseEstimator
from normalise import normalise
import os
from copy import copy
import pandas as pd


class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, variety="BrE", user_abbrevs={}, n_jobs=1):
        """
        Text preprocessing transformer includes steps:
            1. Text normalization
            2. Punctuation removal
            3. Stop words removal
            4. Lemmatization

        variety - format of date (AmE - american type, BrE - british format)
        user_abbrevs - dict of user abbreviations mappings (from normalise package)
        n_jobs - parallel jobs to run
        """
        nltk.download("brown")
        nltk.download("names")
        os.system("python -m spacy download en_core_web_sm")
        self.variety = variety
        self.user_abbrevs = user_abbrevs
        self.n_jobs = n_jobs
        self.nlp = spacy.load("en_core_web_sm")

    def fit(self, X, y=None):
        return self

    def transform(self, X, *_):
        X_copy = X.copy()

        partitions = 1
        cores = mp.cpu_count()
        if self.n_jobs <= -1:
            partitions = cores
        elif self.n_jobs <= 0:
            return X_copy.apply(self._preprocess_text)
        else:
            partitions = min(self.n_jobs, cores)

        data_split = np.array_split(X_copy, partitions)
        pool = mp.Pool(cores)
        data = pd.concat(pool.map(self._preprocess_part, data_split))
        pool.close()
        pool.join()

        return data

    def _preprocess_part(self, part):
        return part.apply(self._preprocess_text)

    def _preprocess_text(self, text):
        normalized_text = self._normalize(text)
        doc = self.nlp(normalized_text)
        removed_punct = self._remove_punct(doc)
        removed_stop_words = self._remove_stop_words(removed_punct)
        return self._lemmatize(removed_stop_words)

    def _normalize(self, text):
        # some issues in normalise package
        try:
            return " ".join(
                normalise(
                    text,
                    variety=self.variety,
                    user_abbrevs=self.user_abbrevs,
                    verbose=False,
                )
            )
        except:
            return text

    def _remove_punct(self, doc):
        return [t for t in doc if t.text not in string.punctuation]

    def _remove_stop_words(self, doc):
        return [t for t in doc if not t.is_stop]

    def _lemmatize(self, doc):
        return " ".join([t.lemma_ for t in doc])


def preprocess_text(save_path):
    df_bbc = pd.read_csv("data/bbc-text.csv")
    text = TextPreprocessor(n_jobs=-1).transform(df_bbc["text"])
    df_bbc["text"] = text
    df_bbc.to_csv(save_path, sep=",", index=False)
    return True
