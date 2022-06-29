import numpy as np
import scipy.fftpack
from scipy.integrate import simps
from pyiEEGfeatures.IIR_notch_filter import *
from pyiEEGfeatures.FilterEEG import *
from pyEDFieeg.edfCollectionInfo import *

def EEG_PyWelch_abnormalities(EEGdata, srate, which_channel, butter_cutoff, butter_order, frange_bands, winLength, overlap, notch, notch_freq, quality_factor):

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

    # Get the non-NaN values
    partnonNaN = ~np.isnan(EEGdata_Channel)
    #partNaN = np.isnan(EEGdata_Channel)

    if notch == True:
        # Notch filter
        notched_data = iirnotch_filter(srate, notch_freq, quality_factor, EEGdata_Channel[partnonNaN])
    else:
        notched_data = EEGdata_Channel.copy()
    # Butterworth bandpass filter
    butter_filtered_data = FilterEEG_Channel(notched_data, butter_cutoff, srate, "bandpass", butter_order)

    srate_new = 200
    # Downsample the data to 200Hz
    downsampled_data = downsample_decimate(signal = butter_filtered_data, fs = srate, target_fs=srate_new, method = "fourier")
    ## The Welch's method will be applied to the filtered data from previous step
    freq, psds = scipy.signal.welch(downsampled_data, fs=srate_new, nperseg=winlength,
                                    noverlap=nOverlap, detrend=False)

    # Frequency resolution
    freq_res = freq[1] - freq[0]

    # Band frequencies and filtered data
    len_frange_bands = len(frange_bands)

    # initialise the spectral power density for each band overall
    len_frange_band_last = 5
    psd_band = np.zeros(len_frange_band_last)
    psd_band_tmp = np.zeros(len_frange_bands)

    for band in range(0, len_frange_bands):
        # Get the values of the i element of the dictionary
        selected_frange = [element for element in frange_bands.values()]
        selected_frange = np.array(selected_frange[band])

        # Find closest indices of band in frequency vector
        idx_band = np.logical_and(freq >= selected_frange[0], freq <= selected_frange[1])

        # Integral approximation of the spectrum using Simpson's rule.
        bp = simps(psds[idx_band], dx=freq_res)

        # Store the spectral density power for each band and each window into the matrix
        psd_band_tmp[band] = bp

    psd_band[0:4] = psd_band_tmp[0:4]
    psd_band[4:5] = np.sum(psd_band_tmp[4:])

    return [psd_band, freq, psds]
