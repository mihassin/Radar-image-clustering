import matplotlib.image as mpimg
import numpy as np
import os


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Class preprocessor                                               '
' attributes:                                                      '
'  - data,   array containing image pixel arrays                   '
'  - amount, amount of images                                      '
'  - path,   path where images where gathered                      '
' function:                                                        '
'  - count_data, returns the amount of images                      '
'  - get_path, returns path as string                              '
'  - get_data, returns an array containing images as pixel arrays  '
'  - __read_data, private function to gather data                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class preprocessor:

	def __init__(self):
		self.__data = []
		self.__amount = 0
		self.__path = ""


	def count_data(self):
		return self.__amount


	def get_path(self):
		return self.__path


	def get_data(self, path):
		if self.count_data() == 0 or self.__path != path:
			self.__path = path
			self.__data = self.__read_data()
			self.__amount = len(self.__data)
		return self.__data  


	def get_data_as_1d(self):
		tmp = self.__data
		shape = np.shape(tmp[0])
		new_shape = np.product(shape)
		for i in range(self.__amount):
			tmp[i] = np.reshape(tmp[i], new_shape)
		return tmp

	#data/pics
	def __read_data(self):
		data = []
		for root, dirs, files in os.walk(self.__path):
			for file in files:
				data.append(mpimg.imread(os.path.join(root,file)))
		return data