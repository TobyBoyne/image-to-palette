import torch

from colour import get_colour_distance_fn

class Model(torch.nn.Module):
	def __init__(self, num_colours, image):
		super().__init__()
		palette = torch.rand((num_colours, 3))
		self.palette = torch.nn.Parameter(palette)

		self.image_size = image.size()[:-1]
		self.colour_distance = get_colour_distance_fn(image)

	def loss_fn(self):
		"""Returns the loss for a given input image with current palette choice"""
		min_dists = None
		for colour in self.palette:
			dists = self.colour_distance(colour)
			if min_dists is None:
				min_dists = dists
			else:
				min_dists = torch.min(min_dists, dists)


		loss = min_dists.mean()
		return loss



if __name__ == "__main__":
	SIZE = (20, 20)
	model = Model(5, SIZE)
	for colour in model.palette:
		print(colour)
		a, b, c = colour
		print(a)
