#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:20:08 2018

@author: Tampan dan Berani
"""

import pandas as pd
import re
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stopword = stop_factory.create_stop_word_remover()

data = pd.read_csv('hasil11.csv')
data = data[['Label','Isi']]

def convert(polarity):
    if polarity == 'Positif':
        return 1
    elif polarity == 'Netral':
        return 0
    else:
        return -1
    
def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', str(text)) #hanya mengijinkan huruf a - z dan A - Z
    text = re.sub(r'\b\w{1,2}\b', '', text) #menghilangkan 2 kata
    text = re.sub(r'\s\s+', ' ', text)
    text = re.sub(r"yng", "yang", text)
    text = re.sub(r"yg", "yang", text)
    text = re.sub(r"kmu", "kamu", text)
    text = re.sub(r"bgt", "banget", text)
    text = re.sub(r"tekomendasi", "rekomendasi", text)
    text = re.sub(r"trletak", "terletak", text)
    text = stemmer.stem(text)
    text = stopword.remove(text)
    text = text.lower()
    text = text.split()
    return text


# data['Isi'] = data['Isi'].map(lambda com : clean_text(com))
#data['Isi'] = data['Isi'].map(lambda com : split(com))
data['Polarity'] = data['Label'].apply(convert)

X = data['Isi']
y = data['Polarity']

bow_transformer = CountVectorizer(analyzer=clean_text).fit(X)

X = bow_transformer.transform(X)

print('Shape of Sparse Matrix: ', X.shape)
print('Amount of Non-Zero occurrences: ', X.nnz)
# Percentage of non-zero values
density = (100.0 * X.nnz / (X.shape[0] * X.shape[1]))
print('Density: {}'.format((density)))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

nb = MultinomialNB()
nb.fit(X_train, y_train)

preds = nb.predict(X_test)
print(classification_report(y_test, preds))
print(accuracy_score(y_test, preds))

