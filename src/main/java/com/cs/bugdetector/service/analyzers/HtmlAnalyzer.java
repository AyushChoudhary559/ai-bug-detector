package com.cs.bugdetector.service.analyzers;

import com.cs.bugdetector.dto.BugReportResponse.Issue;
import org.jsoup.Jsoup;
import org.jsoup.parser.ParseError;
import org.jsoup.parser.Parser;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class HtmlAnalyzer implements LanguageAnalyzer {

    @Override
    public boolean isAvailable() {
        return true; // Using embedded JSoup
    }

    @Override
    public String getLanguage() {
        return "html";
    }

    @Override
    public AnalysisResult analyze(String sourceCode) {
        Parser parser = Parser.htmlParser().setTrackErrors(20);
        Jsoup.parse(sourceCode, "", parser);

        List<Issue> issues = new ArrayList<>();
        
        for (ParseError error : parser.getErrors()) {
            issues.add(Issue.builder()
                    .source("STATIC_ANALYZER")
                    .issueType("SYNTAX")
                    .severity("MEDIUM")
                    .title("HTML Validation Error")
                    .description(error.getErrorMessage())
                    .build()); // JSoup 1.17 doesn't easily expose line numbers for errors in a simple way without positional mapping, so we'll leave it out for simplicity unless we dig deeper.
        }

        boolean success = issues.isEmpty();
        return new AnalysisResult(success, success ? "PASSED" : "FAILED", issues);
    }
}
