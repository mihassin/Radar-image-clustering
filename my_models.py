import numpy as np
import numpy.random as rand
import scipy.spatial.distance as distance
from preprocessor import *

import time


class my_models(object):
	
	def __init__(self):
		self.__preprocessor = preprocessor()
		self.__imgsize = 480*720*3
		self.__means = []
		self.__meanindx = []
		self.__path = ""


	def get_cluster_means(self):
		return self.__means


	def set_cluster_means(self, means):
		self.__means = means


	def get_training_data(self, path):
		print(len(self.__training_data))
		if len(self.__training_data) == 0 or self.__path != path:
			data = self.__preprocessor.get_data(path)
			self.__training_data = self.__preprocessor.get_data_as_1d()
		print("Data harvested")
		return self.__training_data


	def randomly_init_cluster_means(self, k):
		n = self.__preprocessor.count_data()
		means = np.zeros((k, self.__imgsize), dtype="int")
		meanindx = np.zeros(k, dtype="int")
		for i in range(k):
			indx = rand.randint(n)
			img = self.__training_data[indx]
			meanindx[i] = indx
			means[i] = img
		self.__meanindx = meanindx
		self.__means = means
		return self.__means, self.__meanindx


	def fill_empty_clusters(self, clusters):
		n = self.__preprocessor.count_data()
		for i in range(len(clusters)):
			if len(clusters[i]) == 0:
				indx = rand.randint(n)
				arr = list(clusters.values())
				arr.pop(n)
				clusters[i] = 'asd'

	#empty set handeling
	#slow as F#¤%
	def clusterify(self):
		start = time.clock()
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
		return clusters, (time.clock()-start)


	def divide_data(self, clusters, j):
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


	def find_subset_minimum(self, subset):
		sim = np.zeros((len(subset)))
		for i in range(len(subset)):
			for j in range(len(subset)):
				sim[i] = distance.euclidean(subset[i], subset[j])
		minimum = np.argmin(sim.sum(axis=0))
		return subset[minimum]

	#mean index if necessary
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
				tmp_means[j] == self.__find_subset_minimum(subset)
				print("new mean found")
			print("=========")
			if np.array_equal(self.__means, tmp_means):
				print("done")
				break
			self.set_cluster_means(tmp_means)
			i += 1
		return self.__means