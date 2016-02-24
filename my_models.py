import numpy as np
import scipy.spatial.distance as distance
from preprocessor import *


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Class my_models                                                  '
' author: mihassin                                                 '
' attributes:                                                      '
'  - __preprocessor, instance of class preprocessor                '
'  - __imgsize, product of image shape                             '
'  - __kernels'
'  -'
'  - __path, directory path to images                              '
' function:                                                        '
'  - count_data, returns the amount of images                      '
'  - get_path, returns path as string                              '
'  - get_data, returns an array containing images as pixel arrays  '
'  - __read_data, private function to gather data                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class my_models(object):
	
	def __init__(self):
		self.__preprocessor = preprocessor()
		self.__imgsize = 0
		self.__kernels = []
		self.__kernel_indx = []
		self.__path = ""


	def get_cluster_kernels(self):
		return self.__kernels


	def set_cluster_kernels(self, kernels):
		self.__kernels = kernels


	def get_training_data(self, path):
		data = self.__preprocessor.get_data_as_2d(path)
		self.__imgsize = data[1].shape[0]
		self.__path = path
		print("Data harvested")
		return data


	def __randomly_init_cluster_kernels(self, data, k):
		n = len(data)
		kernels = np.zeros((k, self.__imgsize), dtype="int")
		kernel_indx = np.zeros(k, dtype="int")
		for i in range(k):
			indx = np.random.randint(n)
			img = data[indx]
			kernel_indx[i] = indx
			kernels[i] = img
		self.__kernel_indx = kernel_indx
		self.__kernels = kernels
		return self.__kernels, self.__kernel_indx


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
	def __clusterify(self, data):
		kernels = self.get_cluster_kernels()
		distances = np.zeros(len(kernels))
		clusters = dict()
		for i in range(len(kernels)):
			clusters[i] = np.array([], dtype="int")
		for j in range(len(data)):
			i = -1
			for k in range(len(kernels)):
				if j == self.__kernel_indx[k]:
					distances[k] = -1 #if multiple images are same (empty radar)
				else:
					distances[k] = distance.euclidean(data[j], kernels[k])
			i = np.argmin(distances)
			tmp = np.array(clusters[i])
			tmp = np.append(tmp, j)
			clusters[i] = tmp
		#clusters = self.__fill_empty_clusters(clusters)
		return clusters

	#argpartition?
	def __divide_data(self, data, clusters, j):
		if(j > len(clusters)):
			return "oh my gucciness, i got one"
		subset_indx = clusters[j]
		subset = np.array([data[subset_indx[0]]])
		for i in range(1,len(subset_indx)):
			subset = np.append(subset, [data[subset_indx[i]]], axis=0)
		return subset

	#k=4, mb splitting data 
	def __k_means(self, data, k, iterations):
		clusters = dict()
		print("=========")
		for i in range(iterations):
			print("round: " + str(i+1))
			print("=========")
			clusters = self.__clusterify(data)
			print("clusterified")
			tmp_means = np.zeros(np.shape(self.__kernels))
			for j in range(k):
				print("mean: #" + str(j+1))
				subset = self.__divide_data(data, clusters, j)
				print("data division complete")
				tmp_means[j] = subset.mean(axis=0)
				#most likely new mean doesn't exists within it's cluster and meanindx loses its purpose
				self.__kernel_indx[j] = int(1e12)
				print("new mean found")
			print("=========")
			self.set_cluster_kernels(tmp_means)
		return self.__kernels, clusters


	def k_means(self, data, k, iterations):
		self.__randomly_init_cluster_kernels(data, k)
		return self.__k_means(data, k, iterations)


	def __kpp_kernel_init(self, data, K):
		N = len(data)
		# 1. Choose one center uniformly at random from among the data points
		indx = np.random.randint(N)
		indecies = np.array(indx)
		# 4. repeat steps 2. and 3. untile k kernels have been chosen		
		for k in range(K):
		# 2. For each data point x, compute D(x), the distance between x and the nearest center that has already been chosen 
			distances = np.zeros(N)
			for n in range(N):
				for i in range(len(indecies)):
					distances[n]
		# 3. Choose one new data point at random as new center, 
		#    using a weigthed probability distribution where a point x is chosen with a probability proportional to D(x)^2

		return self.__kernels, self.__kernel_indx

		
	def k_means_pp(self, data, k, iterations):
		self.__kpp_kernel_init()
		return self.__kernels, clusters


	#another slow donkey
	def __find_subset_minimum(self, subset):
		sim = np.zeros((len(subset)))
		for i in range(len(subset)):
			for j in range(len(subset)):
				sim[i] += distance.euclidean(subset[i], subset[j])
		minimum = np.argmin(sim.sum(axis=0))
		return subset[minimum]

	#mean index if necessary
	def k_medoids(self, data, k, iterations):
		clusters = dict()
		self.__randomly_init_cluster_kernels(data, k)
		print("=========")
		for i in range(iterations):
			print("round: " + str(i))
			print("=========")
			clusters = self.__clusterify(data)
			print("clusterified")
			tmp_kernels = np.zeros(np.shape(self.__kernels))
			for j in range(k):
				print("mean: #" + str(j))
				subset = self.__divide_data(data, clusters, j)
				print("data division complete")
				tmp_kernels[j] == self.__find_subset_minimum(subset)
				print("new mean found")
			print("=========")
			self.set_cluster_kernels(tmp_kernels)
		return self.__kernels, clusters