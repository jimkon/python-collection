import os
import subprocess
import sys
import argparse
import zipfile
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--reqs', type=str, default='requirements.txt')
parser.add_argument('-d', '--dest', type=str, default='.')
args = vars(parser.parse_args())


def install_package(package, dest_dir='.'):
    print(f"pip install {package} -t {dest_dir}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, '-t', dest_dir])


# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory#:~:text=some%20example%20code%3A-,import,-os%0Aimport%20zipfile
def zip_dir(path):
    with zipfile.ZipFile(f"{path}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '../../..')))


def delete_dir(folder_path):
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def zip_and_delete_file(file):
    if not os.path.exists(file):
        return False

    print(f"Zipping {file}...")
    zip_dir(file)
    print(f"Deleting {file}...")
    delete_dir(file)


def get_requirements(path):
    with open(path, 'r') as f:
        return f.read().split()


def separate_package_name(dependency):
    return dependency.split('==')[0]


def create_dir(dir_name):
    os.mkdir(dir_name)


def main():
    reqs_file = args['reqs']
    dest_dir = args['dest']
    print(f"Reading {reqs_file} file for requirements...")
    reqs = get_requirements(reqs_file)
    print(f"Installing {len(reqs)} packages into {dest_dir} directory...")
    for package in reqs:
        dir_name = separate_package_name(package)
        target_path = os.path.join(dest_dir, dir_name)
        install_package(package, target_path)
        zip_and_delete_file(os.path.join(dest_dir, dir_name))
    print("Done!!")


if __name__ == "__main__":
    main()