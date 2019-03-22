import pandas as pd
import re
import nltk
from bs4 import BeautifulSoup

from tqdm import tqdm

nltk.download('stopwords')
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

if __name__ == '__main__':

	print('Reading data...')
	data = pd.read_csv('../../IMDBlabeledTrainData.tsv', sep='\t')

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
	print('Saving data...')
	data.to_csv('../../IMDBcleanedData.tsv', sep='\t')