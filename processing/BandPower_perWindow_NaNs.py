import scipy.io as sio
from paths import *
from funcs.interplolate_outliers import *
from funcs.Welch_with_NaNs import *




def band_power_process(data_mat, boundaries, fs, indices_keep):

    raw_mat_list_outliers = interpolate_outliers(data_mat[indices_keep], boundaries)
    del data_mat
    print("Detecting outliers and interpolating with cubic function ")
    list_all = EEG_Python_Welch_allChannels(raw_mat_list_outliers, fs)

    super_list = list_all["all_bp"]

    return super_list


def process():

    dataset_names = ["I004_A0001_D001", "I004_A0002_D001", "I004_A0003_D001"]
    subject = dataset_names[0]

    raw_subj = os.path.join(, subject)
    raw_files = os.listdir(raw_subj)
    raw_files_sorted = sorted(raw_files, key = lambda x: int(x.split("_")[1].split(".")[0]))
    raw_subj_info = os.path.join(ROOT_DIR, "raw_data_info", subject)
    raw_info_total_time = sio.loadmat(os.path.join(raw_subj_info, "info_raw_{}.mat".format(subject)))["n_total_time"]

    channels = sio.loadmat(os.path.join(raw_subj_info, "info_raw_{}.mat".format(subject)))["channels"].tolist()
    fs = sio.loadmat(os.path.join(raw_subj_info, "info_raw_{}.mat".format(subject)))["fs"][0][0]

    N = raw_info_total_time
    winlength = int(30*fs)
    winOnsets = np.arange(0, int(N-winlength), winlength)

    boundaries_path = os.path.join(ROOT_DIR, "info", "Boundaries")

    output_folder = os.path.join(ROOT_DIR, "mat_data", subject)
    os.makedirs ( output_folder, exist_ok=True )

    seizures_path = os.path.join(ROOT_DIR, "info")

    sz_info = sio.loadmat(os.path.join(seizures_path, "seizure_info_{}.mat".format(subject)))

    bad_channels = sz_info["bad_channels"]
    # bad_channels = np.array("LEFT_01")
    # Detecting the outliers and interpolating them based on cubic interpolation
    boundaries = sio.loadmat(os.path.join(boundaries_path, "boundaries_{}.mat".format(subject)))
    indices_keep = [i for i in np.arange(0, len(channels))]
    # Drop bad channels if any
    if bad_channels.size != 0:
        if bad_channels.size == 1:
            b_chan = bad_channels
        else:
            b_chan = np.concatenate(bad_channels[0])
        indices_keep = [i for i in np.arange(0, len(channels)) if channels[i] not in b_chan]

        # Identify the index of the bad channels
        index_excl = [i for i in np.arange(0, len(channels)) if channels[i] in b_chan]
        UPPER_last = np.delete(boundaries["UPPER"], index_excl, axis=1)
        LOWER_last = np.delete(boundaries["LOWER"], index_excl, axis=1)
        boundaries = {"UPPER": UPPER_last, "LOWER": LOWER_last}
        # exclude bad channels from channel names
        channels = np.array(channels)[indices_keep].tolist()

    N = len(winOnsets)
    #N = len(raw_files_sorted)
    print(N)
    winlength = np.arange(0, N, 24*120)
    print(winlength)
    [a,b] = np.divmod(N, 24*120)
    print("a:{}".format(a))
    print("b:{}".format(b))
    id=1
    print(id)
    start = winlength[0]
    print("start:{}".format(start))
    end = winlength[1]
    print("end:{}".format(end))
    data_mat_list = [np.load(os.path.join(raw_subj, raw)) for raw in raw_files_sorted[0:4]]

    data_mat_list = [band_power_process(raw_mat, boundaries, fs, indices_keep) for raw_mat in data_mat_list]

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

if __name__ == "__main__":
    process()

