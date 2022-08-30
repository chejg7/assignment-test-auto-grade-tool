from pathlib import Path

__CURRENT_FILE_PATH = Path(__file__).absolute()

RESOURCE_PATH = __CURRENT_FILE_PATH.parent / "resources"

TEST_FILES_RELATIVE_PATH = "src/test/java/com/naver/line/demo"

SUREFILE_REPORTS = {
    "java": "target/surefire-reports",
    "kotlin": "build/test-results/test",
}


ROOT_FILE_NAME = {"java": "pom.xml", "kotlin": "gradle"}

TESTCASE_TAG = "testcase"

LOG_FILE = Path("autovalidator.log")
MAX_LOG_FILE_SIZE = 10 * (2 ** 20)
DEFAULT_LOG_FMT = "[%%(asctime)s][%%(levelname)-8s][%%(name)s][L%%(lineno)s] %%(message).%ds"
DEFAULT_LOG_DATE_FMT = "%Y/%m/%d %H:%M:%S"
LOG_MESSAGE_SIZE_FILE = 5000
LOG_MESSAGE_SIZE_STREAM = 120
LOG_BACKUP_COUNT = 5

ORIGIN_DATA_PATH = Path("spring_project_runner/data/origin_data")
FINAL_JSON_FILE_PATH = Path("spring_project_runner/data/final_result.json")
