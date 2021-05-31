import os
from os import path, listdir


def move_files(dir_path, new_path):
    if path.isdir(dir_path) and path.isdir(new_path):
        if dir_path == new_path:
            return True
        for files in listdir(dir_path):
            os.rename(
                f"{dir_path}/{files}",
                f"{new_path}/{files}",
            )
        os.rmdir(dir_path)
        return True
    return False
