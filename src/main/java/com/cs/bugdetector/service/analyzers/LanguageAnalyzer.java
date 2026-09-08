package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import java.util.List;

public interface LanguageAnalyzer {
    boolean isAvailable();
    String getLanguage();
    AnalysisResult analyze(String sourceCode);

    record AnalysisResult(boolean compileSuccess, String compileStatus, List<Issue> issues, String executionOutput) {}
}
