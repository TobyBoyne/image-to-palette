import torch
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

from model import Model
from colour import open_image



if __name__ == "__main__":
	rgb_image, image_tensor = open_image("fox.jpg")

	model = Model(5, image_tensor)
	optimizer = torch.optim.SGD(model.parameters(), lr=5e-2)

	with tqdm(range(10)) as tqdm_iter:
		for i in tqdm_iter:
			optimizer.zero_grad()
			loss = model.loss_fn()
			loss.backward()
			optimizer.step()
			model.palette.sigmoid()

			tqdm_iter.set_description(f"{loss:.5f}")

	print(model.palette)

	fig, (ax0, ax1, ax2) = plt.subplots(nrows=3,
										subplot_kw=dict(xticks=[], yticks=[]))

	ax0.imshow(rgb_image)
	palette_colours = model.palette.detach().unsqueeze(0).numpy()
	ax1.imshow(hsv_to_rgb(palette_colours))

	_, palette_idx = model.colour_distance(model.palette).min(0)
	palette_img = model.palette[palette_idx].detach().numpy()
	ax2.imshow(hsv_to_rgb(palette_img))

	plt.show()