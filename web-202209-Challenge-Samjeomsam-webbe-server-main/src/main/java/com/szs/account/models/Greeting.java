package com.szs.account.models;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "greeting")
public class Greeting {

  @Id
  @Column(name = "id")
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(name = "message")
  private String message;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  protected Greeting() {/*no-op*/}

  public Long getId() {
    return id;
  }

  public String getMessage() {
    return message;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  @Override
  public String toString() {
    return new ToStringBuilder(this, ToStringStyle.SHORT_PREFIX_STYLE)
        .append("id", id)
        .append("message", message)
        .append("createdAt", createdAt)
        .toString();
  }

}
