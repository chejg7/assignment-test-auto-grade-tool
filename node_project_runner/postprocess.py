from pathlib import Path
import shutil
from distutils.dir_util import copy_tree


def postprocess(path: Path, outer_project_path: Path):
    folder_name = str(outer_project_path).split("/")[-1]

    copy_tree(outer_project_path, f"node_project_runner/data/pass_data/{folder_name}")
    shutil.rmtree(outer_project_path)
