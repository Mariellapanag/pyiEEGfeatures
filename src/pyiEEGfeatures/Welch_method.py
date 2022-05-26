import numpy as np
import scipy.fftpack
from scipy.integrate import simps
from pyiEEGfeatures.IIR_notch_filter import *
from pyiEEGfeatures.FilterEEG import *

# EEGdata = data_CA
def EEG_Python_Welch(EEGdata, srate, which_channel, butter_cutoff, butter_order, frange_bands, winLength, overlap, notch, notch_freq, quality_factor):

    '''
    Args:
        EEGdata: matrix of EEG data, dimensions: channels x time points
        srate: sampling frequency, in Hz
        which_channel: an integer number of the row selected. The rows corresponds to the recorded channels
        frange_bands: a dictionary of all the frequency bands where the power will be computed, for example
        frange_bands = {'Delta': (1, 4),
                    'Theta': (4, 8),
                    'Alpha': (8, 13),
                    'Beta': (13, 30),
                    'Gamma': (30, 80),
                    'hGamma': (80, 120)}
        winLength: the window length to split the data in seconds
        overlap: the overlapping points expressed as proportion of the "winLength" parameter,
        for example for a 50% overlapping, this input parameter should be set as 0.5
        notch: a boolean variable; True if notch filter will be applied and False if not
        notch_freq: the center-line frequency/ies to be filtered, for example [60,120]
        quality_factor: the quality factor. see details in scipy.signal.iirnotch()

    Returns: a list of 3 elements:
    1. all_bp: a dictionary with key elements the band power for each frequency band. Each frequency band contains an 1d array
    with values of power in this frequency band for one selected channel (which_channel).
    2. freqs: A vector of frequencies that the welch method was computed for the selected channel.
    3. psds: A vector of power spectral density values based on Welch method for one channel.

    '''

    # Data for the "which_channel" channel
    EEGdata_Channel = EEGdata[which_channel]

    # time vector
    N = EEGdata_Channel.shape[0]
    timevec = np.arange(0,N)/srate

    # window length in seconds*srate
    winlength = int(winLength*srate)

    # number of points to overlap
    nOverlap = np.round(winlength * overlap)

    # window onset times
    winOnsets = np.arange(0,int(N-winlength),int(winlength-nOverlap))

    # vector of frequencies, Hz
    Nyquist = srate/2
    freqvec = np.linspace(0,Nyquist,int(np.floor(winlength/2)+1))

    # Hanning window for reducing edge effect
    hannw = .5 - np.cos(2*np.pi*np.linspace(0,1,int(winlength)))/2

    # initialize the power matrix (windows x frequencies)
    eegpowW = np.zeros(len(freqvec))

    #count the number of window that included in the calculation
    Countwin = 0
    # loop over frequencies
    for wi in range(0,len(winOnsets)):
        # get a chunk of data from this time window
        datachunk = EEGdata_Channel[ winOnsets[wi]:winOnsets[wi]+winlength]
        if (np.sum(np.isnan(datachunk)) == 0):
            Countwin = Countwin + 1
            if notch == True:
                # Notch filter
                notched_data1 = iirnotch_filter(srate, notch_freq[0], quality_factor, datachunk)
                notched_data = iirnotch_filter(srate, notch_freq[1], quality_factor, notched_data1)
            else:
                notched_data = datachunk.copy()
            # Butterworth bandpass filter
            butter_filtered_data = FilterEEG_Channel(datachunk, butter_cutoff, srate,"bandpass", butter_order)

            # apply Hanning taper to data
            datachunk = butter_filtered_data * hannw

            # compute its power
            tmppow = np.abs(scipy.fftpack.fft(datachunk)/winlength)**2

            # enter into matrix
            eegpowW = eegpowW + tmppow[0:len(freqvec)]

    # divide by Countwin/ number of windows that were included in the calculation
    eegpowW = eegpowW / Countwin

    # Frequency resolution
    freq_res = freqvec[1] - freqvec[0]

    # Band frequencies and filtered data
    len_frange_bands = len(frange_bands)

    # initialise the spectral power density for each band overall
    psd_band = np.zeros(len_frange_bands)

    for band in range(0, len_frange_bands):
        # Get the values of the i element of the dictionary
        selected_frange = [element for element in frange_bands.values()]
        selected_frange = np.array(selected_frange[band])

        # Find closest indices of band in frequency vector
        idx_band = np.logical_and(freqvec >= selected_frange[0], freqvec <= selected_frange[1])

        # Integral approximation of the spectrum using Simpson's rule.
        bp = simps(eegpowW[idx_band], dx=freq_res)

        # Store the spectral density power for each band and each window into the matrix
        psd_band[band] = bp


    return [psd_band, freqvec, eegpowW]
