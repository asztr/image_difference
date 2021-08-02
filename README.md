# image_difference
A flexible Python code to compute the signed RMSE difference between two images.

## Usage

```bash
$ python image_difference.py <image1> <image2>  
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
$ python image_difference.py image1.png image2.png  
```

<img align="center" src="/img/image1.png" width="30%"><img align="center" src="/img/image2.png" width="30%"><img align="center" src="/img/rms.png" width="30%"><img align="center" src="/img/cbar.png" width="5%">

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
