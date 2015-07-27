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

1. In `pymel-order-curve-points.py` adjust file paths according to your system (lines: 10, 11, 119)
2. In Maya, select a ring of mesh vertices, and run the script `pymel-order-curve-points.py`

## To run pdf generation on new data

    cd pymel-svg-hack
    bin/generate-pdfs data/ordered-mouth-points.dat

# Design

1. output lists of values from Maya
2. generate SVG from values
3. convert SVG to PDF
4. import pdf to ToonBoom
