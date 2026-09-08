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
public class PythonAnalyzer implements LanguageAnalyzer {

    private final CompilerService compilerService;

    private static final Pattern LINE_PATTERN = Pattern.compile("File \"[^\"]+\", line (\\d+)");
    private static final Pattern ERROR_PATTERN = Pattern.compile("(\\w+Error): (.*)");

    @Override
    public boolean isAvailable() {
        try {
            return new ProcessBuilder("python", "--version").start().waitFor() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String getLanguage() {
        return "python";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        if (!isAvailable()) return new AnalysisResult(false, "UNAVAILABLE: python not found.", List.of());

        CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"python", "-m", "py_compile", "source.py"}, 
                sourceCode, "source.py"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", parseOutput(result.output()));
    }

    private List<Issue> parseOutput(String output) {
        List<Issue> issues = new ArrayList<>();
        String[] lines = output.split("\\r?\\n");
        
        Integer currentLine = null;
        for (String line : lines) {
            Matcher lm = LINE_PATTERN.matcher(line);
            if (lm.find()) {
                currentLine = Integer.parseInt(lm.group(1));
            }
            
            Matcher em = ERROR_PATTERN.matcher(line);
            if (em.find() && currentLine != null) {
                issues.add(Issue.builder()
                        .source("COMPILER")
                        .issueType("SYNTAX")
                        .severity("CRITICAL")
                        .title("Python " + em.group(1))
                        .description(em.group(2))
                        .lineNumber(currentLine)
                        .build());
                currentLine = null; // Reset for next error
            }
        }
        return issues;
    }
}
