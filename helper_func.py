import numpy as np
import scipy.spatial.distance as dist

def factorial(n): 
	if n == 0:
		return 1
	return n*factorial(n-1)

def binomial(n, k):
	if(k<0 or k>n):
		return 0
	if(n==k or k==0):
		return 1
	return factorial(n) / (factorial(k)*factorial(n-k))

def avg_dist(data):
	tot = 0
	for i in range(len(data)):
		for j in range(len(data)):
			dist.euclidean(data[i], data[j])
	return tot / binomial(len(data), 2) #pairs