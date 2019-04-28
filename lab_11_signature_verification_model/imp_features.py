import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

from pprint import pprint

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

	print(len(x), len(x[0]))
	print(len(y))

	# Create the RFE object and rank each pixel
	print('Find the right features...')
	knn = KNeighborsClassifier(n_neighbors=3)
	sfs1 = SFS(knn, 
           k_features=7, 
           forward=True, 
           floating=True, 
           verbose=2,
           scoring='accuracy',
           cv=0,
           n_jobs=-1)

	sfs1 = sfs1.fit(np.array(x), np.array(y), custom_feature_names=tuple(fields))
	print()
	pprint(sfs1.subsets_)