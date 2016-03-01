import numpy as np
import scipy.spatial.distance as distance
from preprocessor import preprocessor


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Class my_models                                                                     '
' author: mihassin                                                                    '
' attributes:                                                                         '
'  - __preprocessor, instance of class preprocessor                                   '
'  - __imgsize, product of image shape                                                '
'  - __kernels, kernel images stored here as an array                                 '
'  - __kernel_indx, indecies of kernels in data                                       ' 
'  - __path, directory path to images                                                 '
' function:                                                                           '
'  - get_cluster_kernels, returns __kernels                                           '
'  - set_cluster_kernels, sets new kernels to __kernels                               ' 
'  - get_training_data, uses preprocessor to get data from given path                 '
'  - __randomly_init_cluster_kernels, selects randomly kernels                        '
'  - __clusterify, returns a dictionary filled with index arrays                      '
'  - __divide_data, old function creating subarrays replaced with __faster_div        '
'  - __faster_div, faster way to create subarrays with indecies of the original array '
'  - __k_means, basic implementation of k-means                                       '
'  - k_means, uses __k_means and initial kernels with __randomly_init_cluster_kernels '
'  - __kpp_kernel_init, helper function that finds initial kernels                    '
'  - k_means_pp, k++ implementation                                                   '
'  - __find_subset_minimum, k-medoids way to find new cluster kernel in update phase  '
'  - k_medoids, basic k_medoids implementation, without distance matrix (memory rip)  '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class my_models(object):
	

	def __init__(self):
		self.__preprocessor = preprocessor()
		self.__imgsize = 0
		self.__kernels = []
		self.__kernel_indx = []
		self.__path = ""


	def get_cluster_kernels(self):
		return self.__kernels


	#does not modify __kernel_indx
	def set_cluster_kernels(self, kernels):
		self.__kernels = kernels


    #uses preprocessor to get data as 2d array
	def get_training_data(self, path):
		data = self.__preprocessor.get_data_as_2d(path)
		self.__imgsize = data[1].shape[0]
		self.__path = path
		print("Data harvested")
		return data


	#cloud be improved 
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


	#slow as F#¤%
	#numpys built-in functions could improve the run-time
	def __clusterify(self, data):
		kernels = self.get_cluster_kernels()
		distances = np.zeros(len(kernels))
		clusters = dict()
		for i in range(len(kernels)):
			clusters[i] = np.array([], dtype="int")
		for j in range(len(data)):
			i = -1
			for k in range(len(kernels)):
				#it seems that P(empty radar image) is pretty high  
				if j == self.__kernel_indx[k]: #might not be necessary
					distances[k] = -1 #kernel belongs to it's own cluster
				else:
					distances[k] = distance.euclidean(data[j], kernels[k])
			i = np.argmin(distances)
			tmp = np.array(clusters[i])
			tmp = np.append(tmp, j)
			clusters[i] = tmp
		return clusters


	#subarray creation
	#n = 1181, avg run 36s
	def __divide_data(self, data, clusters, j): 
		if(j > len(clusters)):
			return "oh my gucciness, i got one"
		subset_indx = clusters[j]
		subset = np.array([data[subset_indx[0]]])
		for i in range(1,len(subset_indx)):
			subset = np.append(subset, [data[subset_indx[i]]], axis=0)
		return subset, subset_indx

	#n = 1181, avg run 16s
	def __faster_div(self, data, clusters, j):
		return np.array([data[i] for i in clusters[j]])

	#Basic k-means without kernel init 
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
				subset = self.__faster_div(data, clusters, j)
				print("data division complete")
				tmp_means[j] = subset.mean(axis=0)
				#most likely new mean doesn't exists within it's cluster and meanindx loses its purpose
				self.__kernel_indx[j] = int(1e12)
				print("new mean found")
			print("=========")
			if np.array_equal(tmp_means, self.__kernels):
				break
			self.set_cluster_kernels(tmp_means)
		return self.__kernels, clusters


	#Initial cluster kernels are selected randomly
	def k_means(self, data, k, iterations):
		self.__randomly_init_cluster_kernels(data, k)
		return self.__k_means(data, k, iterations)

	def __next_k(self, data, C):
		d = np.zeros(len(data))
		for i in range(len(data)):
			tmp = np.zeros(len(C))
			for j in range(len(C)):
				tmp[j] = distance.euclidean(data[i], data[j])
			d[i] = np.min(tmp)
		d **= 2
		d /= np.sum(d)
		return np.random.choice(len(data), p=d)

	''' Wikipedia.org
	1. Choose one center uniformly at random from among the data points
	2. For each data point x, compute D(x), the distance between x and the nearest center that has already been chosen 
	3. Choose one new data point at random as new center, 
	   using a weigthed probability distribution where a point x is chosen with a probability proportional to D(x)^2
	4. repeat steps 2. and 3. untile k kernels have been chosen		
	'''
	def __kpp_kernel_init(self, data, K):
		N = len(data)
		indx = np.random.randint(N)#1
		C = np.array([data[indx]], dtype="int")
		indecies = np.array([indx], dtype="int")
		while len(C) < K:#4
			sample = self.__next_k(data, C)#2 #3
			indecies = np.append(indecies, sample)
			C = np.append(C, [data[sample]], axis=0)
		self.__kernels = C
		self.__kernel_indx = indecies
		return self.__kernels, self.__kernel_indx

		
	#improved initial kernels	
	def k_means_pp(self, data, k, iterations):
		self.__kpp_kernel_init(data, k)
		return self.__k_means(data, k, iterations)


	#another slow donkey
	def __find_subset_minimum(self, subset, subset_indx):
		sim = np.zeros(len(subset))
		for i in range(len(subset)):
			for j in range(len(subset)):
				sim[i] += distance.euclidean(subset[i], subset[j])
		minimum = sim.argmin()
		return subset[minimum], subset_indx[minimum]


	#slower than k-means (IML)
	def k_medoids(self, data, k, iterations):
		clusters = dict()
		self.__randomly_init_cluster_kernels(data, k)
		print("=========")
		for i in range(iterations):
			print("round: " + str(i+1))
			print("=========")
			clusters = self.__clusterify(data)
			print("clusterified")
			tmp_kernels = np.zeros(np.shape(self.__kernels))
			tmp_indx = np.zeros(k)
			for j in range(k):
				print("mean: #" + str(j+1))
				subset = self.__faster_div(data, clusters, j)
				subset_indx = clusters[j]
				print("data division complete")
				tmp_kernels[j], tmp_indx[j] = self.__find_subset_minimum(subset, subset_indx)
				print("new mean found")
			print("=========")
			if np.array_equal(tmp_kernels, self.__kernels):
				break
			self.set_cluster_kernels(tmp_kernels)
			self.__kernel_indx = tmp_indx
		return self.__kernels, clusters