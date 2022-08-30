from pathlib import Path
import shutil
from distutils.dir_util import copy_tree


def postprocess(project_folder_relative_path: Path, is_pass: bool):
    folder_name = str(project_folder_relative_path).split("/")[-1]
    if is_pass == True:
        copy_tree(
            project_folder_relative_path,
            f"spring_project_runner/data/pass_data/{folder_name}",
        )
    elif is_pass == False:
        copy_tree(
            project_folder_relative_path,
            f"spring_project_runner/data/fail_data/{folder_name}",
        )
    shutil.rmtree(project_folder_relative_path)
