import numpy as np
import numpy.random as rand
import scipy.spatial.distance as distance
from preprocessor import *


class my_models(object):
	
	def __init__(self):
		self.__preprocessor = preprocessor()
		self.__training_data = []
		self.__imgsize = 480*720*3
		self.__means = np.zeros((10, self.__imgsize), dtype="int")
		self.__meanindx = np.zeros(10, dtype="int")
		self.__path = ""


	def get_cluster_means(self):
		return self.__means


	def set_cluster_means(self, means):
		self.__means = means


	def get_training_data(self, path):
		print(len(self.__training_data))
		if len(self.__training_data) == 0 or self.__path != path:
			data = self.__preprocessor.get_data(path)
			print("Data harvested")
			self.__training_data = self.__preprocessor.get_data_as_1d()
			print("Data in 1d")
		return self.__training_data


	def __randomly_init_cluster_means(self, k):
		n = self.__preprocessor.count_data()
		for i in range(k):
			indx = rand.randint(n)
			img = self.__training_data[indx]
			self.__meanindx[i] = indx
			self.__means[i] = img
		return self.__means, self.__meanindx


	def __fill_empty_clusters(self, clusters):
		n = self.__preprocessor.count_data()
		for i in range(len(clusters)):
			if len(clusters[i]) == 0:
				indx = rand.randint(n)
				arr = list(clusters.values())
				arr.pop(n)
				clusters[i] = 'asd'

	#empty set handeling
	#slow as F#¤%
	def __clusterify(self):
		data = self.__training_data
		means = self.get_cluster_means()
		distances = np.zeros(len(means))
		clusters = dict()
		for i in range(len(means)):
			clusters[i] = np.array([], dtype="int")
		for j in range(self.__preprocessor.count_data()):
			i = -1
			for k in range(len(means)):
				if j == self.__meanindx[k]:
					distances[k] = -1 #if multiple images are same (empty radar)
				else:
					distances[k] = distance.euclidean(data[j], means[k])
			i = np.argmin(distances)
			tmp = np.array(clusters[i])
			tmp = np.append(tmp, j)
			clusters[i] = tmp
		#clusters = self.__fill_empty_clusters(clusters)
		return clusters

	#empty set handeling
	def __divide_data(self, clusters, j):
		subset_indx = clusters[j]
		data = self.__training_data
		subset = np.array([data[subset_indx[0]]])
		for i in range(1,len(subset_indx)):
			subset = np.append(subset, [data[subset_indx[i]]], axis=0)
		return subset


	def k_means(self, k):
		clusters = dict()
		self.__randomly_init_cluster_means(k)
		print("=========")
		i = 1
		while True:
			print("round: " + str(i))
			print("=========")
			clusters = self.__clusterify()
			print("clusterified")
			tmp_means = np.zeros(np.shape(self.__means))
			for j in range(k):
				print("mean: #" + str(j))
				subset = self.__divide_data(clusters, j)
				print("data division complete")
				tmp_means[j] = subset.mean(axis=0)
				#most likely new mean doesn't exists within it's cluster and meanindx loses its purpose
				self.__meanindx[j] = int(1e12)
				print("new mean found")
			print("=========")
			if np.array_equal(self.__means, tmp_means):
				print("done")
				break
			self.set_cluster_means(tmp_means)
			i += 1
		return self.__means

	
	def __find_subset_minimum(self, subset):
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
		print("=========")
		i = 1
		while True:
			print("round: " + str(i))
			print("=========")
			clusters = self.__clusterify()
			print("clusterified")
			tmp_means = np.zeros(np.shape(self.__means))
			for j in range(k):
				print("mean: #" + str(j))
				subset = self.__divide_data(clusters, j)
				print("data division complete")
				tmp_means[k] == self.__find_subset_minimum(subset)
			if self.__means == tmp_means:
				break
			self.__means = tmp_means
		return self.__means