import numpy as np
from scipy import signal
from scipy.signal import iirfilter
from scipy.signal import lfilter

def Implement_Notch_Filter(fs: float, band: list, freq: float, ripple: float, order: int, filter_type: str, data: np.array):
    r"""

    Args:
        fs: frequency sampling
        band: the bandwidth around the center-line frequency that you wish to filter
        freq: the center - line frequency to be filtered
        ripple: the maximum pass-band ripple that is allowed in db
        order: the filter order.  For FIR notch filters this is best set to 2 or 3,
         IIR filters are best suited for high values of order.
        filter_type: the type of the filter; 'butter', 'bessel', 'cheby1', 'cheby2', 'ellip'
        data: the data to be filtered

    Returns:
        np.array: the filtered data
    """
    nyq = fs/2.0
    low = freq - band/2.0
    high = freq + band/2.0
    low = low/nyq
    high = high/nyq
    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop', analog=False, ftype=filter_type)
    filtered_data = lfilter(b, a, data)
    return filtered_data

def iirnotch_filter(fs, notch_frequency, quality_factor, data):
    r"""

    Args:
        fs: frequency sampling, in Hz
        notch_freq: the center-line frequency to be filtered
        quality_factor: the quality factor. see details in scipy.signal.iirnotch()
        data: signal the filtered will be applied

    Returns:
        np.array: signal after applying the filter
    """

    b_notch, a_notch = signal.iirnotch(notch_frequency, quality_factor, fs)

    # apply notch filter to signal
    data_notched = signal.filtfilt(b_notch, a_notch, data)

    return data_notched

# freq, h = signal.freqz(b_notch, a_notch, fs = srate)
# plt.figure('filter')
# plt.plot( freq, 20*np.log10(abs(h)))
### Example
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy import signal
# # Create/view notch filter
# samp_freq = 1000  # Sample frequency (Hz)
# notch_freq = 60.0  # Frequency to be removed from signal (Hz)
# quality_factor = 30.0  # Quality factor
# b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
# freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)
# plt.figure('filter')
# plt.plot( freq, 20*np.log10(abs(h)))
#
# # Create/view signal that is a mixture of two frequencies
# f1 = 17
# f2 = 60
# t = np.linspace(0.0, 1, 1_000)
# y_pure = np.sin(f1 * 2.0*np.pi*t) + np.sin(f2 * 2.0*np.pi*t)
# plt.figure('result')
# plt.subplot(211)
# plt.plot(t, y_pure, color = 'r')
#
# # apply notch filter to signal
# y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
#
# # plot notch-filtered version of signal
# plt.subplot(212)
# plt.plot(t, y_notched, color = 'r')