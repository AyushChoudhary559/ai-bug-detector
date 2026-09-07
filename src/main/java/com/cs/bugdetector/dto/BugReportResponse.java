package com.cs.bugdetector.dto;

import java.util.List;

public record BugReportResponse(
    String summary,
    int totalBugsFound,
    String qualityScore,
    List<Issue> issues,
    String correctedCode
) {
    public record Issue(
        int lineNumber,
        String issueType,
        String severity,
        String description,
        String recommendation
    ) {}
}
