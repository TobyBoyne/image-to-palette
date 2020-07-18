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