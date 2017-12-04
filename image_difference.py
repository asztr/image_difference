#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns; sns.set()
import numpy as np
import sys
import imageio
import argparse

def rms(image1, image2, divergent=False, **kwargs):
	img1 = imageio.read_image(image1)
	img2 = imageio.read_image(image2)

	diff_rgb = img2-img1
	rms = np.linalg.norm(diff_rgb, axis=2)

	if not divergent:
		return rms
	else:
		diff_rgb_sum = np.sum(diff_rgb, axis=2)
		sgn = -1 + 2*(diff_rgb_sum >= 0)
		return sgn * rms

def plot_rms(rms, output='rms.png', scale=1.0, cmap='RdBu', cbar_size=0.8, vmin=None, vmax=None, mode='both', **kwargs):
	orig_cmap = plt.get_cmap(cmap)
	rms_cmap = mcolors.LinearSegmentedColormap.from_list(name='rms_cmap', N=255, colors=[orig_cmap(0), (1,1,1), orig_cmap(255)])

	dpi = 100.0 #approx value. not used unless we wanted to plot this directly.
	fig = plt.figure(figsize=(rms.shape[1]/dpi, rms.shape[0]/dpi), frameon=False)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	ax2 = plt.Axes(fig, [1.0, 0.5*(1-cbar_size), 0.05, cbar_size])
	fig.add_axes(ax2)

	sns.heatmap(scale * rms, cmap=rms_cmap, center=0, annot=False, vmin=vmin, vmax=vmax,
				xticklabels=False, yticklabels=False, cbar=True, ax=ax, cbar_ax=ax2) #cbar_kws={'shrink':cbar_size}

	if (mode == 'both'):
		fig.savefig(output, dpi=dpi, bbox_inches='tight')
	elif (mode == 'error_only'):
		ax2.remove()
		fig.savefig(output, dpi=dpi)
	elif (mode == 'cbar_only'):
		ax.remove()
		fig.savefig(output, bbox_inches='tight')

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Compute signed square difference between two images')
	parser.add_argument('image1', help='Input image 1')
	parser.add_argument('image2', help='Input image 2')
	parser.add_argument('-o', '--output', default='rms.png')
	parser.add_argument('-s', '--scale', default=1.0, type=float)
	parser.add_argument('-csize', '--cbar_size', default=0.8, type=float)
	parser.add_argument('-cmap', '--cmap', default='RdBu', help='colormap')
	parser.add_argument('-num', '--numeric', action='store_true', default=False, help='print rms')
	parser.add_argument('-d', '--divergent', default=True, help='signed difference (tip: use divergent colormap)')
	parser.add_argument('-m', '--mode', choices=['error_only', 'cbar_only', 'both'], default='both')
	parser.add_argument('-vmin', '--vmin', default=None, type=float)
	parser.add_argument('-vmax', '--vmax', default=None, type=float)

	args = parser.parse_args()
	args_dict = vars(args)

	rms = rms(**args_dict)

	if (args.numeric):
		_rms = rms.ravel()
		print('Total error: ', _rms.sum(), '\n')
		print('Min: ', _rms.min(), '. Max: ', _rms.max())
	else:
		plot_rms(rms, **args_dict)
