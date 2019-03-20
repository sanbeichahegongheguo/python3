import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def demo1():
    mu, sigma = 0, 1
    sampleNo = 100
    np.random.seed(0)
    s = np.random.normal(mu, sigma, sampleNo)

    plt.hist(s, bins=100, normed=True)
    plt.show()

demo1()