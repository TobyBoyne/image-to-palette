import torch
from torch.optim import optimizer
from torch.nn import MSELoss


import math
import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb



HSV_SCALE = torch.tensor([2*math.pi, 1.0, 1.0])
def get_colour_distance_fn(arr, palette_size):
	"""Finds element-wise squared-distance in colour space between a pytorch tensor and an HSV colour
	Treating HSV colour space as a cone
	https://stackoverflow.com/a/39113477/12126787"""
	A = arr * HSV_SCALE
	H = torch.sin(A[..., 0]) * A[..., 1] * A[..., 2]
	S = torch.cos(A[..., 0]) * A[..., 1] * A[..., 2]
	V = A[..., 2]

	H = H.unsqueeze(0).repeat(palette_size, 1, 1)
	S = S.unsqueeze(0).repeat(palette_size, 1, 1)
	V = V.unsqueeze(0).repeat(palette_size, 1, 1)

	def f(colour):
		"""Takes a colour palette tensor (N x 3), returns distance between each pixel in image
		and the palette, as a tensor (N x H x W), where H and W are the image dimensions"""

		h, s, v = colour.T
		h = h * 2 * math.pi
		h, s, v = h[:, None, None], s[:, None, None], v[:, None, None]  # 'unsqueeze' in H, W dimensions
		dh = (H - torch.sin(h) * s * v) ** 2
		ds = (S - torch.cos(h) * s * v) ** 2
		dv = (V - v) ** 2
		return dh + ds + dv

	return f

def open_image(fname):
	rgb_image = plt.imread(f"images/{fname}")
	hsv_image = rgb_to_hsv(rgb_image)
	image_tensor = torch.from_numpy(hsv_image) * torch.tensor([1, 1, 1/255])
	return rgb_image, image_tensor


# def get_colour_tensor(colour, tensor_like):
# 	"""Returns a tensor the size of `tensor_like` with each element having a value of `colour`"""
# 	colour_tensor = torch.zeros_like(tensor_like)
# 	colour_tensor[...,:] = torch.tensor(colour)
# 	return colour_tensor


if __name__ == "__main__":
	fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)

	x, y = torch.linspace(0, 1, 100), torch.linspace(0, 1, 300)
	V, H = torch.meshgrid(x, y)
	S = torch.ones_like(V)
	HSV = torch.stack((H, S, V), dim=-1)
	print(HSV)
	RGB = hsv_to_rgb(HSV)

	# COLOUR is given as HSV
	COLOUR = torch.tensor([0.8, 0.8, 1])
	COLOUR_ARR = torch.zeros_like(HSV)
	COLOUR_ARR[...,:] = torch.from_numpy(hsv_to_rgb(COLOUR))

	dists = torch.sqrt(colour_distance(HSV, COLOUR))
	ax0.imshow(RGB, extent=[0, 360, 0, 1], aspect=150)
	ax1.imshow(COLOUR_ARR, extent=[0, 360, 0, 1], aspect=150)
	ax2.imshow(dists, extent=[0, 360, 0, 1], aspect=150)

	plt.show()