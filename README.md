# image_difference
Python code to compute the color difference (with sign) between two images

## Usage

```bash
./image_difference <image1> <image2>  
```

Optional Parameters:  
```
	[--output <string>] output filename (default: rms.png)  
	[--scale <float>] scale multiplier for difference  
	[--cbar_size <float>] size of colorbar (default: 0.8)  
	[--cmap <string>] matplotlib colormap (default: 'RdBu')  
	[--cbar_pad <float>] padding of the colorbar (default: 0.01)
	[--cbar_sens <float>] colorbar sensitivity (higher values -> higher color gradient close to zero) (default: 1.0)
	[--numeric] print total difference  
	[--divergent <bool>] divergent error: difference values with sign (default: True)
	[--mode {error_only, cbar_only, both}] output content (error and colorbar or only one component) (default: both)
	[--pct_ticks] show colorbar values as percentages
	[--vmin <float>] Minimum value in the colorbar
	[--vmax <float>] Maximum value in the colorbar
```

## Examples
In the default mode of operation the code generates an image with the color difference between two images:
```bash
./image_difference.py image1.png image2.png  
```

<img src="/img/image1.png" width="30%"><img src="/img/image2.png" width="30%"><img src="/img/both.png" width="30%">

However the error image has a different resolution than the original images, which is bothersome for visual comparison.
To solve this problem we can use the error_only mode, which produces an error image with the original resolution, without
any white border (padding):
```bash
./image_difference.py image1.png image2.png --mode error_only
```

<img align="center" src="/img/image1.png" width="30%"><img align="center" src="/img/image2.png" width="30%"><img align="center" src="/img/rms.png" width="30%"><img align="center" src="/img/cbar.png" width="5%">

This is ideal to display the difference alongside the original images. If we also wish to show the colorbar, we need to generate it in a separate image file:
```bash
./image_difference.py image1.png image2.png --mode cbar_only --output cbar.png
```

## Color difference computation

The color difference is computed as:
<p align="center">
	<img src="/img/diff-eqn.png" width="50%">
</p>

were the denominator is a normalization factor so that the maximum possible difference in a single pixel is 1 (which happens when the pixel is pure white in one image and pure black in the other). With the option --pct_ticks we can convert these values to percentages.

## Colorbar sensitivity

For plots where most of the information is contained in a subset of the colorbar range (e.g. low values of error), it might be useful to change the sensitivity parameter:
```bash
./image_difference.py image1.png image2.png --cbar_sens <value>
```
<p align="center">
	<img src='/img/cbar_sensitivity.png' width='60%'>
</p>

## Colormap

With the --cmap option we can specify the colormap. All matplotlib cmaps are supported, although in the default case (with positive and negative error values) divergent colormaps with a white center are recommended. For a list of colormaps:
<a href="https://matplotlib.org/users/colormaps.html">https://matplotlib.org/users/colormaps.html</a>
