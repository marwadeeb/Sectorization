> Data analysis:
	we saw the number of websites we have in each category using a histogram
	we viewed one of the websites text we have (uncleaned)
	we plotted the difference in length between the websites and they were close
> Feature Engineering:
		################################################
	1. Text Cleaning and Preparation: cleaning of special characters, downcasing, punctuation signs. possessive pronouns and stop words removal and lemmatization.
	2. Label coding: creation of a dictionary to map each category to a code.
	3. Train-test split: to test the models on unseen data.
	4. Text representation: use of TF-IDF scores to represent text.
		#################################################
	1) we loaded the data set and visualized a sample
	special character cleaning \r \n \* "
	lower case the whole content
	remove punctuation
	remove possessive pronouns
	lemmaization
	stop words
	2) give a number to each category
	3) divide the set we have randomly
	4) from github:
We have various options:

- Count Vectors as features
- TF-IDF Vectors as features
- Word Embeddings as features
- Text / NLP based features
- Topic Models as features

We'll use TF-IDF Vectors as features.

We have to define the different parameters:

+ ngram_range: We want to consider both unigrams and bigrams.
+ max_df: When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold
+ min_df: When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold.
+ max_features: If not None, build a vocabulary that only consider the top max_features ordered by term frequency across the corpus.

examples:
# 'business' category:
  . Most correlated unigrams:
. market
. price
. economy
. growth
. bank
  . Most correlated bigrams:
. last year
. year old

# 'entertainment' category:
  . Most correlated unigrams:
. tv
. music
. star
. award
. film
  . Most correlated bigrams:
. mr blair
. prime minister