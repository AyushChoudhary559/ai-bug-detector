package com.cs.bugdetector.dto;

public record CodeAnalysisRequest(
    String language,
    String sourceCode
) {}
