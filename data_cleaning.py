import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bf
from googletrans import Translator
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
import numpy as np
import enchant

# Downloading nltk stopwords on first run
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('words')
# nltk.download('omw-1.4')

csv_path = "lcert_formed_host_2021-03-19.csv"

## Handling unexpected input
def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)
    except:        
        return ''


df_websites = pd.read_csv("{}".format(csv_path), skipinitialspace=True, usecols=["tld","industry"], converters={'tld': convert_dtype,'industry': convert_dtype})

categories = [category for category in df_websites['industry'] if '[' not in category and category != '']
categories = list(dict.fromkeys(categories))

df_websites= df_websites[df_websites.industry.isin(categories)]

web = []
cat = []
words=[]
d = enchant.Dict("en_US")
for tld, industry in df_websites.itertuples(index=False):
    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome), "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Encoding": "gzip, deflate"}
    try:
        url = 'http://' + tld
        print(url)
        raw_html = requests.get(url, headers=header, timeout=5, verify=False)
    except: 
        continue
    soup = bf(str(raw_html.content),"html5lib")
    for tag in soup(["style","script"]):
        tag.decompose()
    text = soup.get_text(separator='\n')
    text = text[2:-2]
    for char in ['\\n', '\\t', '\\r','\\x']:
        text = text.replace(char, '')
    text = re.compile(r"\s+").sub(" ",text).strip().lower()
    text = re.sub('[^a-z ]','',text)
    text = text.split()
    all_stopwords = stopwords.words('english')
    all_stopwords.extend(["email","home","contact","website","online","news","phone","copyright","reserved","sitemap","newsletter","navigation","homepage","article",""])
    wordnet_lemmatizer = WordNetLemmatizer()
    text = [wordnet_lemmatizer.lemmatize(word) for word in text if word not in all_stopwords and re.match("^[a-z]{4,12}$", wordnet_lemmatizer.lemmatize(word))]

    line = ""
    for txt in text:
        if d.check(txt):
            line += txt + " "

    web.append(tld)
    words.append(line)    
    cat.append(industry)
    df_results = pd.DataFrame({'Category':list(cat), 'Website':list(web), 'Cleaned':list(words)},columns=['Category','Website','Cleaned'])
    df_results.to_csv('cleaned.csv')
