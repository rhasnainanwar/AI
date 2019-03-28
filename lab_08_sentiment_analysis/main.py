import pandas as pd
import re
import nltk
from bs4 import BeautifulSoup

from tqdm import tqdm

nltk.download('stopwords')
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

from sklearn.naive_bayes import MultinomialNB

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
	# data = clean_data('../../IMDBlabeledTrainData.tsv')
	data = pd.read_csv('../../IMDBcleanedData.tsv', sep='\t')

	reviews = data['review']
	sentiments = data['sentiment']

	# classifier
	vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=100)

	# fitting the model
	X = vectorizer.fit_transform(reviews).toarray()

	print(X.shape)
	print(vectorizer.vocabulary)