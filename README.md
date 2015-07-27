# Maya to ToonBoom pipeline

This was developed for Mac OS.

# Dependencies

* Maya
* [pymel](https://github.com/LumaPictures/pymel/releases)
* inkscape

# Demo

## To run pdf generation on sample data

    cd pymel-svg-hack
    bin/generate-pdfs sample-data/ordered-mouth-points.dat


The script generates intermediate data in subfolders of the
folder containing the ordered list of points.

## To generate new data from Maya

1. In `pymel-order-curve-points.py` adjust file paths according to your system (lines: [10](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L10), [11](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L11), [119](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L119))
2. In Maya, select a ring of mesh vertices, and run the script `pymel-order-curve-points.py`

## To run pdf generation on new data

    cd pymel-svg-hack
    bin/generate-pdfs data/ordered-mouth-points.dat

The resulting pdf frames are in a `pdf` folder in the same directory as the ordered points file.
In this case, that file is `data/ordered-mouth-points.dat`, and hence the resulting pdfs
are in the folder `data/pdf`.

# Design

1. output lists of values from Maya
2. generate SVG from values
3. convert SVG to PDF
4. import pdf to ToonBoom
