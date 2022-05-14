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

start = time.time()

## load data
csv_path = "cleaned.csv"
df_cleaned = pd.read_csv("{}".format(csv_path), skipinitialspace=True, usecols=['Category','Website','Cleaned'], converters={'Category': convert_dtype,'Website': convert_dtype,'Cleaned': convert_dtype}, encoding='latin-1')
categories = [category for category in df_cleaned['Category']]
categories = list(dict.fromkeys(categories))

## split data into train and test
df_train, df_test = model_selection.train_test_split(df_cleaned,test_size=0.10)

end = time.time()
print(end-start)

