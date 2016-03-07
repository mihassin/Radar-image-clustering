import numpy as np
import matplotlib.pyplot as plt

def small_im_429_k_ite():
	plt.title("Iterations vs. K")
	plt.plot(range(1,8), [2,6,5,6,5,6,7], "b", label='k-means')
	plt.plot(range(1,8), [2,2,4,5,3,7,8], "g", label='k-means++')
	plt.plot(range(1,8), [2,2,2,3,2,5,3], "r", label='k-medoids')
	plt.legend(loc="upper left")
	plt.ylim(1,8)
	plt.xlim(1,7)
	ax = plt.gca()
	ax.set_ylabel("iterations")
	ax.set_xlabel("K")
	plt.show()

def small_im_429_k_sim():
	plt.title("Similarity vs. K")
	plt.plot(range(1,8), [0., 0.42568385, 0.66943681, 0.7086565, 0.45180703, 0.55535718, 0.36814961], "b", label='k-means')
	plt.plot(range(1,8), [0.47187195, 1.26259759, 1.43059756, 0.25311395,0. ,1.07364746, 0.47181107], "g", label='k-means++')
	plt.plot(range(1,8), [1.14122916, 0., 1.08783383, 1.48782411, 2.03165995, 1.76882027, 2.08283833], "r", label='k-medoids')
	plt.legend(loc="upper left")
	plt.ylim(0,2.1)
	plt.xlim(1,7)
	ax = plt.gca()
	ax.set_ylabel("similarity")
	ax.set_xlabel("K")
	plt.show()

#km 1498.839, 2136.87056 ,2502.217, 2561.001, 2176.025, 2331.23, 2050.636
#kpp 1498.839, 2304.052, 2475.13, 1276.073, 1018.3216, 2111.64, 1498.777
#kmed 1498.839, 699.99, 1461.4628, 1741.452, 2122.13165, 1938.1465, 2157.956

#normalisation
#1. find set min
#2. div all set elements with min
#3. substract 1 from every set element