package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import com.cs.bugdetector.service.CompilerService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
@RequiredArgsConstructor
public class JsAnalyzer implements LanguageAnalyzer {

    private final CompilerService compilerService;

    // node --check output
    private static final Pattern ERROR_PATTERN = Pattern.compile("([^:]+):(\\d+)\\s*(.*)");

    @Override
    public boolean isAvailable() {
        try {
            return new ProcessBuilder("node", "--version").start().waitFor() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String getLanguage() {
        return "javascript";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        if (!isAvailable()) return new AnalysisResult(false, "UNAVAILABLE: node.js not found.", List.of(), "");

        CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"node", "source.js"}, 
                sourceCode, "source.js"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");

        List<Issue> issues = new ArrayList<>();
        if (!result.success()) {
             issues.add(Issue.builder()
                .source("COMPILER")
                .issueType("SYNTAX")
                .severity("CRITICAL")
                .title("JavaScript Error")
                .description(result.output().length() > 500 ? result.output().substring(0, 500) + "..." : result.output())
                .build());
        }

        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, result.success() ? result.output() : "");
    }
}
