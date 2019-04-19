from scipy.spatial.distance import euclidean
import sys
import os

import pandas as pd

if __name__ == '__main__':
	ref = sys.argv[1]
	ques = sys.argv[2]

	fields = ['angles', 'blacks', 'centroids', 'normalized_sizes', 'normalized_sums', 'ratios', 'transitions']
	results = []

	for ref_img in os.listdir(ref):
		print(ref_img)

		for ques_img in os.listdir(ques):
			print(ques_img)

			result = dict()

			result['Reference'] = ref_img
			result['Questioned'] = ques_img

			for field in fields:
				ref_file = open(os.path.join(ref, ref_img, field+'.txt'), 'r')
				ques_file = open(os.path.join(ques, ques_img, field+'.txt'), 'r')

				if field == 'centroids':
					ref_data = []
					for line in ref_file.readlines():
						line = line.replace('(','').replace(')','').split(',')
						ref_data.append(float(line[0]))
						ref_data.append(float(line[1]))

					ques_data = []
					for line in ques_file.readlines():
						line = line.replace('(','').replace(')','').split(',')
						ques_data.append(float(line[0]))
						ques_data.append(float(line[1]))

				else:
					ref_data = [float(line) for line in ref_file.readlines()]
					ques_data = [float(line) for line in ques_file.readlines()]

				result[field] = euclidean(ref_data, ques_data)

			#print(result)
			results.append(result)
		print()

	df = pd.DataFrame( results )

	df.to_csv('distances.csv', index=False)