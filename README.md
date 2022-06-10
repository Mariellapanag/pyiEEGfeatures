# pyEDFieeg

![Image](https://github.com/Mariellapanag/pyEDFieeg/blob/main/GitpageImages/frontimage.png?raw=true)

![Python Versions](https://img.shields.io/badge/python-^3.8<3.11-blue)
![Development](https://img.shields.io/badge/development-active-green.svg)
[![License](https://img.shields.io/github/license/mariellaPanag/pyEDFieeg.svg)](https://github.com/Mariellapanag/pyEDFieeg/blob/main/LICENSE)

##  Useful functions for navigating unstructured folders of EDF files, gathering useful information and extracting specified segments of data.

## About

This package was motivated by the necessity of collecting and organising electroencephalographic (EEG) recordings from unstructured folders with European Data Format (EDF) files.
Real data collected from patients with epilepsy often have several issues:
1. EDF files might overlap, either in the entire time period that enclose or in parts of it
2. Channels might be drop out along the recording period
3. Channels might be added along the recording period
4. Missing recordings might be present along the entire recording

## Installation

The ```pip``` tool can be used to download the package

```bash
$ pip install git+https://github.com/Mariellapanag/pyEDFieeg.git
```
or

```bash
$ git clone https://github.com/Mariellapanag/pyEDFieeg.git
```
then the whole repository is being downloaded. The library root is located in the ```.\src``` folder.

## Dependencies

### For the ```root``` package

* [[pandas = "^1.4.2"]](https://pandas.pydata.org/)

* [[pyEDFlib = "^0.1.28"]](https://pypi.org/project/pyEDFlib/)

* [[scipy = "^1.8.1"]](http://scipy.org)

* [[matplotlib = "^3.5.2"]](https://matplotlib.org)

* [[plotly = "^5.8.0"]](https://plotly.com/python/)

* [[kaleido = "0.2.1"]](https://pypi.org/project/kaleido/)

### for running the ```processingUCLH``` scripts

[[openpyxl = "^3.0.10"]](https://openpyxl.readthedocs.io/en/stable/)

## Documentation

The documentation can be found here [[Sphinx documentation]](https://mariellapanag.github.io/pyEDFieeg/)


## Acknowledgements

Resources, help and support was provided within the [Computational Neurology, Neuroscience & Psychiatry Lab](https://sites.google.com/view/cnnp-lab/home) at Newcastle University.
> The CNNP Lab is a group of interdisciplinary researchers working on Computational Neurology, Neuroscience, and Psychiatry (psychology). 
> We apply theoretical and computational approaches to questions in the neuroscience domain. The lab members come from a colourful mix of backgrounds, ranging from computing, 
>mathematics, statistics, and engineering to biology, psychology, neuroscience, and neurology.


## References

## License

Released under the MIT license.



