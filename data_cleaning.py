import pandas as pd
from fake_useragent import UserAgent
import requests

## Downloading nltk stopwords on first run
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

ua = UserAgent()
header = {'User-Agent':str(ua.chrome), "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Encoding": "gzip, deflate"}
url = 'http://' + df_websites['tld'][2305]
print(url)
raw_html = requests.get(url, headers=header, timeout=5, verify=False)

with open('sample_content.txt', 'w') as f:
    f.write(str(raw_html.content))
