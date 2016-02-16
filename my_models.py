import numpy as np
import numpy.random as rand
from preprocessor import *


class my_models:
	
	def __init__(self):
		self.__preprocessor = preprocessor()
		self.__training_data = []
		self.__means = []


	def get_cluster_means(self):
		return self.__means


	def get_training_data(self, path):
		self.__training_data = self.__preprocessor.get_data(path)
		return "done"


	def __randomly_init_cluster_means(self, k):
		n = self.__preprocessor.count_data()
		for i in range(k):
			img = self.__training_data[rand.randint(n)]
			self.__means.append(img)
		return self.__means


	def __clusterify():
		return


	def __divide_data():
		return


	def __newmean(self, subset):
		mean = np.sum(subset, axis=0)
		mean /= len(subset)
		return mean


	def k_means(self, k):
		clusters = dict()
		self.__randomly_init_cluster_means(k)
		while True:
			clusters = __clusterify()
			tmp_means = []
			for j in range(k):
				subset = divide_data()
				tmp_means[j] = newmean(subset)
			if self.__means == tmp_means:
				break
		return self.__means

	#requires modifications
	def __find_subset_minimum(self, dis_X, subset):
    	mu_key = -1
    	mu_dist = 1.0e12
    	tmp_dist = 0
    	for i in subset:
        	for j in subset:
            	tmp_dist += dis_X[i][j] 
        	if mu_dist > tmp_dist:
            	mu_key = i
            	mu_dist = tmp_dist
    	return X[mu_key]


	def k_metoids(self, k):
		clusters = dict()
		self.__randomly_init_cluster_means(k)
		while True:
			clusters = __clusterify()
			tmp_means = []
			for j in range(k):
				subset = self.__subset(clusters, j)
				tmp_means[k] == self.__find_subset_minimum(subset)
			if self.__means == tmp_means:
				break
			self.__means = tmp_means
		return self.__means