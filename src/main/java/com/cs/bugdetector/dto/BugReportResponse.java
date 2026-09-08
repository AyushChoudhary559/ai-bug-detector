package com.cs.bugdetector.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class BugReportResponse {
    private Long auditId;
    private String language;
    private Integer score;
    private String qualityScore;
    private String summary;
    private String status;
    private String compileStatus;
    private int totalBugsFound;

    @Builder.Default
    private List<Issue> issues = new ArrayList<>();

    @Builder.Default
    private List<Issue> bugs = new ArrayList<>();

    @Builder.Default
    private List<Issue> securityIssues = new ArrayList<>();

    @Builder.Default
    private List<Issue> performanceIssues = new ArrayList<>();

    @Builder.Default
    private List<String> recommendations = new ArrayList<>();

    @Builder.Default
    private List<String> performance = new ArrayList<>();

    private Complexity complexity;
    private Quality quality;

    @Builder.Default
    private List<TestCase> testCases = new ArrayList<>();

    private String correctedCode;

    // Backward-compatible record-like getters
    public Integer score() {
        return score != null ? score : 0;
    }

    public String qualityScore() {
        return qualityScore != null ? qualityScore : String.valueOf(score());
    }

    public String summary() {
        return summary;
    }

    public int totalBugsFound() {
        return totalBugsFound;
    }

    public List<Issue> issues() {
        return issues;
    }

    public String correctedCode() {
        return correctedCode;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Issue {
        private Integer lineNumber;
        private String source;
        private String issueType;
        private String severity;
        private String title;
        private String description;
        private String recommendation;
        private String fixCode;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Complexity {
        private String time;
        private String timeComplexity;
        private String timeExplanation;
        private String space;
        private String spaceComplexity;
        private String spaceExplanation;

        public String getTimeComplexity() {
            return timeComplexity != null ? timeComplexity : time;
        }

        public String getSpaceComplexity() {
            return spaceComplexity != null ? spaceComplexity : space;
        }
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Quality {
        private Integer readability;
        private Integer maintainability;
        private Integer reliability;
        private Integer smells;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TestCase {
        private String input;
        private String expected;
        private String purpose;
    }
}