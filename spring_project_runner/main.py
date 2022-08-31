import json
import logging
import os
from pathlib import Path
import subprocess
import traceback
import typing
import xml.etree.ElementTree as ElementTree
import warnings

from .constants import FINAL_JSON_FILE_PATH, SUREFILE_REPORTS, TESTCASE_TAG
from .preprocess import preprocess
from .postprocess import postprocess

logger = logging.getLogger(__name__)


def parse(xml_path: Path) -> typing.List[dict]:
    try:
        root = ElementTree.parse(xml_path).getroot()
        successful_tests = []

        successful_tests = [
            child.attrib for child in root if child.tag == TESTCASE_TAG and not [grandchild for grandchild in child]
        ]
        return successful_tests
    except FileNotFoundError:
        return []


def build_and_parse(target: str) -> typing.List[dict]:
    subprocess_result = ""
    if target == "java":
        subprocess_result = subprocess.run(
            ["mvn", "clean", "test"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=300,
        )
    elif target == "kotlin":
        subprocess_result = subprocess.run(
            ["gradle", "clean", "test"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=300,
        )

    if subprocess_result.returncode != 0:
        logger.warning("Build or test failed with exit code %d.", subprocess_result.returncode)
    successful_tests = []
    report_base_path = Path(SUREFILE_REPORTS[target])

    for file in os.listdir(report_base_path):
        if file.split(".")[-1] == "xml":
            successful_tests += parse(report_base_path / file)

    return successful_tests


def test_single(path: Path, target: str) -> typing.Tuple[str, typing.List[dict]]:
    logger.info("Preprocessing for '%s'..", path)
    original_path = os.getcwd()
    is_pass = True

    project_folder_relative_path, project_folder_absolute_path = preprocess(path, target)
    logger.debug(
        "Preprocessed. Outer = '%s', Inner = '%s'",
        project_folder_relative_path,
        project_folder_absolute_path,
    )
    os.chdir(project_folder_absolute_path)

    try:
        logger.info("Build and parsing for '%s'..", path)
        result = build_and_parse(target)
    except:
        logger.exception("Something went wrong.")
        result = "build_and_parse Fail"
        is_pass = False

    os.chdir(original_path)
    logger.info("Postprocessing for '%s'..", path)
    postprocess(project_folder_relative_path, is_pass)
    return project_folder_relative_path.name, result


def test_multiple(*paths: typing.Iterable[Path], final_json_path: Path = FINAL_JSON_FILE_PATH, target: str):
    logger.info("Starting multiple test..")
    universal_result = {}
    for path in paths:
        if isinstance(path, str):
            path = Path(path)
        _uuid, result = test_single(path, target)
        universal_result[path.name] = result
    logger.info("Saving total result into json file..")
    with open(final_json_path, "w") as jsonfile:
        json.dump(universal_result, jsonfile, indent=4, ensure_ascii=False)
