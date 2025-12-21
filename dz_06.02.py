import sys
import os

DIRS = {
    'Images': ('.jpg', '.png'),
    'Documents': ('.pdf', '.docx'),
    'Archives': ('.zip',)
    }
OTHER_DIR = 'Other'
os.chdir(sys.argv[1])
files = tuple(file for file in os.listdir() if os.path.isfile(file))
ext_to_dir = {}
for dir_name, dir_exts in DIRS.items():
    os.makedirs(dir_name, exist_ok=True)
    for ext in dir_exts:
        ext_to_dir[ext] = dir_name
os.makedirs(OTHER_DIR, exist_ok=True)
for file in files:
    file_dir = ext_to_dir.get(os.path.splitext(file)[1], OTHER_DIR)
    os.rename(file, os.path.join(file_dir, file))