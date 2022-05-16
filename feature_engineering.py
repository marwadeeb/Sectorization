import pandas as pd 
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import time
import pandas as pd
import time
import nltk
import numpy as np
from sklearn import model_selection, feature_selection, feature_extraction

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
csv_path = "cleaned.csv"
df_cleaned = pd.read_csv("{}".format(csv_path), skipinitialspace=True, usecols=['Category','Website','Cleaned'], converters={'Category': convert_dtype,'Website': convert_dtype,'Cleaned': convert_dtype}, encoding='latin-1')
df_cleaned['Cleaned'].replace('', np.nan, inplace=True)
df_cleaned.dropna(subset=['Cleaned'], inplace=True)
categories = [category for category in df_cleaned['Category']]
categories = list(dict.fromkeys(categories))

## split data into train and test
df_train, df_test = model_selection.train_test_split(df_cleaned,test_size=0.05)
y_train= df_train['Category'].values

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
tfidf_vectorizer = TfidfVectorizer(max_df=0.7,min_df=0.05)
X_train = tfidf_vectorizer.fit_transform(bow) 
X_names = tfidf_vectorizer.get_feature_names_out()

## updated bow
freq_train = X_train.toarray()
u_bow = [] 
for cat in freq_train:
    features = []
    for X_name, word_freq in zip(X_names, cat):
        if word_freq > 0:
            features.append(X_name)
    u_bow.append(features)

## extract high-value features
df_where=pd.DataFrame({"category":categories})
p_value_limit = 0.05
df_features = pd.DataFrame()
for category in df_where['category']:
    chi2, p = feature_selection.chi2(X_train, df_where['category']==category)
    df_features = df_features.append(pd.DataFrame({"feature":X_names,"score":1-p, "category":category}))
    df_features = df_features.sort_values(["category","score"], ascending=[True,False])
    df_features = df_features[df_features["score"]>p_value_limit]
df_features = df_features[df_features["feature"].isin(set(nltk.corpus.words.words()))]    
df_features.drop_duplicates(subset="feature",keep=False,inplace=True)
X_names = df_features["feature"].unique().tolist()

## print features of each category
for category in np.unique(categories):
   print("# {}:".format(category))
   print("  . number of documents:",len(df_train[df_train["Category"]==category]))
   print("  . selected features:",len(df_features[df_features["category"]==category]))
   print("  . top features:", ",".join(df_features[df_features["category"]==category]["feature"].values[:50]))
   print(" ")

## fit new features into the vectorizer
vectorizer = feature_extraction.text.TfidfVectorizer(vocabulary=X_names)
vectorizer.fit(df_train['Cleaned'])
X_train = vectorizer.transform(df_train['Cleaned'])

end = time.time()
print(end-start)