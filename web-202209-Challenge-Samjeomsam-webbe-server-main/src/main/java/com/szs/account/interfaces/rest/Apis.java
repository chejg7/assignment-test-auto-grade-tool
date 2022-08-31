package com.szs.account.interfaces.rest;

import com.szs.account.auth.AuthorizedUser;
import com.szs.account.interfaces.rest.dto.ApiResult;
import com.szs.account.models.Greeting;
import com.szs.account.services.GreetingService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class Apis {

  private final GreetingService greetingService;

  public Apis(GreetingService greetingService) {
    this.greetingService = greetingService;
  }

  @GetMapping("/greeting/{greetingId}")
  public ApiResult<String> greeting(
      @RequestAttribute(required = false) AuthorizedUser authorizedUser,
      @PathVariable long greetingId
  ) {
    return ApiResult.succeed(
        greetingService.getMessage(greetingId)
            .map(Greeting::getMessage)
            .orElse("fallback greeting message!")
    );
  }

}
