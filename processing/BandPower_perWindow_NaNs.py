"""Script for computing band power on UCLH/GLAS subjects"""

# Python module
import json
import seaborn as sns
import scipy.io as sio

# internal modules
from pyiEEGfeatures.artefactsMetrics import *
from pyiEEGfeatures.Welch_with_NaNs import *
from pyEDFieeg.edfSegmentsiEEGSimple import *
import paths


sta = 0
sto = 10

def bandpower_process(EEGdata, fs, badch_indx):

    # Define EEG bands - those where used for SWEC data processing
    frange_bands = {'Delta': (1, 4),
                    'Theta': (4, 8),
                    'Alpha': (8, 13),
                    'Beta': (13, 30),
                    'Gamma': (30, 80),
                    'hGamma': (80, 120)}

    butter_cutoff = [0.5, 120]

    butter_order = 2 # The 4th order of the (IIR) Butterworth filter, bandpass filter,
    #because this filter is forward-backward

    # this was used for SWEC data processing
    winLength = 3  # The window length in seconds for the Welch's method
    # this was used for SWEC data processing
    overlap = 0  # The percentage of overlapping to be performed in the windowing method

    notch = True
    base_notch = 50 # 50Hz for the UCLH and GLAS data, while for the Canine data is 60Hz
    # THIS NEEDS TO BE SPECIDIED BY THE USER
    notch_freq = [50.0, 100.0] # remove line noise and its harmonics

    quality_factor = 30.0
    NaNthreshold = 0.5

    print("Computing band power for this segment of data")
    list_all = EEG_Python_Welch_allChannels(EEGdata, badch_indx, fs, frange_bands,
                                            winLength, butter_cutoff, butter_order, overlap, notch,
                                            notch_freq, quality_factor, NaNthreshold)
    super_list = list_all["all_bp"]
    return super_list


subject_list = ["1106", "1109", "1149", "1163", "1182", "851",
                "934", "95", "999", "GLAS040", "GLAS041", "GLAS044", "GLAS047",
                "1005", "1200", "1211", "1379", "1395", "1167"]

#subject = subject_list[0]
# This subject is used for test purposes
subject = "909"

# Set the root directory for patient
root = os.path.join(paths.IN_EDF_DATA, subject)

error_edfs = paths.error_edfs # channels labels appear in error edfs
min_n_Chan = paths.min_n_Chan # the minimum threshold of the number of channels needed to be included in the edf file

# iEEG channels for each subject provided in json files (or mat file). This mat files include the iEEG channels
# having excluded the Heart Rate Channels
# EEG_channels = sio.loadmat(os.path.join(paths.iEEG_channels, subject, "channels.mat"))
EEG_channel_path = os.path.join(paths.IN_CHANNELS, "{}.json".format(subject))
with open(EEG_channel_path) as json_file:
    Channels_json = json.load(json_file)
    print(Channels_json)
EEG_channel_list = [element['name'] for element in Channels_json]

# Get info about edf files and a list with the final paths pointed to the edf files to be used for the analysis
[f_paths_clean, f_path_list_excluded, f_path_list_checkChanNotInList, f_paths, edf_chan] = clean_edf_paths(root = root,
                                                                                                           error_edfs = error_edfs,
                                                                                                           channel_list = EEG_channel_list,
                                                                                                           min_n_Chan = min_n_Chan)
edfs_info = get_EDFs_info(root = root,
                          edf_path_list = f_paths_clean,
                          channel_list = EEG_channel_list)

unique_channels_across_allEDFs = nChannelsConsistency(root = root,
                                                      edf_path_list = f_paths_clean, # we are using the list with the final edf files
                                                      channel_list = EEG_channel_list)

unique_channels_across_allEDFs.sort()
# The channels to keep; these are the ones that are included in the list and in at least one edf file.
# If a channel is not included in en edf file will be filled with NaN values.
channelsKeep = unique_channels_across_allEDFs.copy()

# Compute minimum sample rate across edf files and channels
fs_target = sampleRateConsistency(root = root,
                                  edf_path_list = f_paths_clean,
                                  channel_list = EEG_channel_list)

# EDF paths
edf_fpaths = edfs_info["fpath"]

# Find the length of the recording based on the edfs_info
# edf start and stop times for all edf files
edf_start_time = edfs_info["start_time"]
edf_stop_time = edfs_info["end_time"]
# Identify the start and end time of the entire recording based on the edf files
start_EDFs_global = sorted(edf_start_time)[0]
end_EDFs_global = sorted(edf_stop_time)[-1]

# Split the range into start points of length 30s
#n_win = np.floor(((end_EDFs_global - start_EDFs_global)+datetime.timedelta(seconds = 1)).seconds/30)

# window length in seconds
winsec = 30
overlap = 0
winlength = int(winsec)

def datetime_range(start, end, delta):
    current = start
    while current < (end-delta):
        # this controls in the case of the last window going over the last recorded period.
        yield current
        current += delta

"""Check all segments within the recording"""
# These are the start points of all the starting points of the windows
t_start = [dt for dt in
           datetime_range(start_EDFs_global, end_EDFs_global,
                          datetime.timedelta(seconds=30))]

t_stop = [tt + datetime.timedelta(seconds=winsec-1) for tt in t_start]

# Checking all segments
tt_start = t_start[sta:sto]
tt_stop = t_stop[sta:sto]

iEEGraw_data = edfExportSegieeg_A(edfs_info = edfs_info, channelsKeep = channelsKeep, t_start = tt_start, t_stop = tt_stop, fs_target = fs_target)

# Start working on extracting band power
fs = fs_target


# Compute amplitude range for every 30s windows
ampl_range_all = [amplrange_axis1(dd) for dd in iEEGraw_data]

# i = 0
# for ii in ampl_range_all:
#
#     rr = standardise(ii)
#     print(i)
#     print(rr)
#     i = i+1
# standradise each 30s window amplitude ranges across channels (range - mean(range of all channels))/std(range of all channels)
ampl_range_all_stand = [standardise(ss) for ss in ampl_range_all]

ampl_range_stand_conc = np.hstack(ampl_range_all_stand)

# Check all standardise values obtained from all 30s windows amplitude ranges
plot_bad_path = os.path.join(paths.PLOTS_BAD_CHANNELS_DIR, subject)
os.makedirs(plot_bad_path, exist_ok=True)

sns.set_style('whitegrid')
sns.kdeplot(np.array(ampl_range_stand_conc), bw=0.5)
plt.savefig(os.path.join(plot_bad_path, 'Ampl_range_across_all.pdf'))

z_threshold = 3 # if z-score is above 3 or below -3 then the channel is flagged as outlier/bad

i=0
bad_ch_ind_allw = list()
for ww in ampl_range_all_stand:
    print(i)
    print(ww)
    bad_ch_ind = [i for i,v in enumerate(ww) if abs(v) > 3]
    bad_ch_ind_allw.append(bad_ch_ind)
    i = i+1


data_bp_list = list()
for bb in range(len(iEEGraw_data)):
    data_bp_list.append(bandpower_process(iEEGraw_data[bb], fs, bad_ch_ind_allw[bb]))


super_dict = {}
for d in data_bp_list:
    for k,v in d.items():
        super_dict.setdefault(k,[]).append(v)
        #append(v)

del data_bp_list

for k,v in super_dict.items():
    # print(k,v)
    super_dict[k] = np.vstack(v)

super_dict_ch = {"super_dict": super_dict, "channels": channelsKeep, "fs": fs}

del super_dict, channelsKeep

bp_path = os.path.join(paths.BAND_POWER_DIR, subject)
os.makedirs(bp_path)

sio.savemat(os.path.join(bp_path, "BPall_P{}.mat".format(subject)), super_dict_ch)
BPdata = sio.loadmat(os.path.join(bp_path, "BPall_P{}.mat".format(subject)))

