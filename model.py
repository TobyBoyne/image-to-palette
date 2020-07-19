import torch

from colour import get_colour_distance_fn, open_image

class Model(torch.nn.Module):
	def __init__(self, num_colours, image):
		super().__init__()
		palette = torch.rand((num_colours, 3))
		self.palette = torch.nn.Parameter(palette)

		self.image_size = image.size()[:-1]
		self.colour_distance = get_colour_distance_fn(image, num_colours)

	def loss_fn(self):
		"""Returns the loss for a given input image with current palette choice"""
		all_dists = self.colour_distance(self.palette)
		min_dists, _ = all_dists.min(0)

		loss = min_dists.mean()
		return loss



if __name__ == "__main__":
	_, image = open_image("fox.jpg")
	model = Model(5, image)
	loss = model.loss_fn()
	print(loss)