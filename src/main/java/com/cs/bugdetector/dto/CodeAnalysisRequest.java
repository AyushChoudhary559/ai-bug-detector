package com.cs.bugdetector.dto;

import lombok.Data;

@Data
public class CodeAnalysisRequest {
    private String language;
    private String sourceCode;
}
