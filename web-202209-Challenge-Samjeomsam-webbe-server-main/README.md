- [1. 과제개요](#1-과제개요)
- [2. 요구사항](#2-요구사항)
  - [2.1. 인증 토큰 처리](#21-인증-토큰-처리)
  - [2.2. API 개발](#22-api-개발)
    - [2.2.1. 계좌 생성](#221-계좌-생성)
    - [2.2.2. 계좌 목록 조회](#222-계좌-목록-조회)
    - [2.2.3. 계좌 입출금 기록](#223-계좌-입출금-기록)
    - [2.2.4. 단일 계좌 조회](#224-단일-계좌-조회)
    - [2.2.5. 계좌 동기화 처리](#225-계좌-동기화-처리)

---

## 1. 과제개요

요구 사항 항목을 참고하여 `spring-web-mvc`, `spring-data-jpa` 기반 계좌 관리 API 서버를 개발한다.

- 라이브러리 추가를 위해 `build.gradle` 파일을 수정할 수 있음
- `com.szs.account.api.ApisTest`의 모든 테스트(총 24개)를 통과해야 함
  - 테스트 실행 명령: gradle clean test
  - 기존 24개 테스트케이스 외에 응시자가 자유롭게 테스트 추가 가능함
- 개발에 필요한 데이터베이스 스키마 및 샘플 데이터가 준비되어 있음
  - In-Memory 경량 RDBMS H2가 사용되며 **프로젝트를 재시작 할 때마다 데이터가 초기화 됨**
  - 스키마: resources/schema-h2.sql
  - 데이터: resources/data-h2.sql
  - 스키마 및 샘플 데이터 수정 없이 채점을 위한 모든 테스트 통과가 가능함 (샘플 데이터 수정시 일부 테스트가 실패 할수 있음에 주의)

> `greeting 테이블`, `Greeting.java`, `GreetingRepository.java`, `GreetingService.java` 그리고 `GET /api/greeting/{greetingId}` API 구현은 샘플 코드이며, 과제 구현과는 전혀 관계없다. (삭제해도 무방함)

## 2. 요구사항

본 요구사항 항목에 따라 기존 부분을 수정하거나 새롭게 개발한다.

### 2.1. 인증 토큰 처리

계좌 관리 API에 접근하기 위해서는 HTTP `Authorization 헤더`를 통해 전달되는 `access-token` 처리가 필요하다. (Bearer 스킴)

```
Authorization: Bearer {access-token}
```

`access-token` 값은 아래와 같은 JSON 텍스트를 base64 인코딩해 만들어진다. (인코딩 문자셋 UTF-8)

- id — 사용자 ID
- expire — `access-token` 만료 시각 (Epoch Unix Timestamp)

```json
{
  "id": 1,
  "expire": 1672488000000
}
```

아래는 위 JSON 텍스트를 base64 인코딩해 만들어진 access-token 이다.

```text
ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==
```

`access-token`을 정상적으로 디코딩할 수 없거나(존재하지 않는 경우 포함) 또는 만료되었다면 `HTTP STATUS 401`로 응답한다.

`access-token`을 정상적으로 디코딩할 수 있고 만료되지 않았다면 정상적으로 API 호출이 가능하다. 이때, `AuthorizedUser` 인스턴스를 생성하고, `HttpServletRequest.setAttribute` 메소드를 이용하여 Controller 메소드에 `AuthorizedUser` 인스턴스를 전달할 수 있도록 한다.

위 요구사항에 따라 `com.szs.account.auth.interceptor.UserAuthenticationInterceptor` 클래스 구현을 완성한다.

### 2.2. API 개발

API 응답 포맷을 아래와 같이 정의한다.

- 정상 처리 및 오류 처리 모두 `HTTP STATUS 200`으로 응답함
  - `access-token`을 정상적으로 디코딩할 수 없거나 또는 만료되었다면, API는 정상적으로 호출되지 않으며 `HTTP STATUS 401`로 응답함
- 정상 처리라면 `data 필드를 포함`하고, `error 필드는 null`을 출력함
- 오류 처리라면 `data 필드는 null`이고, `error 필드는 오류 메시지`를 출력함

구현해야 하는 API 목록은 아래와 같다.

#### 2.2.1. 계좌 생성

사용자는 최대 3개의 계좌를 생성할 수 있다. 3개를 초과하여 계좌 생성 요청시 오류로 처리한다. 필요한 사용자 데이터는 `AuthorizedUser` 인스턴스에서 가져온다.

- URL: POST /api/account
- Request Body:
  - `name`: 계좌 명칭

```json
{
  "name": "세 번째 저금통"
}
```

- Response Body:
  - `id`: 계좌 ID
  - `userId`: 사용자 ID
  - `name`: 계좌 명칭
  - `createdAt`: 계좌 생성일시

```json
{
  "data": {
    "id": 9,
    "userId": 1,
    "name": "세 번째 저금통",
    "createdAt": "2022-08-04 00:23:10"
  },
  "error": null
}
```

계좌 갯수 초과시 응답 예시는 아래와 같다.

```json
{
  "data": null,
  "error": "계좌 최대 갯수 초과"
}
```

#### 2.2.2. 계좌 목록 조회

사용자의 모든 계좌 목록을 `id` 값이 큰 순서로 정렬하여 출력한다. 필요한 사용자 데이터는 `AuthorizedUser` 인스턴스에서 가져온다.

- URL: GET /api/accounts
- Request Body: N/A
- Response Body: 계좌 목록

```json
{
  "data": [
    {
      "id": 9,
      "userId": 1,
      "name": "세 번째 저금통",
      "createdAt": "2022-08-04 00:23:10"
    },
    {
      "id": 2,
      "userId": 1,
      "name": "두 번째 저금통",
      "createdAt": "2022-08-04 00:22:53"
    },
    {
      "id": 1,
      "userId": 1,
      "name": "첫 번째 저금통",
      "createdAt": "2022-08-04 00:22:53"
    }
  ],
  "error": null
}
```

#### 2.2.3. 계좌 입출금 기록

계좌에 입금, 출금 거래 기록을 추가한다. 단, 출금 금액은 계좌의 현재 잔액보다 클수 없다. 필요한 사용자 데이터는 `AuthorizedUser` 인스턴스에서 가져온다.

- URL: POST /api/account/{accountId}/transaction
  - {accountId}: 계좌 ID
- Request Body:
  - `amount`: 거래 금액 (0보다 큰 양의 정수)
  - `type`: 거래 구분
    - DEPOSIT: 입금
    - WITHDRAW: 출금
```json
{
  "amount": 400000,
  "type": "DEPOSIT"
}
```

```json
{
  "amount": 1000000,
  "type": "WITHDRAW"
}
```

- Response Body:
  - `id`: 거래 ID
  - `accountId`: 계좌 ID
  - `userId`: 사용자 ID
  - `amount`: 거래 금액
  - `type`: 거래 구분
  - `createdAt`: 거래 생성일시

```json
{
  "data": {
    "id": 3,
    "accountId": 1,
    "userId": 1,
    "amount": 400000,
    "type": "DEPOSIT",
    "createdAt": "2022-08-04 00:24:23"
  },
  "error": null
}
```

출금 금액이 계좌의 현재 잔액보다 큰 경우 응답 예시는 아래와 같다.

```json
{
  "data": null,
  "error": "출금 금액은 현재 잔액보다 클 수 없음"
}
```

#### 2.2.4. 단일 계좌 조회

사용자의 특정 계좌를 출력한다. 출력 항목에는 계좌의 `현재 잔액`과 `지급 예정 이자`가 포함된다. 필요한 사용자 데이터는 `AuthorizedUser` 인스턴스에서 가져온다.

- `현재 잔액` — 입출금 금액의 총 합 (0보다 작을수 없음)
  - 입출금 거래 기록이 없다면 0원으로 처리함
- `지급 예정 이자` — 소수점 둘 째 자리에서 반올림 하여, 첫째 자리까지만 표현함
  - 소수점 처리 예시 — `1.23원 → 1.2원`, `1.46원 → 1.5원`
  - `현재 잔액`이 `1,000,000원 미만`인 경우 `3% 이율` 적용
    - 현재 잔액 500,000원 이라면 지급 예정 이자 15,000.0원
    - 현재 잔액 15원 이라면 지급 예정 이자 0.5원
  - `현재 잔액`이 `1,000,000원 이상`인 경우 `4% 이율` 적용
    - 현재 잔액 1,000,000원 이라면 지급 예정 이자 40,000.0원
    - 현재 잔액 1,000,003원 이라면 지급 예정 이자 40,000.1원

- URL: GET /api/account/{accountId}
  - {accountId}: 계좌 ID
- Request Body: N/A
- Response Body: 특정 계좌 정보
  - `id`: 계좌 ID
  - `userId`: 사용자 ID
  - `name`: 계좌 명칭
  - `balance`: 계좌 잔액
  - `interestDue`: 지급 예정 이자
  - `createdAt`: 계좌 생성일시

```json
{
  "data": {
    "id": 2,
    "userId": 1,
    "name": "두 번째 저금통",
    "balance": 0,
    "interestDue": 0.0,
    "createdAt": "2022-08-04 00:22:53"
  },
  "error": null
}
```

#### 2.2.5. 계좌 동기화 처리

현재 계좌 상태를 외부 서비스에 동기화한다. 계좌 상태에는 `계좌 현재 잔액`, `계좌의 가장 마지막 거래 ID`가 포함된다.

동기화를 위한 외부 서비스 API 스펙은 아래와 같다.

> 외부 서비스 연동을 위해 `Spring WebClient`, `OkHttp`, `Apache HttpClient` 라이브러리를 `build.gradle` 파일에 포함하고 있다. 그 외 필요한 HTTP Client 라이브러리는 자유롭게 추가하고 사용할 수 있다.

- URL: POST https://codetest.3o3.co.kr/api/account/sync
- Request Body:
  - `accountId`: 계좌 ID
  - `lastTransactionId`: 마지막 거래 ID
    - 해당 계좌에 거래내역이 없다면 0으로 처리함
  - `balance`: 계좌 잔액

```json
{
    "accountId": 1,
    "lastTransactionId": 10,
    "balance": 100000
}
```

- Response Body:
  - `accountId`: 계좌 ID
  - `lastTransactionId`: 마지막 거래 ID
  - `balance`: 계좌 잔액
  - `uuid`: 동기화 완료 UUID

```json
{
	"accountId": 1,
	"lastTransactionId": 10,
	"balance": 100000,
	"uuid": "bd60d5e7-53af-4605-a8fe-bdf83820dd7b"
}
```

외부 서비스 동기화 처리 결과 응답에서 `UUID` 필드값을 추출하여 `동기화 로그를 데이터베이스(account_sync_logs 테이블)에 저장`하고 응답을 출력한다. 필요한 사용자 데이터는 `AuthorizedUser` 인스턴스에서 가져온다.

- URL: PUT /api/account/{accountId}/sync
  - {accountId}: 계좌 ID
- Request Body: N/A
- Response Body: 동기화 로그
  - `id`: 동기화 로그 ID
  - `accountId`: 계좌 ID
  - `lastTransactionId`: 계좌의 가장 마지막 거래 ID
  - `balance`: 계좌 현재 잔액
  - `uuid`: 동기화 완료 UUID
  - `createdAt`: 동기화 처리 일시

```json
{
  "data": {
    "id": 1,
    "accountId": 1,
    "lastTransactionId": 3,
    "balance": 400500,
    "uuid": "11dfafa6-dc65-427b-8946-03df93c8d034",
    "createdAt": "2022-08-04 00:25:44"
  },
  "error": null
}
```
