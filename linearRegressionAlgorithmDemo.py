from statistics import mean
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')

#xs = np.array([1,2,3,4,5,6], dtype=np.float64)
#ys = np.array([5,4,6,5,7,8], dtype=np.float64)

def createDataset(amt, varience, step=2, correlation=False):
	val = 1
	ys = []
	for i in range(amt):
		y = val + random.randrange(-varience, varience)
		ys.append(y)
		if correlation and correlation == 'pos':
			val += step
		elif correlation and correlation == 'neg':
			val -= step

	xs = [i for i in range(len(ys))]

	return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)


def bestFitSlope_Intercept(xs,ys):
	m = ( ((mean(xs) * mean(ys)) - mean(xs * ys)) / 
		((mean(xs) * mean(xs)) - mean(xs * xs)) )
	b = mean(ys) - m * mean(xs)

	return m, b

def squaredError(ys_orig, ys_line):
	return sum((ys_line-ys_orig)**2)

def coefficientOfDeterminitaion(ys_orig, ys_line):
	y_mean_line = [mean(ys_orig) for y in ys_orig]
	squared_error_regr = squaredError(ys_orig, ys_line)
	squared_error_y_mean = squaredError(ys_orig, y_mean_line)
	return 1 - (squared_error_regr / squared_error_y_mean)

xs, ys =  createDataset(40, 80, 2, correlation=False)

m, b = bestFitSlope_Intercept(xs,ys)

regression_line = [(m*x + b) for x in xs]

rSquared = coefficientOfDeterminitaion(ys, regression_line)

print(m, b, rSquared)

plt.scatter(xs, ys)
plt.plot(xs, regression_line)
plt.show()