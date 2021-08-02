#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import scipy
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

def pct_fmt(x, pos):
    return r'${0:.2g} \%$'.format(x*100.0)

def sign(x):
	return x/np.abs(x)

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False, sensitivity=1.0):
		self.midpoint = midpoint
		self.sensitivity = sensitivity
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, values, clip=None):
		minleg = (self.midpoint + self.vmin) / (2.0 * self.sensitivity)
		maxleg = (self.vmax + self.midpoint) / (2.0 * self.sensitivity)
		x, y = [self.vmin, minleg, self.midpoint, maxleg, self.vmax], [0.0, 0.25, 0.5, 0.75, 1.0]
		interp_f = scipy.interpolate.interp1d(x, y, kind='slinear')
		interp_values = interp_f(np.array(values))
		return np.ma.masked_array(interp_values)

def plot_rms(rms, output='rms.png', mode='both', scale=1.0, cmap='RdBu', cbar_size=0.8, cbar_sens=1.0, vmin=None, vmax=None, cbar_pad=0.01, pct_ticks=False, **kwargs):
	orig_cmap = plt.get_cmap(cmap)
	rms_cmap = colors.LinearSegmentedColormap.from_list(name='rms_cmap', N=255, colors=[orig_cmap(0), (1,1,1), orig_cmap(255)]) #this adds a white color in the midpoint of the chosen colormap (remove if not divergent cmap)

	dpi = 100.0 #approx value. not used unless we wanted to plot this directly.
	fig = plt.figure(figsize=(rms.shape[1]/dpi, rms.shape[0]/dpi), frameon=False)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	ax2 = plt.Axes(fig, [1.0, 0.5*(1-cbar_size), 0.05, cbar_size])
	fig.add_axes(ax2)

	if (vmin is None) and (vmax is None):
		_min, _max = rms.min(), rms.max()
		if (sign(_min) != sign(_max)):
			absmax = max(-_min, _max)
			vmin, vmax = -absmax, absmax
		elif (sign(_min) == +1):
			vmin, vmax = 0.0, _max
		else:
			vmin, vmax = _min, 0.0

	sns.heatmap(scale * rms, 
				norm=MidpointNormalize(midpoint=0., vmin=vmin, vmax=vmax, sensitivity=cbar_sens),
				vmin=vmin, vmax=vmax, cbar=True, cmap=rms_cmap, cbar_ax=ax2,
				annot=False, xticklabels=False, yticklabels=False, ax=ax,
				cbar_kws={'format':ticker.FuncFormatter(pct_fmt)} if pct_ticks else {})

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
	parser.add_argument('-cpad', '--cbar_pad', default=0.01, type=float, help='colorbar padding')
	parser.add_argument('-csens', '--cbar_sens', default=1.0, type=float, help='colorbar sensitivity (higher values -> color gradient is higher close to zero)')
	parser.add_argument('-num', '--numeric', action='store_true', default=False, help='print rms')
	parser.add_argument('-d', '--divergent', default=True, help='signed difference (tip: use divergent colormap)')
	parser.add_argument('-m', '--mode', choices=['error_only', 'cbar_only', 'both'], default='both')
	parser.add_argument('-p', '--pct_ticks', action='store_true', default=False, help='use percentages in the colorbar')
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
