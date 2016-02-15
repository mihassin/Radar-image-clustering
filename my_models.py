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


	def k_means(self, k):
		self.__randomly_init_cluster_means(k)
		while True:
			clusterify()
			tmp_means = []
			for j in range(k):
				cluster_j = []
				newmean_j
			if self.__means == tmp_means:
				break
		return self.__means


	def k_metoids(self):
		return "TODO"