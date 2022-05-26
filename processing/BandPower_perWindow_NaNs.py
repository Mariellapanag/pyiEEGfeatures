import paths
import sklearn as sns
import pyiEEGfeatures.artefactsMetrics
from pyiEEGfeatures.Welch_with_NaNs import *

# Define EEG bands
frange_bands = {'Delta': (1, 4),
                'Theta': (4, 8),
                'Alpha': (8, 13),
                'Beta': (13, 30),
                'Gamma': (30, 80),
                'hGamma': (80, 120)}

order = 4 # The order of the (IIR) Butterworth filter, bandpass filter
winLength = 3  # The window length in seconds for the Welch's method
overlap = 0  # The percentage of overlapping to be performed in the windowing method
notch = True
notch_freq = [60.0, 120.0] # remove line noise and its harmonics
quality_factor = 30.0
NaNthreshold = 0.5

# fs = 399 # Dog data
# fs = 512 # subject 909

dataset_names = ["909", "I004_A0001_D001", "I004_A0002_D001", "I004_A0003_D001"]
subject = dataset_names[0]

raw_subj = os.path.join(paths.IN_DATA, subject)
# list of files within the DATA folder for this subject
raw_files = os.listdir(raw_subj)
# sort files based on the number included in their names
raw_files_sorted = sorted(raw_files, key = lambda x: int(x.split("_")[1].split(".")[0]))

raw_data_list = [np.load(os.path.join(raw_subj, raw)) for raw in raw_files_sorted[0:2]]

# Compute amplitude range for every 30s windows
ampl_range_all = [amplrange_axis1(dd) for dd in raw_data_list]
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

