import pandas as pd 
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import time
import pandas as pd
import time
import nltk
import numpy as np
from sklearn import model_selection, feature_selection
import itertools as IT

## Handling unexpected input
def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)
    except:        
        return ''

# start time
start = time.time()

## load data
csv_path = "sample.csv"
df_cleaned = pd.read_csv("{}".format(csv_path), skipinitialspace=True, usecols=['Category','Website','Cleaned'], converters={'Category': convert_dtype,'Website': convert_dtype,'Cleaned': convert_dtype}, encoding='latin-1')
categories = [category for category in df_cleaned['Category']]
categories = list(dict.fromkeys(categories))

## split data into train and test
df_train, df_test = model_selection.train_test_split(df_cleaned,test_size=0.05)

## create bag of words for each industry
bow = []
for category in categories:
    df_category = df_train[df_train['Category'] == category]
    content = ""
    for feature in df_category['Cleaned']:
        content += feature + " "
    bow.append(content)

# apply tfidf vectorizer  
X = CountVectorizer().fit_transform(bow)
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.05)
X_train = tfidf_vectorizer.fit_transform(bow) 
X_names = tfidf_vectorizer.get_feature_names_out()
print(X_names)

## updated bow
freq_train = X_train.toarray()
u_bow = [] 
for cat in freq_train:
    features = []
    for X_name, word_freq in zip(X_names, cat):
        if word_freq != 0:
            features.append(X_name)
    u_bow.append(features)



end = time.time()
print(end-start)

