from pyiEEGfeatures.NaNControl import NaNControl
from pyiEEGfeatures.Pyweltch_method_abnormalities import EEG_PyWelch_abnormalities
import numpy as np

"""
Welch method for 6 main frequency bands applied to EEG/iEEG data
Combine all preprocessing steps

Version 0.1 Date: 30/12/2020
"""

'''Test data'''
#
# dat = raw_df_list[1]
# example_data = { "srate": srate, "EEGdata": dat }
# with open(os.path.join("F:\GitHub", "ieegpy-master", "results","example.pickle"),"wb") as f:
#     pickle.dump( example_data, f)
#
# # srate = srate[0]
# EEGdata = np.transpose(dat).values
# which_channel = 0
# winLength = 1.5
# overlap = 0.5
# NaNthreshold = 0.5

# EEGdata = np.transpose(raw_df_list_NaNC[0]).values

def EEG_Python_Welch_allChannels_abnormalities(EEGdata, badch_indx, srate, frange_bands, winLength, butter_cutoff, butter_order, overlap, notch, notch_freq, quality_factor, NaNthreshold):
    '''

    Args:
        EEGdata: EEG data in the form of 2d numpy array (matrix) with dimensions channels x time points
        srate: the sampling frequency, in Hz

    Returns: a dictionary of 3 elements:
    1. all_bp: a dictionary with key elements the band power for each frequency band. Each frequency band contains an 1d array
    with values of power in this frequency band for all channels. In case the initial data were flagged as NaNs "all_bp" will contain only NaNs
    but structured as a dictionary similar to the one described above.
    2. freqs: A matrix where each row depicts to the vector of frequencies that the welch method was computed for one channel.
    Each row corresponds to one channel.
    3. psds: A matrix where each row depicts to the vector of power spectral density values based on Welch method for one channel.
    Each row corresponds to one channel.
    '''

    # Define EEG bands
    # frange_bands = {'Delta': (1, 4),
    #                 'Theta': (4, 8),
    #                 'Alpha': (8, 13),
    #                 'Beta': (13, 30),
    #                 'Gamma': (30, 80),
    #                 'hGamma': (80, 120)}

    # order = 4 # The order of the (IIR) Butterworth filter, bandpass filter
    # winLength = 1.5  # The window length in seconds for the Welch's method
    # overlap = 1 / 2  # The percentage of overlapping to be performed in the windowing method
    n_channels = EEGdata.shape[0]
    # notch = True
    # notch_freq = [60.0, 120.0] # remove line noise and its harmonics
    # quality_factor = 30.0
    # NaNthreshold = 0.5

    # Check if all values are NaNs
    if np.sum(np.isnan(EEGdata).all()) == 1:
        init_array = np.zeros(n_channels, dtype = np.float32)
        all_bp = {"Delta": np.full_like(init_array, np.nan), "Theta": np.full_like(init_array, np.nan),
                  "Alpha": np.full_like(init_array, np.nan), "Beta": np.full_like(init_array, np.nan),
                  "Gamma": np.full_like(init_array, np.nan)}
        freqs = np.full_like(init_array, np.nan)
        psds = np.full_like(init_array, np.nan)

    else:
        # if there are bad channels detected we exclude them form the common average calculation
        if (len(badch_indx) != 0):
            # Referencing using common average reference
            keeprows = [ii for ii in range(EEGdata.shape[0]) if ii not in badch_indx]
            mean = np.nanmean(EEGdata[keeprows,:], axis=0)
            data_CA = EEGdata - mean[np.newaxis,:]
        else:
            # Referencing using common average reference
            mean = np.nanmean(EEGdata, axis=0)
            data_CA = EEGdata - mean[np.newaxis,:]

        freqb_channels_bp = np.zeros((len(frange_bands), n_channels), dtype = np.float32)

        freqlist = []
        eegpowW = []
        for i in range(0, n_channels):
            which_channel = i
            # Control checking for NaNs
            message = NaNControl(data_CA, which_channel, srate, winLength, NaNthreshold, overlap)
            if(message == "Pass"):
                temp_run = EEG_PyWelch_abnormalities(data_CA, srate, which_channel,
                                            butter_cutoff, butter_order, frange_bands,
                                            winLength, overlap, notch, notch_freq, quality_factor)
                freqb_channels_bp[:,i] = temp_run[0]
                freqlist.append(temp_run[1])
                eegpowW.append(temp_run[2])
            else:
                # window length in seconds*srate
                winlength = int(winLength*srate)
                # vector of frequencies, Hz
                srate_new = 200
                Nyquist = srate_new/2
                freqvec = np.linspace(0,Nyquist,int(np.floor(winlength/2)+1))
                init_array = np.zeros(len(frange_bands), dtype = np.float32)
                freqb_channels_bp[:,i] = np.full_like(init_array, np.nan)

                initfreq_array = np.zeros(len(freqvec), dtype = np.float32)
                freqlist.append(np.full_like(initfreq_array, np.nan))
                eegpowW.append(np.full_like(initfreq_array, np.nan))

        all_bp = {"Delta": freqb_channels_bp[0,:], "Theta": freqb_channels_bp[1,:], "Alpha": freqb_channels_bp[2,:], "Beta": freqb_channels_bp[3,:],
                  "Gamma": freqb_channels_bp[4,:]}

        freqs = np.vstack(freqlist)
        psds = np.vstack(eegpowW)

    return {"all_bp": all_bp, "freqs": freqs, "psds": psds}
