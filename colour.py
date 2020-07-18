import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import numpy as np

from scipy import ndimage



def colour_distance(c0, c1):
	"""Finds the distance in colour space between two HSV values
	Treating HSV colour space as a cone
	https://stackoverflow.com/a/39113477/12126787"""
	(h0, s0, v0), (h1, s1, v1) = c0, c1
	h0, h1 = h0*2*np.pi, h1*2*np.pi
	v0, v1 = v0 / 255, v1 / 255
	dh = (np.sin(h0)*s0*v0 - np.sin(h1)*s1*v1) ** 2
	ds = (np.cos(h0)*s0*v0 - np.cos(h1)*s1*v1) ** 2
	dv = (v0 - v1) ** 2
	dist = np.sqrt(dh + ds + dv)
	return dist

def colour_distance_arrs(a0, a1):
	"""Finds element-wise squared-distance in colour space between two arrays of HSV values
	Treating HSV colour space as a cone
	https://stackoverflow.com/a/39113477/12126787"""
	h0, h1 = a0[...,0]*2*np.pi, a1[...,0]*2*np.pi
	s0, s1 = a0[...,1],         a1[...,1]
	v0, v1 = a0[...,2]/255,     a1[...,2]/255

	dh = (np.sin(h0) * s0 * v0 - np.sin(h1) * s1 * v1) ** 2
	ds = (np.cos(h0) * s0 * v0 - np.cos(h1) * s1 * v1) ** 2
	dv = (v0 - v1) ** 2

	return dh + ds + dv

if __name__ == "__main__":
	fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)

	V, H = np.mgrid[0:1:100j, 0:1:300j]
	S = np.ones_like(V)
	HSV = np.dstack((H, S, V))
	RGB = hsv_to_rgb(HSV)

	RED = np.zeros_like(RGB)
	RED[...,:] = [0.0, 1.0, 0.0]

	dists = np.sqrt(colour_distance_arrs(HSV, rgb_to_hsv(RED)))

	ax0.imshow(RGB, extent=[0, 360, 0, 1], aspect=150)
	ax1.imshow(RED, extent=[0, 360, 0, 1], aspect=150)
	ax2.imshow(dists, extent=[0, 360, 0, 1], aspect=150)

	plt.show()