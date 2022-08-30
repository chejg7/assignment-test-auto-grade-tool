import logging
import os
from pathlib import Path
import subprocess
import shutil
from distutils.dir_util import copy_tree
import typing

from .constants import ROOT_FILE_NAME, TEST_FILES_RELATIVE_PATH, RESOURCE_PATH

logger = logging.getLogger(__name__)


def unzip(zip_path: Path, destination: Path) -> Path:
    logger.debug("Preprocess: Unzipping..")
    if not zip_path.exists():
        raise FileNotFoundError("Cannot find zip path '%s'", zip_path)
    target_folder = Path(zip_path.stem)
    if target_folder.exists():
        shutil.rmtree(target_folder)

    macosx_path = Path("__MACOSX")
    if macosx_path.exists():
        shutil.rmtree(macosx_path)
    subprocess.run(
        ["unzip", zip_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
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


def find_project_path(unzipped_path: Path, target: str) -> Path:
    root_file_name = ROOT_FILE_NAME[target]

    available_paths = list(unzipped_path.glob("%s" % (root_file_name,)))
    if len(available_paths) == 1:
        return available_paths[0].absolute().parent
    elif len(available_paths) > 1:
        raise OSError("Multiple '%s' found: %s" % (root_file_name, available_paths[:5]))
    else:
        raise FileNotFoundError("Cannot find '%s'" % (root_file_name,))


def place_file(target_folder: Path, file: Path) -> Path:
    os.makedirs(target_folder, exist_ok=True)
    target_path = target_folder / file.name
    if target_path.exists():
        os.remove(target_path)
    shutil.copyfile(file, target_path)
    return target_path


# resources 하위 파일 target_path로 복사
def replace_test_file(project_folder_path: Path):
    target_path = project_folder_path / TEST_FILES_RELATIVE_PATH

    # 기존에 test 파일 존재 시 삭제
    if os.path.isdir(project_folder_path / "src" / "test"):
        shutil.rmtree(project_folder_path / "src" / "test")
    copy_tree(str(RESOURCE_PATH), str(target_path))


def remove_target_file(target_path: Path):
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)


def preprocess(path: Path, target: str) -> typing.Tuple[Path, Path]:
    if isinstance(path, str):
        path = Path(path).absolute()

    folder_id = str(path).split("/")[-1]

    logger.debug("Preprocess: UUID = %s", folder_id)
    destination = Path(f"spring_project_runner/data/progress_data/{folder_id}")

    if os.path.isdir(destination):
        shutil.rmtree(destination)

    project_folder_relative_path = (
        shutil.copytree(path / "source", destination) if path.is_dir() else unzip(path, destination=destination)
    )

    remove_target_folder = ""
    if target == "java":
        remove_target_folder = "target"
    elif target == "kotlin":
        remove_target_folder = "build"

    # 기존 target file 제거
    default_target_path = f"{project_folder_relative_path}/{remove_target_folder}"
    if os.path.isdir(default_target_path):
        shutil.rmtree(default_target_path)

    project_folder_absolute_path = find_project_path(project_folder_relative_path, target)
    replace_test_file(project_folder_absolute_path)
    return project_folder_relative_path, project_folder_absolute_path
