import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
	src = sys.argv[1]
	n = int(sys.argv[2])

	fields = ['angles', 'blacks', 'centroids', 'normalized_sizes', 'normalized_sums', 'ratios', 'transitions']
	disguised = ['Q006', 'Q015', 'Q028', 'Q029', 'Q034', 'Q087', 'Q090']

	df =  pd.read_csv(src)
	df = df.sample(frac=1)
	
	df = df[~df.Questioned.isin(disguised)]

	x = df['Reference'] + df['Questioned']
	x = x[:n]

	for field in fields:
		print(field.capitalize())
		y = df[field][:n]

		plt.scatter(x, y)
		plt.title(field.upper())
		plt.xticks(rotation=70)
		plt.show()