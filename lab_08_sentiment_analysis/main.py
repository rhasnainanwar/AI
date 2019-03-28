import pandas as pd
import re
import nltk
from bs4 import BeautifulSoup
import numpy as np
import sys

from tqdm import tqdm
from random import choices

nltk.download('stopwords')
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def clean_data(file_name):
	print('Reading data...')
	data = pd.read_csv(file_name, sep='\t')

	print('Cleaning data...')
	# removing extra characters
	regex = re.compile('[^a-zA-Z]')
	for ind, row in tqdm(data.iterrows()):
		# removing HTML tags
		clean_text = BeautifulSoup(row['review'], 'lxml').text
		# words without alphanumeric characters
		words = regex.sub(' ', clean_text).lower().split()
		# removing stop words
		words = [w for w in words if w not in stops]
		# combining
		sentence = ' '.join(words)

		# adding back to dataframe
		data['review'][ind] = sentence

	# save to fild
	# print('Saving data...')
	# data.to_csv(file_name.split('/')[-1].split('.')[0]+'.tsv', sep='\t')
	return data

if __name__ == '__main__':
	data = clean_data('../../IMDBlabeledTrainData.tsv')
	# data = pd.read_csv('../../IMDBcleanedData.tsv', sep='\t')

	reviews = data['review']
	sentiments = data['sentiment']

	X_train, X_test, y_train, y_test = train_test_split(reviews, sentiments, test_size=0.20)
	
	alpha = float(sys.argv[1])
	featrues = int(sys.argv[2])

	# featrues extraction
	vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=featrues)

	# get features
	X = vectorizer.fit_transform(X_train).toarray()

	# classifier
	print('Training with alpha=',alpha,'\tNO. of Features:',featrues)
	classifier = MultinomialNB(alpha=alpha)

	# fitting the model
	classifier.fit(X, np.array(y_train))

	# test
	tX = vectorizer.transform(X_test).toarray()

	y_pred = classifier.predict(tX)

	print('Accuracy:',accuracy_score(y_test, y_pred))