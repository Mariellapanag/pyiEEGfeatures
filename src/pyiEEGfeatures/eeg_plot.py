import numpy as np
import matplotlib.pyplot as plt

def plotEEG(data, n_channels, ch_names, n_TimePoints, srate):
    # Plot EEG
    sampling_points = data.shape[1]  # Sampling points that correspond to the seconds selected
    # Identify seconds
    seconds = int(sampling_points/srate)
    eegdata = data.T[0:(sampling_points),]
    # set up time and separator to add space between channels
    time = np.linspace(0.0,seconds,sampling_points)
    sep = np.max(np.abs(eegdata[~np.isnan(eegdata)]))*np.arange(n_channels-1,-1,-1)

    # plot it!
    fig = plt.figure(figsize=(18,12))
    ax = fig.add_subplot(1,1,1)
    for ch in range(n_channels):
        # indx_nan = np.isnan(eegdata[:,ch])
        ax.plot(time, eegdata[:, ch]+sep[ch])
        ax.set_xlim([0, time.max()])
        # ax.plot(time[~indx_nan], eegdata[~indx_nan, ch]+sep[ch])
        # ax.plot(time[indx_nan], eegdata[indx_nan, ch]+sep[ch], color = "lightgrey", label = "NaN")
        # # # for y in time[indx_nan, ch]:
        #     ax.axvline(y, ls="--")
    # label_format = '{:,.0f}'
    ax.set_yticks(sep)
    ax.set_yticklabels(ch_names)
    ax.axis('tight')
    ax.set_title("#Time points:{}".format( n_TimePoints))
    return fig
