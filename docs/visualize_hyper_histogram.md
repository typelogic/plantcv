## Plot Histogram for Hyperspectral Images

This is a plotting method that is used to examine the distrubution of signal within an hyperspectral image for specific wavelengths. This function is an application of the [histogram](visualize_histogram.md) function.

**plantcv.visualize.histogram**(*array, mask=None, bins=100, lower_bound=None, upper_bound=None, title=None, wvlengths=[480, 550, 670]*)

**returns** fig_hist

- **Parameters:**
    - array - Spectral_data
    - mask - Optional binary mask made from selected contours.
    - bins - Number of class to divide spectrum into (default bins=100).
    - lower_bound - Lower bound of range to be shown in the histogram (default lower_range=None). 
    - upper_bound - Upper bound of range to be shown in the histogram. 
    - title - The title for the histogram (default title=None) 
    - wvlengths - Interested wavelengths (in nanometers) to show histogram of (default wvlengths=[480, 550, 670])
    
- **Context:**
    - Examine the distribution of the signal, this can help select a value for calling the binary thresholding function.
    - If the provided wavelength is in the range of visible spectrum, the color corresponds to the wavelength would be used as the histogram color
    
- **Example use:**
<!---
    - [Use In NIR Tutorial](nir_tutorial.md)
  --->

**Hyperspectral image**

![Screenshot](img/documentation_images/hyper_histogram/hyper.png)

**Mask**

![Screenshot](img/documentation_images/hyper_histogram/mask.png)

```python

from plantcv import plantcv as pcv

pcv.params.debug = "plot"

# Showing histograms for 3 default wavelengths
hist_figure1 = pcv.visualize.hyper_histogram(array, mask=mask)

# Showing the histogram for a single wavelength (700nm)
hist_figure2 = pcv.visualize.hyper_histogram(array, mask=mask, wvlengths=[700])

# Showing the histogram for two wavelengths (the 970nm is not in the range of visible spectrum)
hist_figure3 = pcv.visualize.hyper_histogram(array, mask=mask, wvlengths=[380, 970])

```

**Histogram of signal intensity**

![hist_default](img/documentation_images/hyper_histogram/hist_default_bands.png)
![hist_single](img/documentation_images/hyper_histogram/hist_single_band.png)
![hist_two](img/documentation_images/hyper_histogram/hist_two_bands.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/hyper_histogram.py)