import pandas as pd 
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import time
import pandas as pd
import time
from sklearn import model_selection

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
categories = [category for category in df_cleaned['Category']]
categories = list(dict.fromkeys(categories))

## split data into train and test
df_train, df_test = model_selection.train_test_split(df_cleaned,test_size=0.10)

## create bag of words for each industry
vectorizer = CountVectorizer()
bow = []
for category in categories:
    df_category = df_train[df_train['Category'] == category]
    content = ""
    for feature in df_category['Cleaned']:
        content += feature + " "
    content=content.replace("['","'")
    content=content.replace("']","'")
    content=content.replace("[]","")
    content=content.replace("''","','")
    content=content.replace("\n",",")
    bow.append(content)
X = vectorizer.fit_transform(bow)

## apply tfidf vectorizer 
X = vectorizer.fit_transform(bow)
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.2)
X_train = tfidf_vectorizer.fit_transform(bow) 
X_names = tfidf_vectorizer.get_feature_names_out()

end = time.time()
print(end-start)

