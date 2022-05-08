import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

csv_path = "lcert_formed_host_2021-03-19.csv"

df_websites = pd.read_csv("{}".format(csv_path), skipinitialspace=True, usecols=["tld","industry"])

categories = [category for category in df_websites['industry'] if '[' not in category]
categories = set(filter(None, categories))
print(categories)

df_filtered = df_websites[df_websites["industry"].isin(categories)]
df_remaining = df_websites[~df_websites["industry"].isin(categories)]

counted = Counter(df_filtered["industry"])
counted.update({"Multilabel":len(df_remaining), "Blank":len([cell for cell in df_websites['industry'] if cell == ''])})
bar = plt.bar(counted.keys(), counted.values(), 0.5)
plt.show()
