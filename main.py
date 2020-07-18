import torch
from tqdm import tqdm
import matplotlib.pyplot as plt

from model import Model
from colour import open_image



if __name__ == "__main__":
	rgb_image, image_tensor = open_image("fox.jpg")

	model = Model(5, image_tensor)
	optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)

	with tqdm(range(100)) as tqdm_iter:
		for i in tqdm_iter:
			optimizer.zero_grad()
			loss = model.loss_fn()
			loss.backward()
			optimizer.step()

			tqdm_iter.set_description(f"{loss:.5f}")

	print(model.palette)

	fig, (ax0, ax1) = plt.subplots()