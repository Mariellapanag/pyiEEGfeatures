import numpy as np

def NaNControl(EEGdata, which_channel, srate, winLength, NaNthreshold, overlap):
    '''

    Args:
        EEGdata: matrix of EEG data, dimensions: channels x time points
        srate: sampling frequency in Hz
        winLength: the window length to split the data in seconds
        NaNthreshold: The lower cut-off as percentage of windows with NaNs values. This will be a threshold of denoting the EEGdata
        eligible for computing the band power or just handling them as NaNs. For example, if NaNthreshold = 0.5, this means that if
        the %windows with at least one NaN is greater than 50%, then the band power values won't be computed and instead will be replaced
        by NaNs values.
        overlap: the overlapping points expressed as proportion of the "winLength" parameter,
        for example for a 50% overlapping, this input parameter should be set as 0.5

    Returns: a matrix of dimensions channels x time points
    This will either a matrix of NaNs in case the proportion of chunks with at least 1 NaN value is greater than the NaNthreshold or
    a matrix with the original values for the chunks without NaNs and NaNs for the chunks that at least 1 NaN was found

    '''
    # select specific channel
    EEGchannel = EEGdata[which_channel]
    # time vector
    N = EEGchannel.shape[0]

    # window length in seconds*srate
    winlength = int(winLength*srate)

    # number of points to overlap
    nOverlap = np.round(winlength * overlap)

    # window onset times
    winOnsets = np.arange(0,int(N-winlength),int(winlength-nOverlap))

    # Count all chunks/windows of the data where
    # at least 1 NaN occured
    winCountNaN = 0

    # Number of windows/chunks
    Nwin = len(winOnsets)

    # loop over all windows
    for wi in range(0,len(winOnsets)):

        # get a chunk of data from this time window
        datachunk = EEGchannel[winOnsets[wi]:winOnsets[wi]+winlength ]

        # Count the number of NaNs in the datachunk
        NaNsum = np.sum(np.isnan(datachunk))

        # If there is at least 1 NaN value (even in one channel only)
        # then the window will be denoted as NaN
        if NaNsum >= 1:
            # Count the number of all windows with at least 1 NaN value (at least in one channel)
            winCountNaN = winCountNaN + 1

    if winCountNaN/Nwin > NaNthreshold:
        message = "Fail"
    else:
        message = "Pass"
    return message
