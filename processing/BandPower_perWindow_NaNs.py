"""Script for computing band power on UCLH/GLAS subjects"""

# Python module
import json
import sklearn as sns

# internal modules
from pyiEEGfeatures.artefactsMetrics import *
from pyiEEGfeatures.Welch_with_NaNs import *
from pyEDFieeg.edfSegmentsiEEGSimple import *
import paths


subject_list = ["1106", "1109", "1149", "1163", "1182", "851",
                "934", "95", "999", "GLAS040", "GLAS041", "GLAS044", "GLAS047",
                "1005", "1200", "1211", "1379", "1395", "1167"]

subject = subject_list[0]

# Set the root directory for patient
root = os.path.join(paths.IN_EDF_DATA, subject)

corrupted_edf_paths = paths.corrupted_edfs[subject]

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
                                                                                                           corrupted_edf_paths = corrupted_edf_paths,
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
tt_start = t_start
tt_stop = t_stop

iEEGraw_data = edfExportSegieeg_A(edfs_info = edfs_info, channelsKeep = channelsKeep, t_start = tt_start, t_stop = tt_stop, fs_target = fs_target)

# Start working on extracting band power
fs = fs_target

# Define EEG bands - those where used for SWEC data processing
frange_bands = {'Delta': (1, 4),
                'Theta': (4, 8),
                'Alpha': (8, 13),
                'Beta': (13, 30),
                'Gamma': (30, 80),
                'hGamma': (80, 120)}

order = 4 # The order of the (IIR) Butterworth filter, bandpass filter
# this was used for SWEC data processing
winLength = 3  # The window length in seconds for the Welch's method
# this was used for SWEC data processing
overlap = 0  # The percentage of overlapping to be performed in the windowing method

notch = True
base_notch = 50
# THIS NEEDS TO BE SPECIDIED BY THE USER
notch_freq = [50.0, 100.0] # remove line noise and its harmonics

quality_factor = 30.0
NaNthreshold = 0.5


# Compute amplitude range for every 30s windows
ampl_range_all = [amplrange_axis1(dd) for dd in iEEGraw_data]
# standradise each 30s window amplitude ranges across channels (range - mean(range of all channels))/std(range of all channels)
ampl_range_all_stand = [standardise(ss) for ss in ampl_range_all]

# Check all standardise values obtained from all 30s windows amplitude ranges
sns.set_style('whitegrid')
sns.kdeplot(np.array(data), bw=0.5)



EEG_Python_Welch_allChannels(raw_data_list, fs)
data_mat_list = [band_power_process(raw_npy, boundaries, fs, indices_keep) for raw_npy in raw_files_sorted]

super_dict = {}
for d in data_mat_list:
    for k,v in d.items():
        super_dict.setdefault(k,[]).append(v)
        #append(v)

del data_mat_list

for k,v in super_dict.items():
    # print(k,v)
    super_dict[k] = np.vstack(v)

super_dict_ch = {"super_dict": super_dict, "channels": channels}
del super_dict, channels
sio.savemat(os.path.join(output_folder, "BPall_D{}.mat".format(id)), super_dict_ch)
BPdata = sio.loadmat(os.path.join(output_folder, "BPall_D{}.mat".format(id)))

