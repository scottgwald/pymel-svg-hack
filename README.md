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

Select a ring of mesh vertices, and run the script `pymel-order-curve-points.py`

# Design

1. output lists of values from Maya
2. generate SVG from values
3. convert SVG to PDF
4. import pdf to ToonBoom
