# Assignment Test Auto Grade Tool

이 프로젝트는 과제 테스트를 자동으로 채점하기 위한 프로젝트입니다. 채점 가능한 항목은 다음과 같습니다.

- NodeJS
- Spring(Java, Kotlin)

# 프로젝트 세팅

VS CODE를 기준으로 설명합니다.

## 파이썬 다운로드

본 프로젝트는 파이썬 3.9버전을 사용합니다. [파이썬 홈페이지](https://www.python.org/downloads/)에서 파이썬 3.9버전을 다운로드 해주세요. 릴리즈 버전은 3.9버전대라면 상관 없습니다.

또는 brew를 사용하여 다운로드 할 수도 있습니다.

```
brew install python@3.9
```

## venv

가상 환경을 세팅하기 위하여
[venv](https://docs.python.org/ko/3.9/tutorial/venv.html)
를 사용합니다. venv는 python3에서 기본으로 제공하는 가상환경을 만들 수 있는 모듈입니다. venv는 python3에 빌트인 되어 있으며 python2.7에서는 사용이 불가능합니다.

다음 명령어로 현재 디렉토리에 가상환경을 만들 수 있습니다.

```
python3 -m venv auto-grade-tool-env
```

생성된 가상환경을 활성화하는 명령어는 다음과 같습니다.

- Window

```
auto-grade-tool-env\Scripts\activate.bat
```

- MacOS

```
source auto-grade-tool-env/bin/activate
```

성공적으로 가상환경에 들어갔다면 셀의 프롬프트가 변경되어 사용 중인 가상환경을 볼 수 있습니다.

## 패키지 다운로드

가상환경 활성화 이후 다음 명령어를 통하여 본 프로젝트에서 사용하는 패키지들을 다운로드하여 주세요.

```
pip install -r requirements.txt
```

## black

code formatting을 위하여 [black](https://github.com/psf/black)을 사용합니다. black을 사용하여 코드 저장 시 자동으로 formatting하기 위하여 Settings를 들어갑니다.

윈도우의 경우 `ctrl` + `,` MAC의 경우 `command` + `,`를 사용하여 Settings를 열 수 있습니다.

Settings에서 `format on save`를 on으로 설정하고 `Python › Formatting: Provider`에서 black를 선택하여주세요.

이후 코드를 저장할 때 마다 black에 의해 formatting이 이루어집니다.

## pre-commit

commit 명령어 수행 시 black이 잘 적용되었는지 확인하기 위해 [pre-commit](https://pre-commit.com/)을 사용합니다.

다음 명령어를 사용하여 pre-commit을 적용시켜주세요.

```
pre-commit install
```

#

## NodeJS 채점 준비

NodeJS 과제 테스트를 채점하기 위해서는 [yarn](https://classic.yarnpkg.com/en/)을 설치해야 합니다. yarn은 의존성 관리 javascript 패키지 매니저 입니다. node, npm, yarn 순서로 설치하겠습니다. node만 설치하면 npm은 자동으로 설치됩니다.

```
brew install node
```

다음 명령어로 node와 npm이 잘 설치되었는지 확인할 수 있습니다.

```
node -v
npm -v

```

yarn을 설치합니다. node를 위에서 설치하였으므로 _--ignore-dependecies_ 옵션을 사용하여 node를 빼고 설치할 수 있습니다.

```
brew install yarn --ignore-dependencies
```

다음 명령어로 yarn이 잘 설치되었는지 확인할 수 있습니다.

```
yarn -v
```

## Java 채점 준비

Java 과제 테스트를 채점하기 위해서는 [maven](https://maven.apache.org/)을 설치해야 합니다. Maven은 자바용 프로젝트 관리 도구입니다. brew를 사용하여 설치할 수 있습니다.

```
brew install maven
```

다음 명령어로 maven이 잘 설치되었는지 확인할 수 있습니다.

```
mvn -version
```

## Kotlin 채점 준비

Kotlin 과제 테스트를 채점하기 위해서는 [gradle](https://gradle.org/)을 설치해야 합니다. gradle은 그루비를 기반으로 한 빌드 도구입니다. brew를 사용하여 설치할 수 있습니다.

```
brew install gradle
```

다음 명령어로 gradle이 잘 설치되었는지 확인할 수 있습니다.

```
gradle --version
```

#

## 응시자 프로젝트 폴더

채점을 실시할 응시자 프로젝트 폴더를 xxxxxx_project_runner/data/origin_data 폴더 아래에 위치시켜주세요.

```
└──xxxxxx_project_runner
   └── data
       └── origin_data
           ├── 응시자1 프로젝트 폴더
           ├── 응시자2 프로젝트 폴더
           ├── 응시자3 프로젝트 폴더
            ...
```

## 테스트코드

채점에 사용할 테스트 코드를 xxxxxx_project_runner/resources 폴더 아래에 위치시켜주세요.

```
└── xxxxxx_project_runner
    └── resources
        ├── 테스트코드1
        ├── 테스트코드2
        ├── 테스트코드3
        ...
```

## constants

xxxxxx_project_runner 폴더의 contants.py에는 프로젝트 구동에 필요한 여러가지 상수 값들이 정의되어 있습니다. 필수로 수정되어야할 값은 다음과 같습니다.

- TEST_FILES_RELATIVE_PATH

  과제테스트 출제 시 초기 세팅된 테스트 코드를 삭제하고, 채점에 사용될 테스트 코드를 삽입하기 위하여 경로를 설정해주어야합니다. 응시자 프로젝트 폴더에서 기존 테스트코드가 있는 곳의 경로를 source를 기준으로 상대 경로로 입력해주시면 됩니다. 예시는 다음과 같습니다.

  - Spring

    ```
    TEST_FILES_RELATIVE_PATH = "src/test/java/com/naver/line/demo"
    ```

  - NodeJS
    ```
    TEST_FILES_RELATIVE_PATH = "test"
    ```

# 실행

다음 명령어로 프로그램을 실행시킬 수 있습니다.

```
python3 run.py
```

## 결과

프로그램 실행 후 data폴더 구조가 다음과 같이 설정됩니다.

```
└── xxxxxx_project_runner
    └── data
        ├── fail_data
        ├── origin_data
        ├── pass_data
        ├── progress_data
        └── final_result.json
```

- fail_data

  빌드에 실패한 프로젝트 폴더들이 담긴 폴더입니다. 테스트 명령어를 입력하기 전 상태로 저장됩니다.

- origin_data

  원본 프로젝트 폴더들이 담긴 폴더입니다. 프로그램을 실행하더라도 변하지 않습니다.

- pass_data

  채점에 성공한 프로젝트 폴더들이 담긴 폴더입니다. 테스트 명령어를 입력하기 전 상태로 저장됩니다.

- progress_data
  현재 채점 중인 프로젝트 폴더가 담긴 폴더입니다. 성공적으로 채점이 끝난 상태이면 빈 폴더입니다.
- final_result.json

  채점 결과가 json 파일로 저장됩니다. 응시자 프로젝트 폴더명을 키로 갖고 채점 결과를 값으로 가집니다. 채점에 성공했을 경우에는 통과한 항목에 대한 객체가 배열로 저장되어 있습니다. 빌드에 실패했을 경우 build_and_parse Fail이라는 string 값을 가집니다.
