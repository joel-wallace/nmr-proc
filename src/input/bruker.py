import os, re

def map_nmr_directory(directory):
    directories = []
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        if os.path.isdir(full_path) and name.isdigit():
            data_file = os.path.join(full_path, "pdata", "1", "1r")
            if os.path.isfile(data_file):
                nucleus = get_dir_nucleus(full_path)
                if nucleus == "1H":
                    directories.append({"name": name, "type": "1H"})
                elif nucleus == "19F":
                    directories.append({"name": name, "type": "19F"})
            else:
                directories.append({"name": name, "type": None})
    return directories

def get_dir_nucleus(directory):
    acqus_path = os.path.join(directory, "acqus")
    with open(acqus_path, 'r') as file:
        for line in file:
            if line.startswith("##$NUC1="):
                match = re.search(r'<([^>]+)>', line)
                if match:
                    return match.group(1)
    return None  # If not found