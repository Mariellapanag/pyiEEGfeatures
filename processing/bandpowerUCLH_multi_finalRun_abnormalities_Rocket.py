# Python module
import multiprocessing
import time
import scipy.io as sio

# internal modules
from pyiEEGfeatures.artefactsMetrics import *
from pyiEEGfeatures.Welch_with_NaNs_abnormalities import *
from pyEDFieeg.edfSegmentsiEEGSimple import *
import paths

def bandpower_process(EEGdata, fs, badch_indx):

    # Define EEG bands - those where used for SWEC data processing
    frange_bands = {'Delta': (1, 4),
                    'Theta': (4, 8),
                    'Alpha': (8, 13),
                    'Beta': (13, 30),
                    'Gamma1': (30, 47.5),
                    'Gamma2': (52.5, 57.5),
                    'Gamma3': (62.5, 77.5)
                    }

    butter_cutoff = [0.5, 80]

    butter_order = 2 # The 4th order of the (IIR) Butterworth filter, bandpass filter,
    #because this filter is forward-backward

    # this was used for SWEC data processing
    winLength = 2  # The window length in seconds for the Welch's method
    # this was used for SWEC data processing
    overlap = 0  # The percentage of overlapping to be performed in the windowing method

    notch = True
    #base_notch = 50 # 50Hz for the UCLH and GLAS data, while for the Canine data is 60Hz
    # THIS NEEDS TO BE SPECIDIED BY THE USER
    notch_freq = 50.0 # remove line noise and its harmonics

    quality_factor = 35
    NaNthreshold = 0

    print("Computing band power for this segment of data")
    list_all = EEG_Python_Welch_allChannels_abnormalities(EEGdata, badch_indx, fs, frange_bands,
                                            winLength, butter_cutoff, butter_order, overlap, notch,
                                            notch_freq, quality_factor, NaNthreshold)
    super_list = list_all["all_bp"]
    return super_list


subject_list = ["931", "934", "999", "1163", "1200"]

subject = ss

#subject = subject_list[0]
# This subject is used for test purposes
# subject = "909"

# Set the root directory for patient
root = os.path.join(paths.IN_EDF_DATA, subject)

raw_info_path = os.path.join(paths.RAW_INFO_DIR, subject)
raw_info = sio.loadmat(os.path.join(raw_info_path, "rawInfo_{}.mat".format(subject)))

# The channels to keep; these are the ones that are included in the list and in at least one edf file.
# The final channels included in the raw data
channelsKeep = list(raw_info["channelsKeep"])

# The final fs
fs = raw_info["fs"][0][0]

# The path where the raw data are
raw_data_path = os.path.join(paths.IN_RAW_DIR, subject)

# Read the list of files exist in RAW_DATA_DIR
raw_files = os.listdir(raw_data_path)

#edf_files_sorted = sorted(edf_files, key = lambda x: int(x.split("_")[2].split(".")[0]))[1:50]

z_threshold = 3 # if z-score is above 3 or below -3 then the channel is flagged as outlier/bad

bp_path = os.path.join(paths.BAND_POWER_DIR, subject)
os.makedirs(bp_path, exist_ok=True)


# Go and read the raw data
def process_file(mat_file):

    print("Processing:{}".format(mat_file))
    raw_data_path = os.path.join(paths.IN_RAW_DIR, subject)

    bp_path = os.path.join(paths.BAND_POWER_DIR, subject)

    raw_file = os.path.join(raw_data_path, mat_file)

    iEEGraw_data = sio.loadmat(raw_file)["EEG"]

    # Compute amplitude range for every 30s windows
    ampl_range_all = amplrange_axis1(iEEGraw_data)

    # standradise each 30s window amplitude ranges across channels (range - mean(range of all channels))/std(range of all channels)
    ampl_range_all_stand = standardise(ampl_range_all)

    bad_ch_ind = [i for i,v in enumerate(ampl_range_all_stand) if abs(v) > z_threshold]

    bp_computed = bandpower_process(iEEGraw_data, fs, bad_ch_ind)

    idd = int(mat_file.split("raw_")[1].split(".mat")[0])

    sio.savemat(os.path.join(bp_path, "BPall_P{}_{}.mat".format(subject, idd)), bp_computed, do_compression = True)



if __name__ == '__main__':

    pool = multiprocessing.Pool(8)
    start = time.time()

    for file in raw_files:
        pool.apply_async(process_file, [file])

    pool.close()
    pool.join()

    print("\n job done!!: {}".format(time.time()-start))




