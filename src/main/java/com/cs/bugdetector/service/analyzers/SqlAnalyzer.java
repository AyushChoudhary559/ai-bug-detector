package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import net.sf.jsqlparser.JSQLParserException;
import net.sf.jsqlparser.parser.CCJSqlParserUtil;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class SqlAnalyzer implements LanguageAnalyzer {

    @Override
    public boolean isAvailable() {
        return true; // Embedded JSqlParser
    }

    @Override
    public String getLanguage() {
        return "sql";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        List<Issue> issues = new ArrayList<>();
        
        try {
            // JSqlParser can parse multiple statements if we split or parse statements
            CCJSqlParserUtil.parseStatements(sourceCode);
        } catch (JSQLParserException e) {
            String message = e.getMessage();
            issues.add(Issue.builder()
                    .source("STATIC_ANALYZER")
                    .issueType("SYNTAX")
                    .severity("CRITICAL")
                    .title("SQL Syntax Error")
                    .description(message != null && message.length() > 300 ? message.substring(0, 300) + "..." : message)
                    .build());
        }

        boolean success = issues.isEmpty();
        return new AnalysisResult(success, success ? "PASSED" : "FAILED", issues, "Valid SQL Syntax");
    }
}
