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
public class CAnalyzer implements LanguageAnalyzer {

    private final CompilerService compilerService;

    // source.c:5:3: error: ...
    private static final Pattern ERROR_PATTERN = Pattern.compile("([^:]+):(\\d+):(\\d+):\\s*(error|warning|note):\\s*(.*)");

    @Override
    public boolean isAvailable() {
        try {
            return new ProcessBuilder("gcc", "--version").start().waitFor() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String getLanguage() {
        return "c";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        if (!isAvailable()) return new AnalysisResult(false, "UNAVAILABLE: gcc not found.", List.of());

        CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"gcc", "-Wall", "-Wextra", "-Wpedantic", "-fsyntax-only", "source.c"}, 
                sourceCode, "source.c"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", parseOutput(result.output()));
    }

    protected List<Issue> parseOutput(String output) {
        List<Issue> issues = new ArrayList<>();
        for (String line : output.split("\\r?\\n")) {
            Matcher m = ERROR_PATTERN.matcher(line);
            if (m.find()) {
                issues.add(Issue.builder()
                        .source("COMPILER")
                        .issueType("COMPILATION")
                        .severity(m.group(4).equalsIgnoreCase("error") ? "CRITICAL" : "MEDIUM")
                        .title("GCC " + m.group(4).toUpperCase())
                        .description(m.group(5))
                        .lineNumber(Integer.parseInt(m.group(2)))
                        .build());
            }
        }
        return issues;
    }
}
