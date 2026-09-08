package com.cs.bugdetector.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class CodeAnalysisRequest {
    private String language;

    @JsonAlias({"code", "source"})
    private String sourceCode;

    private String fileName;

    public String language() {
        return language;
    }

    public String sourceCode() {
        return sourceCode;
    }

    public String getCode() {
        return sourceCode;
    }

    public void setCode(String code) {
        this.sourceCode = code;
    }
}