import logging
from optparse import OptionParser
from pathlib import Path

from spring_project_runner.constants import (
    ORIGIN_DATA_PATH as SPRING_ORIGIN_DATA_PATH,
    FINAL_JSON_FILE_PATH as SPRING_FINAL_JSON_FILE_PATH,
)
from spring_project_runner.log import prepare_logger as spring_prepare_logger
from spring_project_runner.main import test_multiple as spring_test_multiple

from node_project_runner.constants import (
    ORIGIN_DATA_PATH as NODE_ORIGIN_DATA_PATH,
    FINAL_JSON_FILE_PATH as NODE_FINAL_JSON_FILE_PATH,
)
from node_project_runner.log import prepare_logger as node_prepare_logger
from node_project_runner.main import test_multiple as node_test_multiple


logger = logging.getLogger(__name__)

LOG_FILE = "autovalidator.log"

if __name__ == "__main__":

    # Log file
    spring_prepare_logger(LOG_FILE)
    logger.info("=" * 120)

    # Opt parse
    parser = OptionParser()

    parser.add_option(
        "--target",
        action="store",
        dest="target",
    )

    options, args = parser.parse_args()

    logger.info("Parsed options = %s", options)
    logger.info("Parsed args = %s", args)

    if options.target == "java" or options.target == "kotlin":
        paths = list(SPRING_ORIGIN_DATA_PATH.glob("*"))
        paths = [path for path in paths if Path(path).is_dir() or Path(path).suffix == ".zip"]
        spring_test_multiple(*paths, final_json_path=SPRING_FINAL_JSON_FILE_PATH, target=options.target)
    elif options.target == "node":
        paths = list(Path(NODE_ORIGIN_DATA_PATH).glob("*"))
        paths = [path for path in paths if Path(path).is_dir() or Path(path).suffix == ".zip"]
        node_test_multiple(*paths, final_json_path=NODE_FINAL_JSON_FILE_PATH)
    else:
        print("Set '--target' option 'node' or 'java' or 'kotlin'")
        quit()
