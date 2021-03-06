import os

# ROOT DIRECTORY
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

loc_output = "FILES"  # name for parent folder of all program folders
OUT_FILES_DIR = os.path.abspath(os.path.join(ROOT_DIR, loc_output))

loc_input = "IN_FILES"
IN_FILES = os.path.abspath(os.path.join(ROOT_DIR, loc_input))

# The location where edf files are
#IN_EDF_DATA = os.path.abspath(os.path.join("/data1"))
IN_EDF_DATA = os.path.abspath(os.path.join("D:"))


# The location where memmap temporary files are stored
DATA_TEMP_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "DATA_TEMP"))

# Raw data extracted
IN_RAW_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "RAW_DATA"))

# location where iEEG channels are located for each subject
IN_CHANNELS = os.path.abspath(os.path.join(IN_FILES, "CHANNEL_LIST"))

# Include here the labels that are fault edf files
error_edfs = ["1"]  # channels labels appear in error edfs

# Lower acceptable threshold for the number of channels in edf files
min_n_Chan = 5

# location where start and end times for segments and fs saved
RAW_INFO_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "RAW_INFO"))

# location where EDF information is written to
EDF_INFO_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "EDF_INFO"))

# location where Plots for Detecting Bad channels are located for each subject
PLOTS_BAD_CHANNELS_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "PLOTS_BAD_CHANNELS"))
#
# location where bandpower files will be saved
BAND_POWER_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "BP_EXTRACTED"))

# location where bandpower files are concatenated
BAND_POWER_CONCAT_DIR = os.path.abspath(os.path.join(OUT_FILES_DIR, "BP_EXTRACTED_CONCAT"))

# setup directories
directories = [constant for constant in dir() if "_DIR" in constant]
for dir_name in directories:
    dir_location = globals()[dir_name]
    if not os.path.exists(dir_location):
        print("Setting up directory for {} at {}".format(dir_name, dir_location))
    os.makedirs(dir_location, exist_ok=True)
