# image_difference
Python code to compute the color difference (with sign) between two images

## Usage

```bash
./image_difference <image1> <image2>  
```

Optional Parameters:  
	[-o <string>] output filename (default: rms.png)  
	[-s <float>] scale multiplier for difference  
	[-cbar <bool>] show colorbar  
	[-csize <float>] size of colorbar (default: 1.0)  
	[-cmap <string>] matplotlib colormap (default: 'RdBu')  
	[-csym <bool>] colorbar symmetric  
	[-num <bool>] print total difference  
	[-sgn <bool>] difference values with sign (default: True)  

## Example

```bash
./image_difference.py -cbar=False examples/image1.png examples/image2.png  
```

<img src="/examples/image1.png" width="30%"><img src="/examples/image2.png" width="30%"><img src="/examples/rms.png" width="30%">

Removing the colorbar generates an RMS image with the exact same size of the original images,
with white background and without any added white border (padding). This is ideal to display
the difference alongside the original images.
