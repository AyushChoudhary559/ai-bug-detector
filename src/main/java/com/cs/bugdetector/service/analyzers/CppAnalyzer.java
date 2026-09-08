package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import com.cs.bugdetector.service.CompilerService;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class CppAnalyzer extends CAnalyzer {

    private final CompilerService compilerService;

    public CppAnalyzer(CompilerService compilerService) {
        super(compilerService);
        this.compilerService = compilerService;
    }

    @Override
    public boolean isAvailable() {
        try {
            return new ProcessBuilder("g++", "--version").start().waitFor() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String getLanguage() {
        return "cpp";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        if (!isAvailable()) return new AnalysisResult(false, "UNAVAILABLE: g++ not found.", List.of(), "");

        CompilerService.CompilerResult result = compilerService.executeMultipleCommands(
                new String[][]{{"g++", "-Wall", "-Wextra", "-Wpedantic", "source.cpp", "-o", "out.exe"}, {"./out.exe"}}, 
                sourceCode, "source.cpp"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");
        
        List<Issue> issues = parseOutput(result.output());
        String out = result.success() ? result.output() : "";
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, out);
    }
}
