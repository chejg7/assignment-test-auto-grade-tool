import logging
import os
from pathlib import Path
import subprocess
import shutil
import typing
from distutils.dir_util import copy_tree


from .constants import TEST_FILES_RELATIVE_PATH, RESOURCE_PATH

logger = logging.getLogger(__name__)


def unzip(zip_path: Path, destination: Path) -> Path:
    print(zip_path, destination)
    logger.debug("Preprocess: Unzipping..")
    if not zip_path.exists():
        raise FileNotFoundError("Cannot find zip path '%s'", zip_path)
    target_folder = Path(zip_path.stem)
    if target_folder.exists():
        shutil.rmtree(target_folder)

    macosx_path = Path("__MACOSX")
    if macosx_path.exists():
        shutil.rmtree(macosx_path)
    subprocess.run(["unzip", zip_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if macosx_path.exists():
        shutil.rmtree(macosx_path)

    logger.debug("Preprocess: Moving unzipped files to destination '%s'..", destination)
    if not destination.parent.is_dir():
        raise OSError("Destination parent is not directory")
    elif destination.exists():
        logger.warn("Preprocess: Unzipping: Destination already exists")
        shutil.rmtree(destination)
    subprocess.run(["mv", target_folder, destination], check=True)
    target_folder = destination
    return target_folder


def replace_test_file(project_folder_path: Path):
    target_path = project_folder_path / TEST_FILES_RELATIVE_PATH
    if target_path.exists():
        shutil.rmtree(target_path)
    copy_tree(f"{RESOURCE_PATH}", str(target_path))


def preprocess(path: Path) -> typing.Tuple[Path, Path]:
    if isinstance(path, str):
        path = Path(path).absolute()

    folder_id = str(path).split("/")[-1]
    logger.debug("Preprocess: UUID = %s", folder_id)

    destination = Path(f"node_project_runner/data/progress_data/{folder_id}")

    if os.path.isdir(destination):
        shutil.rmtree(destination)

    outer_project_folder_path = (
        shutil.copytree(f"{path}/source", destination) if path.is_dir() else unzip(path, destination=destination)
    )
    inner_project_folder_path = outer_project_folder_path
    replace_test_file(inner_project_folder_path)
    return outer_project_folder_path, inner_project_folder_path
