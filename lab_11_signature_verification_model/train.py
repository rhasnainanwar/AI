import sys
import os

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


fields = ['angles', 'blacks', 'centroids', 'normalized_sizes', 'normalized_sums', 'ratios', 'transitions']

if __name__ == '__main__':
	gt = pd.read_csv(sys.argv[1])
	src = sys.argv[2]

	x = []
	y = []

	for _, row in gt.iterrows():
		signo = 'Q'+str(row['Number']).zfill(3)
		print(signo)
		loc = []
		for field in fields:
			ref_file = open(os.path.join(src, signo, field+'.txt'), 'r')

			if field == 'centroids':
				ref_data = []
				for line in ref_file.readlines():
					line = line.replace('(','').replace(')','').split(',')
					ref_data.append(float(line[0]) + float(line[1]))

			else:
				ref_data = [float(line) for line in ref_file.readlines()]

			loc.append(np.mean(np.array(ref_data)))

		x.append(loc)

		if 'F' == row['Type']:
			y.append(0)
		elif 'D' == row['Type']:
			y.append(1)
		elif 'G' == row['Type']:
			y.append(2)

	X = np.array(x)
	y = np.array(y)

	print(X.shape)
	print(y.shape)


	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

	print('Training using KNN...')
	for k in range(1, 5):
		knn = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
		knn.fit(X_train, y_train)

		print('kNN accuracy with k =',k,':',knn.score(X_test, y_test))


	print('\nTraining using Naive Bayes...')
	clf = GaussianNB()
	clf.fit(X_train, y_train)

	print('NB accuracy:',clf.score(X_test, y_test))

	print('\nTraining using Decision Trees...')
	clf = DecisionTreeClassifier(random_state=56)
	clf.fit(X_train, y_train)

	print('DT accuracy:',clf.score(X_test, y_test))