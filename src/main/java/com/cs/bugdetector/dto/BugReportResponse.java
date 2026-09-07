package com.cs.bugdetector.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class BugReportResponse {
    private Integer score;
    private String summary;
    private List<Issue> issues;
    private Complexity complexity;
    private List<String> performance;
    private Quality quality;
    private List<TestCase> testCases;

    @Data
    public static class Issue {
        private Integer lineNumber;
        private String issueType;
        private String severity;
        private String title;
        private String description;
        private String recommendation;
        private String fixCode;
    }

    @Data
    public static class Complexity {
        private String time;
        private String timeExplanation;
        private String space;
        private String spaceExplanation;
    }

    @Data
    public static class Quality {
        private Integer readability;
        private Integer maintainability;
        private Integer reliability;
        private Integer smells;
    }

    @Data
    public static class TestCase {
        private String input;
        private String expected;
        private String purpose;
    }
}
