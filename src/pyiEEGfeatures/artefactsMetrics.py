import numpy as np

# Compute the Amplitude range for each channel

def amplrange(data_array: np.array):
    r"""
    Computes the Amplitude range for each row of the ``data_array`` provided.

    Args:
        array: an array object.

    Returns:

    """
    if (np.sum(~np.isnan(data_array)) > 2):
        result = np.nanmax(data_array) - np.nanmin(data_array)
    else:
        result = np.nan
    return result

def amplrange_axis1(data_2darray: np.ndarray):
    r"""

    Args:
        data_2darray:

    Returns:

    """
    return np.apply_along_axis(amplrange, 1, data_2darray)

def standardise(data_array: np.array):

    return (data_array-np.nanmean(data_array))/np.nanstd(data_array)
