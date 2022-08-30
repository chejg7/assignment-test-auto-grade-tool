import json
import logging
import os
from pathlib import Path
import subprocess
import typing

from .constants import FINAL_JSON_FILE_PATH, ERROR_FILE
from .preprocess import preprocess
from .postprocess import postprocess

logger = logging.getLogger(__name__)


def parse(error_txt: Path) -> list:
    result = []
    with open(error_txt, "r") as errorfile:
        for line in errorfile:
            if "API" in line.strip():
                result.append(line.strip())
    if len(result) == 0:
        result = "build_and_parse Fail"
    return result


def build_and_parse() -> typing.List[dict]:
    subprocess.run(["yarn", "install"])

    with open(ERROR_FILE, "w") as error_file:
        subprocess_result = subprocess.run(["jest"], stdout=subprocess.DEVNULL, stderr=error_file)

    if subprocess_result.returncode != 0:
        logger.warning("Build or test failed with exit code %d.", subprocess_result.returncode)

    return parse(ERROR_FILE)


def test_single(path: Path) -> typing.Tuple[str, typing.List[dict]]:
    logger.info("Preprocessing for '%s'..", path)
    original_path = os.getcwd()
    outer_project_path, inner_project_path = preprocess(path)
    logger.debug("Preprocessed. Outer = '%s', Inner = '%s'", outer_project_path, inner_project_path)
    os.chdir(inner_project_path)

    try:
        logger.info("Build and parsing for '%s'..", path)
        result = build_and_parse()
    except Exception as exc:
        logger.exception("Something went wrong.")
        result = []

    os.chdir(original_path)
    logger.info("Postprocessing for '%s'..", path)

    postprocess(path, outer_project_path)

    return outer_project_path.name, result


def test_multiple(*paths: typing.Iterable[Path], final_json_path: Path = FINAL_JSON_FILE_PATH):
    logger.info("Starting multiple test..")
    universal_result = {}

    for path in paths:
        if isinstance(path, str):
            path = Path(path)
        _uuid, result = test_single(path)
        universal_result[path.name] = result
    logger.info("Saving total result into json file..")
    with open(final_json_path, "w") as jsonfile:
        json.dump(universal_result, jsonfile, indent=4, ensure_ascii=False)
