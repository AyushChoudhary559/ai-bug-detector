package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import com.cs.bugdetector.service.CompilerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
@RequiredArgsConstructor
@Slf4j
public class JavaAnalyzer implements LanguageAnalyzer {

    private final CompilerService compilerService;

    // Pattern to match: Main.java:3: error: cannot find symbol
    private static final Pattern ERROR_PATTERN = Pattern.compile("([^:]+):(\\d+):\\s*(error|warning):\\s*(.*)");

    @Override
    public boolean isAvailable() {
        try {
            Process process = new ProcessBuilder("javac", "-version").start();
            return process.waitFor() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String getLanguage() {
        return "java";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        if (!isAvailable()) {
            return new AnalysisResult(false, "UNAVAILABLE: Java compiler not found.", List.of());
        }

        CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"javac", "Main.java"}, sourceCode, "Main.java"
        );

        if (result.isTimeout()) {
            return new AnalysisResult(false, "TIMEOUT", List.of());
        }

        List<Issue> issues = parseOutput(result.output());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues);
    }

    private List<Issue> parseOutput(String output) {
        List<Issue> issues = new ArrayList<>();
        String[] lines = output.split("\\r?\\n");

        for (String line : lines) {
            Matcher m = ERROR_PATTERN.matcher(line);
            if (m.find()) {
                int lineNumber = Integer.parseInt(m.group(2));
                String type = m.group(3).toUpperCase();
                String message = m.group(4);

                issues.add(Issue.builder()
                        .source("COMPILER")
                        .issueType("COMPILATION")
                        .severity(type.equals("ERROR") ? "CRITICAL" : "MEDIUM")
                        .title("Java Compiler " + type)
                        .description(message)
                        .lineNumber(lineNumber)
                        .build());
            }
        }
        return issues;
    }
}
