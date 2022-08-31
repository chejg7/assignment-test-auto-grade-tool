package com.szs.account.api;

import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

import java.util.HashMap;

import static com.szs.account.api.utils.JsonUtils.toJson;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
@TestMethodOrder(MethodOrderer.MethodName.class)
@DisplayName("API 통합 테스트")
public class ApisTest {

  private MockMvc mockMvc;

  @Autowired
  public void setMockMvc(MockMvc mockMvc) {
    this.mockMvc = mockMvc;
  }

  @Test
  @DisplayName("[인증 토큰 테스트] 인증 토큰이 없다면 API 호출을 실패한다.")
  void _01_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isUnauthorized())
    ;
  }

  @Test
  @DisplayName("[인증 토큰 테스트] 인증 토큰이 올바르지 않다면 API 호출을 실패한다.")
  void _02_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "Bearer AABBCC")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isUnauthorized())
    ;
  }

  @Test
  @DisplayName("[인증 토큰 테스트] 인증 토큰이 만료되었다면 API 호출을 실패한다.")
  void _03_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE1NTAwMDAwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isUnauthorized())
    ;
  }

  @Test
  @DisplayName("[인증 토큰 테스트] 인증 토큰 스킴(Bearer)이 올바르지 않다면 API 호출을 실패한다.")
  void _04_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isUnauthorized())
    ;
  }

  @Test
  @DisplayName("[계좌 생성 API 테스트] name 파라미터가 누락되면 API 호출을 실패한다.")
  void _05_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("name", "");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 생성 API 테스트] 세 번째 계좌를 생성할 수 있다.")
  void _06_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("name", "세 번째 저금통");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.userId", is(1)))
        .andExpect(jsonPath("$.data.name", is("세 번째 저금통")))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[계좌 생성 API 테스트] 네 번째 계좌를 생성할 수 없다.")
  void _07_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("name", "네 번째 저금통");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 3개)")
  void _08_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data").isArray())
        .andExpect(jsonPath("$.data.length()", is(3)))
        .andExpect(jsonPath("$.data[0].id", is(5)))
        .andExpect(jsonPath("$.data[0].userId", is(2)))
        .andExpect(jsonPath("$.data[0].name", is("세 번째 저금통")))
        .andExpect(jsonPath("$.data[0].createdAt").exists())
        .andExpect(jsonPath("$.data[1].id", is(4)))
        .andExpect(jsonPath("$.data[1].userId", is(2)))
        .andExpect(jsonPath("$.data[1].name", is("두 번째 저금통")))
        .andExpect(jsonPath("$.data[1].createdAt").exists())
        .andExpect(jsonPath("$.data[2].id", is(3)))
        .andExpect(jsonPath("$.data[2].userId", is(2)))
        .andExpect(jsonPath("$.data[2].name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data[2].createdAt").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 2개)")
  void _09_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "Bearer ewogICJpZCI6IDMsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data").isArray())
        .andExpect(jsonPath("$.data.length()", is(2)))
        .andExpect(jsonPath("$.data[0].id", is(7)))
        .andExpect(jsonPath("$.data[0].userId", is(3)))
        .andExpect(jsonPath("$.data[0].name", is("두 번째 저금통")))
        .andExpect(jsonPath("$.data[0].createdAt").exists())
        .andExpect(jsonPath("$.data[1].id", is(6)))
        .andExpect(jsonPath("$.data[1].userId", is(3)))
        .andExpect(jsonPath("$.data[1].name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data[1].createdAt").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 목록 조회 API 테스트] 계좌 목록을 조회할 수 있다. (계좌출력 1개)")
  void _10_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/accounts")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data").isArray())
        .andExpect(jsonPath("$.data.length()", is(1)))
        .andExpect(jsonPath("$.data[0].id", is(8)))
        .andExpect(jsonPath("$.data[0].userId", is(4)))
        .andExpect(jsonPath("$.data[0].name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data[0].createdAt").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 입출금 기록 API 테스트] 거래 금액이 1원 보다 작으면 API 호출을 실패한다.")
  void _11_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 0);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
    result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", -1);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 입출금 기록 API 테스트] 거래 구분이 올바르지 않으면 API 호출을 실패한다.")
  void _12_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 100);
                      put("type", "DEPOSIT2");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 입출금 기록 API 테스트] 출금 금액이 잔액보다 크면 API 호출을 실패한다.")
  void _13_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", Long.MAX_VALUE);
                      put("type", "WITHDRAW");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 입출금 기록 API 테스트] 100원 입금을 성공한다.")
  void _14_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 100);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(3)))
        .andExpect(jsonPath("$.data.userId", is(2)))
        .andExpect(jsonPath("$.data.amount", is(100)))
        .andExpect(jsonPath("$.data.type", is("DEPOSIT")))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[계좌 입출금 기록 API 테스트] 1원 출금을 성공한다.")
  void _15_test() throws Exception {
    ResultActions result = mockMvc.perform(
        post("/api/account/3/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDIsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 100);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(3)))
        .andExpect(jsonPath("$.data.userId", is(2)))
        .andExpect(jsonPath("$.data.amount", is(100)))
        .andExpect(jsonPath("$.data.type", is("DEPOSIT")))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[단일 계좌 조회 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.")
  void _16_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/account/9")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[단일 계좌 조회 API 테스트] accountId, userId 조합이 올바르지 않다면 API 호출을 실패한다.")
  void _17_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/account/7")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[단일 계좌 조회 API 테스트] 계좌 잔액 0원인 계좌를 조회한다.")
  void _18_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/account/8")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id", is(8)))
        .andExpect(jsonPath("$.data.userId", is(4)))
        .andExpect(jsonPath("$.data.name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data.balance", is(0)))
        .andExpect(jsonPath("$.data.interestDue", is(0.0)))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[단일 계좌 조회 API 테스트] 이자 3% 적용 계좌를 조회한다.")
  void _19_test() throws Exception {
    ResultActions result = mockMvc.perform(
        get("/api/account/1")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id", is(1)))
        .andExpect(jsonPath("$.data.userId", is(1)))
        .andExpect(jsonPath("$.data.name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data.balance", is(500)))
        .andExpect(jsonPath("$.data.interestDue", is(15.0)))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[단일 계좌 조회 API 테스트] 이자 4% 적용 계좌를 조회한다.")
  void _20_test() throws Exception {
    // 입금 처리
    ResultActions result = mockMvc.perform(
        post("/api/account/8/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 1000003);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(8)))
        .andExpect(jsonPath("$.data.userId", is(4)))
        .andExpect(jsonPath("$.data.amount", is(1000003)))
        .andExpect(jsonPath("$.data.type", is("DEPOSIT")))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
    result = mockMvc.perform(
        get("/api/account/8")
            .header("Authorization", "Bearer ewogICJpZCI6IDQsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id", is(8)))
        .andExpect(jsonPath("$.data.userId", is(4)))
        .andExpect(jsonPath("$.data.name", is("첫 번째 저금통")))
        .andExpect(jsonPath("$.data.balance", is(1000003)))
        .andExpect(jsonPath("$.data.interestDue", is(40000.1)))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[계좌 동기화 처리 API 테스트] 존재하지 않는 계좌라면 API 호출을 실패한다.")
  void _21_test() throws Exception {
    ResultActions result = mockMvc.perform(
        put("/api/account/8/sync")
            .header("Authorization", "Bearer ewogICJpZCI6IDMsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.data").doesNotExist())
        .andExpect(jsonPath("$.error").exists())
    ;
  }

  @Test
  @DisplayName("[계좌 동기화 처리 API 테스트] 거래내역이 없는 계좌를 동기화 할 수 있다.")
  void _22_test() throws Exception {
    ResultActions result = mockMvc.perform(
        put("/api/account/6/sync")
            .header("Authorization", "Bearer ewogICJpZCI6IDMsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(6)))
        .andExpect(jsonPath("$.data.lastTransactionId", is(0)))
        .andExpect(jsonPath("$.data.balance", is(0)))
        .andExpect(jsonPath("$.data.uuid").isString())
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[계좌 동기화 처리 API 테스트] 거래내역이 있는 계좌를 동기화 할 수 있다.")
  void _23_test() throws Exception {
    ResultActions result = mockMvc.perform(
        put("/api/account/1/sync")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(1)))
        .andExpect(jsonPath("$.data.lastTransactionId", is(2)))
        .andExpect(jsonPath("$.data.balance", is(500)))
        .andExpect(jsonPath("$.data.uuid").isString())
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

  @Test
  @DisplayName("[계좌 동기화 처리 API 테스트] 마지막 거래내역 ID와 계좌 잔액을 올바르게 처리한다.")
  void _24_test() throws Exception {
    // 마지막 거래 생성
    ResultActions result = mockMvc.perform(
        post("/api/account/1/transaction")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON)
            .content(
                toJson(
                    new HashMap<String, Object>() {{
                      put("amount", 250);
                      put("type", "DEPOSIT");
                    }}
                )
            )
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(1)))
        .andExpect(jsonPath("$.data.userId", is(1)))
        .andExpect(jsonPath("$.data.amount", is(250)))
        .andExpect(jsonPath("$.data.type", is("DEPOSIT")))
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
    result = mockMvc.perform(
        put("/api/account/1/sync")
            .header("Authorization", "Bearer ewogICJpZCI6IDEsCiAgImV4cGlyZSI6IDE2NzI0ODgwMDAwMDAKfQ==")
            .accept(MediaType.APPLICATION_JSON)
    );
    result.andDo(print())
        .andExpect(jsonPath("$.data").exists())
        .andExpect(jsonPath("$.data.id").isNumber())
        .andExpect(jsonPath("$.data.accountId", is(1)))
        .andExpect(jsonPath("$.data.lastTransactionId").value(greaterThan(2)))
        .andExpect(jsonPath("$.data.balance", is(750)))
        .andExpect(jsonPath("$.data.uuid").isString())
        .andExpect(jsonPath("$.data.createdAt").exists())
        .andExpect(jsonPath("$.error").doesNotExist())
    ;
  }

}
