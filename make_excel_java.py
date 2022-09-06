import json
import openpyxl

TARGET_JSON_FILE = "spring_project_runner/data/final_result 2.json"
RESULT_EXCEL_FILE_NAME = "3o3_backend_java.xlsx"

wb = openpyxl.Workbook()
wb.active.title = "SHEET"
sheet = wb[wb.active.title]

user_data = []
column_list = []
api_list = []
data_set = {
    "CreateAccountTests": {  # 11개
        "name": "1. 계좌 생성",
        "test": {
            "unauthorizedWithoutHeader": {
                "name": "실패 - 인증 없음(401) w/o X-USER-ID header",
                "score": 1,
            },
            "unauthorized": {
                "name": "실패 - 인증 실패(401)",
                "score": 2,
            },
            "invalidTransferLimit": {
                "name": "실패 - transfer_limit 유효하지 않음(400)",
                "score": 2,
            },
            "invalidDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 유효하지 않음(400)",
                "score": 2,
            },
            "negativeTransferLimit": {
                "name": "실패 - transfer_limit 음수(400)",
                "score": 2,
            },
            "negativeDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 음수(400)",
                "score": 2,
            },
            "overMaximumTransferLimit": {
                "name": "실패 - transfer_limit 최댓값 초과(400)",
                "score": 2,
            },
            "overMaximumDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 최댓값 초과(400)",
                "score": 2,
            },
            "createdToday": {
                "name": "실패 - 하루 1개 계좌 개설(400)",
                "score": 3,
            },
            "hasThreeAccounts": {
                "name": "실패 - 최대 3개 계좌 개설(400)",
                "score": 3,
            },
            "success": {
                "name": "성공",
                "score": 5,
            },
        },
    },
    "DeleteAccountTests": {  # 7개
        "name": "2. 계좌 비활성화",
        "test": {
            "unauthorizedWithoutHeader": {
                "name": "실패 - 인증 없음(401) w/o X-USER-ID header",
                "score": 1,
            },
            "unauthorized": {
                "name": "실패 - 인증 실패(401)",
                "score": 2,
            },
            "notFound": {
                "name": "실패 - 계좌를 찾을 수 없음(404)",
                "score": 3,
            },
            "forbidden": {
                "name": "실패 - 계좌 소유자가 아님(403)",
                "score": 3,
            },
            "disabledAccount": {
                "name": "실패 - 이미 비활성화된 경우(400)",
                "score": 3,
            },
            "remainedBalance": {
                "name": "실패 - 잔액이 남아 있는 경우(400)",
                "score": 3,
            },
            "success": {
                "name": "성공",
                "score": 5,
            },
        },
    },
    "UpdateAccountTransferLimitTests": {  # 12개
        "name": "3. 계좌 이체 한도 수정",
        "test": {
            "unauthorizedWithoutHeader": {
                "name": "실패 - 인증 없음(401) w/o X-USER-ID header",
                "score": 1,
            },
            "unauthorized": {
                "name": "실패 - 인증 실패(401)",
                "score": 1,
            },
            "notFound": {
                "name": "실패 - 계좌를 찾을 수 없음(404)",
                "score": 3,
            },
            "forbidden": {
                "name": "실패 - 계좌 소유자가 아님(403)",
                "score": 3,
            },
            "disabledAccount": {
                "name": "실패 - 계좌가 비활성화된 경우(400)",
                "score": 3,
            },
            "negativeTransferLimit": {
                "name": "실패 - transfer_limit 음수(400)",
                "score": 2,
            },
            "invalidTransferLimit": {
                "name": "실패 - transfer_limit 유효하지 않음(400)",
                "score": 2,
            },
            "invalidDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 유효하지 않음(400)",
                "score": 2,
            },
            "negativeDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 음수(400)",
                "score": 2,
            },
            "overMaximumTransferLimit": {
                "name": "실패 - transfer_limit 최댓값 초과(400)",
                "score": 2,
            },
            "overMaximumDailyTransferLimit": {
                "name": "실패 - daily_transfer_limit 최댓값 초과(400)",
                "score": 2,
            },
            "success": {
                "name": "성공",
                "score": 5,
            },
        },
    },
    "TransferTests": {  # 15개
        "name": "4. 이체",
        "test": {
            "unauthorizedWithoutHeader": {
                "name": "실패 - 인증 없음(401) w/o X-USER-ID header",
                "score": 1,
            },
            "unauthorized": {
                "name": "실패 - 인증 실패(401)",
                "score": 1,
            },
            "notFoundSenderAccount": {
                "name": "실패 - 출금 계좌를 찾을 수 없음(404)",
                "score": 2,
            },
            "notFoundReceiverAccount": {
                "name": "실패 - 입금 계좌를 찾을 수 없음(404)",
                "score": 2,
            },
            "forbidden": {
                "name": "실패 - 출금 계좌 소유자가 아님(403)",
                "score": 2,
            },
            "zeroAmount": {
                "name": "실패 - amount 최솟값 1 이하(400)",
                "score": 3,
            },
            "invalidSenderAccountNumber": {
                "name": "실패 - sender_account_number 형식에 맞지 않음(400)",
                "score": 3,
            },
            "invalidReceiverAccountNumber": {
                "name": "실패 - receiver_account_number 형식에 맞지 않음(400)",
                "score": 3,
            },
            "disabledSenderAccount": {
                "name": "실패 - 출금 계좌가 비활성화인 경우(400)",
                "score": 3,
            },
            "disabledReceiverAccount": {
                "name": "실패 - 입금 계좌가 비활성화인 경우(400)",
                "score": 3,
            },
            "overTransferLimit": {
                "name": "실패 - 3회 이체 한도 초과(400)",
                "score": 3,
            },
            "overDailyTransferLimit": {
                "name": "실패 - 1일 이체 한도 초과(400)",
                "score": 5,
            },
            "overBalanceAmount": {
                "name": "실패 - 출금 계좌 잔액 초과(400)",
                "score": 3,
            },
            "success": {
                "name": "성공",
                "score": 10,
            },
            "successWithNote": {
                "name": "성공 - note",
                "score": 5,
            },
        },
    },
    "FindAllTransactionsOfAccountTests": {
        "name": "5. 거래 내역 조회",
        "test": {  # 18개
            "unauthorizedWithoutHeader": {
                "name": "실패 - 인증 없음(401) w/o X-USER-ID header",
                "score": 1,
            },
            "unauthorized": {
                "name": "실패 - 인증 실패(401)",
                "score": 1,
            },
            "notFound": {
                "name": "실패 - 계좌를 찾을 수 없음(404)",
                "score": 3,
            },
            "forbidden": {
                "name": "실패 - 계좌 소유자가 아님(403)",
                "score": 3,
            },
            "disabledAccount": {
                "name": "실패 - 계좌가 비활성화된 경우(400)",
                "score": 3,
            },
            "successInvalidPage": {
                "name": "성공 - page 유효하지 않음",
                "score": 2,
            },
            "successInvalidSize": {
                "name": "성공 - size 유효하지 않음",
                "score": 2,
            },
            "successNegativePage": {
                "name": "성공 - page 음수",
                "score": 2,
            },
            "successNegativeSize": {
                "name": "성공 - size 음수",
                "score": 2,
            },
            "successOverMaximumSize": {
                "name": "성공 - size 최댓값 초과",
                "score": 2,
            },
            "successInvalidFromDate": {
                "name": "성공 - from_date 유효하지 않음",
                "score": 2,
            },
            "successInvalidToDate": {
                "name": "성공 - to_date 유효하지 않음",
                "score": 2,
            },
            "successFutureFromDate": {
                "name": "성공 - from_date 오늘보다 미래",
                "score": 2,
            },
            "successFutureToDate": {
                "name": "성공 - to_date 오늘보다 미래",
                "score": 2,
            },
            "successFutureFromDateThanTodate": {
                "name": "성공 - from_date 조회 종료 일자 보다 미래",
                "score": 2,
            },
            "successDefault": {
                "name": "성공",
                "score": 3,
            },
            "successWithPageable": {
                "name": "성공 - pageable",
                "score": 3,
            },
            "successWithDate": {
                "name": "성공 - date",
                "score": 3,
            },
        },
    },
}

test_set = {
    "[인증 토큰 테스트] 인증 토큰이 없다면 API 호출을 실패한다.": 10,
    "[인증 토큰 테스트] 인증 토큰이 올바르지 않다면 API 호출을 실패한다.": 10,
    "[인증 토큰 테스트] 인증 토큰이 만료되었다면 API 호출을 실패한다.": 10,
    "[인증 토큰 테스트] 인증 토큰 스킴(Bearer)이 올바르지 않다면 API 호출을 실패한다.": 10,
    "[계좌 생성 API 테스트] name 파라미터가 누락되면 API 호출을 실패한다.": 10,
    "[계좌 생성 API 테스트] 세 번째 계좌를 생성할 수 있다.": 10,
    "[계좌 생성 API 테스트] 네 번째 계좌를 생성할 수 없다.": 10,
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 3개)": 10,
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 2개)": 10,
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 1개)": 10,
    "[계좌 입출금 기록 API 테스트] 거래 금액이 1원 보다 작으면 API 호출을 실패한다.": 10,
    "[계좌 입출금 기록 API 테스트] 거래 구분이 올바르지 않으면 API 호출을 실패한다.": 10,
    "[계좌 입출금 기록 API 테스트] 출금 금액이 잔액보다 크면 API 호출을 실패한다.": 10,
    "[계좌 입출금 기록 API 테스트] 100원 입금을 성공한다.": 10,
    "[계좌 입출금 기록 API 테스트] 1원 출금을 성공한다.": 10,
    "[단일 계좌 조회 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.": 10,
    "[단일 계좌 조회 API 테스트] accountId, userId 조합이 올바르지 않다면 API 호출을 실패한다.": 10,
    "[단일 계좌 조회 API 테스트] 계좌 잔액 0원인 계좌를 조회한다.": 20,
    "[단일 계좌 조회 API 테스트] 이자 3% 적용 계좌를 조회한다.": 20,
    "[단일 계좌 조회 API 테스트] 이자 4% 적용 계좌를 조회한다.": 20,
    "[계좌 동기화 처리 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.": 10,
    "[계좌 동기화 처리 API 테스트] 거래내역이 없는 계좌를 동기화 할 수 있다.": 20,
    "[계좌 동기화 처리 API 테스트] 거래내역이 있는 계좌를 동기화 할 수 있다.": 20,
    "[계좌 동기화 처리 API 테스트] 마지막 거래내역 ID와 계좌 잔액을 올바르게 처리한다.": 20,
}

# 최종 결과 파일을 user_data로 로딩함
# {폴더명 : 결과값 리스트}
with open(TARGET_JSON_FILE) as f:
    user_data = json.load(f)

# 채점 항목표에서 채점 항목만 리스트로 뽑아내기 위해 사용하는 함수
def make_list():
    global total_api_cnt
    for index in data_set:
        for test in data_set[index]["test"]:
            api_list.append(f"{index} {test}")
            column_list.append(f"{data_set[index]['name']} {data_set[index]['test'][test]['name']}".strip())


# make_list()

test_list = [
    "[인증 토큰 테스트] 인증 토큰이 없다면 API 호출을 실패한다.",
    "[인증 토큰 테스트] 인증 토큰이 올바르지 않다면 API 호출을 실패한다.",
    "[인증 토큰 테스트] 인증 토큰이 만료되었다면 API 호출을 실패한다.",
    "[인증 토큰 테스트] 인증 토큰 스킴(Bearer)이 올바르지 않다면 API 호출을 실패한다.",
    "[계좌 생성 API 테스트] name 파라미터가 누락되면 API 호출을 실패한다.",
    "[계좌 생성 API 테스트] 세 번째 계좌를 생성할 수 있다.",
    "[계좌 생성 API 테스트] 네 번째 계좌를 생성할 수 없다.",
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 3개)",
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 2개)",
    "[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 1개)",
    "[계좌 입출금 기록 API 테스트] 거래 금액이 1원 보다 작으면 API 호출을 실패한다.",
    "[계좌 입출금 기록 API 테스트] 거래 구분이 올바르지 않으면 API 호출을 실패한다.",
    "[계좌 입출금 기록 API 테스트] 출금 금액이 잔액보다 크면 API 호출을 실패한다.",
    "[계좌 입출금 기록 API 테스트] 100원 입금을 성공한다.",
    "[계좌 입출금 기록 API 테스트] 1원 출금을 성공한다.",
    "[단일 계좌 조회 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.",
    "[단일 계좌 조회 API 테스트] accountId, userId 조합이 올바르지 않다면 API 호출을 실패한다.",
    "[단일 계좌 조회 API 테스트] 계좌 잔액 0원인 계좌를 조회한다.",
    "[단일 계좌 조회 API 테스트] 이자 3% 적용 계좌를 조회한다.",
    "[단일 계좌 조회 API 테스트] 이자 4% 적용 계좌를 조회한다.",
    "[계좌 동기화 처리 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.",
    "[계좌 동기화 처리 API 테스트] 거래내역이 없는 계좌를 동기화 할 수 있다.",
    "[계좌 동기화 처리 API 테스트] 거래내역이 있는 계좌를 동기화 할 수 있다.",
    "[계좌 동기화 처리 API 테스트] 마지막 거래내역 ID와 계좌 잔액을 올바르게 처리한다.",
]

# data_set을 이용하여 엑셀 파일을 만드는 함수
def make_excel():
    sheet.append(["이름", "점수"] + column_list)
    total_api_cnt = len(column_list)
    for user in user_data:
        print(user)
        ox_list = ["X" for i in range(total_api_cnt)] + ["JAVA"]
        print(ox_list)
        current_score = 0

        if type(user_data[user]) is str:
            ox_list += ["Build Fail"]
        elif type(user_data[user]) is list:
            for item in user_data[user]:
                test_name = item["name"]
                current_score += test_set[test_name]
                ox_list[api_list.index(test_name)] = "O"

        sheet.append([user, current_score] + ox_list)

    wb.save(RESULT_EXCEL_FILE_NAME)


# test_list를 이용하여 엑셀 파일을 만드는 함수
def make_excel_2():
    sheet.append(["이름", "점수"] + test_list)
    total_api_cnt = len(test_list)
    for user in user_data:
        ox_list = ["X" for i in range(total_api_cnt)]
        current_score = 0

        for item in user_data[user]:
            test_name = item["name"]
            current_score += test_set[test_name]
            ox_list[test_list.index(test_name)] = "O"

        sheet.append([user, current_score] + ox_list)

    wb.save(RESULT_EXCEL_FILE_NAME)


# make_excel()
make_excel_2()
