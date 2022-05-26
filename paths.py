import os

# ROOT DIRECTORY
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

loc_output = "FILES" # name for parent folder of all program folders
ALL_FILES_DIR = os.path.abspath(os.path.join(ROOT_DIR, loc_output))

loc_input = "IN_FILES"
IN_FILES = os.path.abspath(os.path.join(ROOT_DIR, loc_input))

# location where iEEG raw data are located for each subject
IN_DATA = os.path.abspath(os.path.join(IN_FILES, "DATA"))

# location where iEEG channels are located for each subject
IN_CHANNELS = os.path.abspath(os.path.join(IN_FILES, "CHANNEL_LIST"))

# # location where Plots for raw data seizures will be located
# PLOT_SEIZURES_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "PLOTS_SEIZURES"))
#
# # location where Plots for Detecting Bad channels are located for each subject
# PLOTS_BAD_CHANNELS_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "PLOTS_BAD_CHANNELS"))
#
# # location where EDF information is written to
# EDF_INFO_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "EDF_INFO"))
#
# # location where collated EDF is written to
# EDF_OUT_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "EDF_OUT"))
#
# # location where memmaps for channels (if using) are stored temporarily during runtime
# # otherwise, memory is used
# CHANNELS_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "CHANNELS"))
#
# # location segments of the collated data are written to
# SEGMENT_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "SEGMENTS"))
#
# # location of scripts results
# SCRIPTS_OUT_DIR = os.path.abspath(os.path.join(ALL_FILES_DIR, "SCRIPTS_OUT"))

# setup directories
directories = [constant for constant in dir() if "_DIR" in constant]
for dir_name in directories:
    dir_location = globals()[dir_name]
    if not os.path.exists(dir_location):
        print("Setting up directory for {} at {}".format(dir_name, dir_location))
    os.makedirs(dir_location, exist_ok=True)

