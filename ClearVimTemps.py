import os

####
# for windows the temp files end with '~'
# for linux, uncomment the line below

# get file directory (that is the dir to be traversed)
file_dir = os.path.dirname(os.path.realpath(__file__))

for root, dirs, files in os.walk(file_dir):
    for filename in files:
        if filename.endswith("~") and filename[:-1] in files:  # windows version
        # if filename.startswith(".") and filename[1:] in files:  # linux version
            full_file_path = os.path.join(root, filename)
            try:
                os.remove(full_file_path)
                print(full_file_path)
            except Exception as e:
                print("!!! {} error while deleting {}".format(e, full_file_path))
        else:
            print("!!! Found temp file {} with no main file!".format(full_file_path))
