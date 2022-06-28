# this script needs to exist
# due to an inconsistency in the way that
# config files are written
import sys

config_file_loc = sys.argv[1]

config_file = open(config_file_loc, "r")
lines = config_file.readlines()
for (i, line) in enumerate(lines):
    if "datapath = " in line:
        mod = line.split("/")
        mod[-2] = mod[-2]+"000"
        line = "/".join(mod)
        lines[i] = line

config_file = open(config_file_loc, "w")
config_file.writelines(lines)
config_file.close()

