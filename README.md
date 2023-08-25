# Resize TIFF Images with Pixel Size

## **Introduction**
TIFFPixelResizer is a versatile image processing tool designed to efficiently resize TIFF images to specific pixel dimensions. This repository provides a user-friendly command-line interface and library that allows you to adjust the dimensions of TIFF images while preserving their quality and aspect ratio.

![Workflow Diagram](./imgs/im1.png)

## **Resolution**

`Resolution` refers to the level of detail in an `image` or video, which is determined by the number of `pixels` in the `[width x height]` dimensions.

**Unit**: `Pixels (px)`

## **Pixel Size**

`Pixel Size` indicates the resolution of an image, representing how many meters are covered by each pixel in the image.

**Unit**: `Meter per pixel (m/px) or (mpp)`

## **Image Density**

`Image Density` refers to the amount of information contained within a specific area or volume of an image. This can be expressed using either `Pixels per inch (PPI)` or `Dots per inch (DPI)` measurements.

## **Scaling Factor**

A `Scaling Factor` is a `constant` used to resize images by multiplying or dividing their size or dimensions.

#


## **Requirements**

- Conda (Package and environment management system)
- Python = 3.7.7 (Versatile high-level programming language)
- OpenCV (Open Computer Vision Library)
- GDAL (Geospatial Data Abstraction Library)

## Create Conda Envionment
```sh
conda env create -f environment.yml
```
### Activate the Envionment
```sh
conda activate gdal
```

## Usage
```sh
python setup.py [inputImg] [pixelSize]
```
### Example
```
python setup.py img.tiff 0.5
```

---

Feel free to contribute to this documentation by creating pull requests or raising issues.