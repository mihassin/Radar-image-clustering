import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os


def count_data(data):
	return len(data)


def read_data(root):
	data = []
	for root, dirs, files in os.walk(root):
		for file in files:
			img = mpimg.imread(os.path.join(root,file))
			data.append(mpimg.imread(os.path.join(root,file)))
	return data