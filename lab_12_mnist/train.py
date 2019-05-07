import numpy as np
from matplotlib import pyplot as plt

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, ShuffleSplit
from sklearn.neural_network import MLPClassifier

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

if __name__ == '__main__':
	# loading dataset
	print('Fetching and loading MNIST dataset...')
	mnist = load_digits()
	X, y = mnist.data, mnist.target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

	print('Training set:', X_train.shape, y_train.shape)
	
	# model
	print('\nSetting MLP...')
	mlp = MLPClassifier(hidden_layer_sizes=(20,8), batch_size=128, learning_rate_init=0.005)

	print('\nCrossing Validation')
	print(cross_val_score(mlp, X[:500], y[:500], cv=5, n_jobs=-1))

	print('\nTraining MLP...')
	mlp.fit(X_train,y_train)

	print('Train accuracy:', mlp.score(X_train, y_train)*100)
	print('Test accuracy:', mlp.score(X_test, y_test)*100)

	print('\nPlotting...')

	title = "Learning Curves (MLP)"
	plot_learning_curve(mlp, title, X, y, ylim=(0.7, 1.01), cv=5)
	plt.show()