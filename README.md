# Maya to ToonBoom pipeline

This software allows you to start in Maya with a closed curve of contiguous points that is a subset of a deformable/animated mesh in Maya, and export 2d positions those points in a range of frames, and save these as pdf and svg.

This was developed for Mac OS.

The steps to operating the software are as follows:

1. Open Maya and select the closed curve of vertices that are desired.
2. Adjust I/O paths in `pymel-order-curve-points.py` as described below.
3. Run `pymel-order-curve-points.py` to generate position data for the points in the range of frames, one point per file, and one line per frame in each file. By default a file called `ordered-mouth-points.dat` will be generated in the same folder as the point position data files. That file must be passed as an argument in the next step.

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

## To run on new data

1. In `pymel-order-curve-points.py` adjust file paths according to your system (lines: [10](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L10), [11](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L11), [119](https://github.com/scottgwald/pymel-svg-hack/blob/master/pymel-order-curve-points.py#L119))
2. In Maya, select a ring of mesh vertices, and run the script `pymel-order-curve-points.py`

The resulting pdf frames are in a `pdf` folder in the same directory as the ordered points file.
By default, that file is `data/ordered-mouth-points.dat`, and hence the resulting pdfs
are in the folder `data/pdf`.

# Design

1. output lists of values from Maya
2. generate SVG from values
3. convert SVG to PDF
4. import pdf to ToonBoom
