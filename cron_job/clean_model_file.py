import os
import time
import shutil

CONFIG_TIME_THRESHOLD = 24 # hours
CONFIG_MODEL_PATH = 'REST_FindSim/media/files/model'

# Check whether the dir is an empty one.
def check_dir_empty(path):
    if os.listdir(path) == []:
        return True
    return False

# For debuging
# Print info of directory
def print_dir_info(root, dirs, files):
    print('-------'+root)
    print(os.listdir(root))
    print('{')
    print(dirs)
    print(files)
    print('}')

def main():
    # Model file existing longer than this time period can be removed
    # if downloaded by users.
    time_threshold = CONFIG_TIME_THRESHOLD*3600.0

    # 1.Set Path to model files
    base_dir = os.path.realpath(__file__)
    base_dir = os.path.split(base_dir)[0]
    cnt = 0
    l = len(base_dir)
    while base_dir[l-1-cnt] != '/':
        cnt += 1
    base_dir = base_dir[:l-cnt-1]
    base_dir = os.path.join(base_dir, CONFIG_MODEL_PATH)

    # 2.Search for all the model files
    # Delete model files that are:
    # i. Existing for enough time
    # ii. Has been downloaded at least once
    for root, dirs, files in os.walk(base_dir, topdown = False):
        flag = False
        noMd = True
        # Check all files in the dir, find a model file that should be removed:
        for file in files:
            if file.split('.')[-1] != 'md':
                fstat = os.stat(os.path.join(root,file))
                if fstat.st_ctime != fstat.st_atime:
                    if time.time() - fstat.st_ctime > time_threshold:
                        flag = True
            else:
                # if there's .md file, don't remove this dir
                noMd = False

        # Remove the dir recursively if  we think it should be removed:
        if flag and noMd:
            print('Remove: '+root)
            shutil.rmtree(root)

    # 3.Delete empty directory
    for root, dirs, files in os.walk(base_dir, topdown = False):
        print_dir_info(root, dirs, files)
        if check_dir_empty(root):
            shutil.rmtree(root)


if __name__ == '__main__':
    main()
