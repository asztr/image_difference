#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns; sns.set()
import numpy as np
import sys
import imageio
import argparse

def rms(image1, image2, signed=False, **kwargs):
	img1 = imageio.read_image(image1)
	img2 = imageio.read_image(image2)

	diff_rgb = img2-img1
	rms = np.linalg.norm(diff_rgb, axis=2)

	if not signed:
		return rms
	else:
		diff_rgb_sum = np.sum(diff_rgb, axis=2)
		sgn = -1 + 2*(diff_rgb_sum >= 0)
		return sgn * rms

def plot_rms(rms, output='rms.png', scale=1.0, cmap='RdBu', cbar_symmetric=False, cbar=False, cbar_size=0.8, **kwargs):
	if (cmap == 'Tom'):
		rms_cmap = tom_cmap
	else:
		orig_cmap = plt.get_cmap(cmap)
		rms_cmap = mcolors.LinearSegmentedColormap.from_list(name='rms_cmap', N=255, colors=[orig_cmap(0), (1,1,1), orig_cmap(255)])

	vmin, vmax = None, None
	if (cbar_symmetric):
		vmax = max(np.abs(rms.min()), rms.max())
		vmin = -vmax

	dpi = 100.0 #approx value. not used unless we wanted to plot this directly.
	fig = plt.figure(figsize=(rms.shape[1]/dpi, rms.shape[0]/dpi), frameon=False)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	sns.heatmap(scale * rms, cmap=rms_cmap, center=0, annot=False, vmin=vmin, vmax=vmax,
				xticklabels=False, yticklabels=False, cbar=cbar, ax=ax, cbar_kws={'shrink':cbar_size})
	fig.savefig(output, dpi=dpi)

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Compute signed square difference between two images')
	parser.add_argument('image1', help='Input image 1')
	parser.add_argument('image2', help='Input image 2')
	parser.add_argument('-o', '--output', default='rms.png', type=str)
	parser.add_argument('-cscale', '--scale', default=1.0, type=float)
	parser.add_argument('-cbar', '--cbar', default=True)
	parser.add_argument('-csize', '--cbar_size', default=0.8, type=float)
	parser.add_argument('-cmap', '--cmap', default='RdBu', type=str)
	parser.add_argument('-cbar_sym', '--cbar_symmetric', default=False, help='symmetric colorbar')
	parser.add_argument('-num', '--numeric', default=False, help='print total rms')
	parser.add_argument('-sgn', '--signed', default=True, help='absolute difference')
	
	args = parser.parse_args()
	args_dict = vars(args)

	rms = rms(**args_dict)
	
	if (args.numeric):
		print(rms.ravel().sum())
	else:
		plot_rms(rms, **args_dict)
