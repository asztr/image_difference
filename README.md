# image_difference
Python code to compute the color difference (with sign) between two images

## Usage

```bash
./image_difference <image1> <image2>  
```

Optional Parameters:  
```
	[-o <string>] output filename (default: rms.png)  
	[-s <float>] scale multiplier for difference  
	[-csize <float>] size of colorbar (default: 0.8)  
	[-cmap <string>] matplotlib colormap (default: 'RdBu')  
	[-num] print total difference  
	[-d <bool>] divergent error: difference values with sign (default: True)
	[-m {error_only, cbar_only, both}] output content (error and colorbar or only one component) (default: both)
	[-vmin <float>] Minimum value in the colorbar
	[-vmax <float>] Maximum value in the colorbar
```

## Examples
In the default mode of operation the code generates an image with the color difference between two images:
```bash
./image_difference.py image1.png image2.png  
```

<img src="/examples/image1.png" width="30%"><img src="/examples/image2.png" width="30%"><img src="/examples/both.png" width="30%">


```bash
./image_difference.py image1.png image2.png  
```

<img src="/examples/image1.png" width="30%"><img src="/examples/image2.png" width="30%"><img src="/examples/rms.png" width="30%">

Removing the colorbar generates an RMS image with the exact same size of the original images,
with white background and without any added white border (padding). This is ideal to display
the difference alongside the original images.
