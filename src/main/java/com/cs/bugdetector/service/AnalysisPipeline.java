package com.cs.bugdetector.service;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.BugReportResponse.Issue;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import com.cs.bugdetector.service.analyzers.LanguageAnalyzer;
import com.cs.bugdetector.service.analyzers.LanguageAnalyzer.AnalysisResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class AnalysisPipeline {

    private final List<LanguageAnalyzer> analyzers;
    private final AiCodeAnalysisService aiService;
    private final MockStaticAnalysisService mockService;

    public BugReportResponse runPipeline(CodeAnalysisRequest request) {
        String lang = request.getLanguage() != null ? request.getLanguage().toLowerCase() : "java";

        // 1. Find Appropriate Static/Compiler Analyzer
        Optional<LanguageAnalyzer> analyzerOpt = analyzers.stream()
                .filter(a -> a.getLanguage().equals(lang))
                .findFirst();

        AnalysisResult staticResult = null;
        if (analyzerOpt.isPresent()) {
            LanguageAnalyzer analyzer = analyzerOpt.get();
            try {
                staticResult = analyzer.analyze(request.getSourceCode());
            } catch (Exception e) {
                log.error("Static analysis failed for " + lang, e);
            }
        }

        // 2. Run AI Analysis
        BugReportResponse aiResponse;
        try {
            aiResponse = aiService.analyzeCode(request);
            if (aiResponse == null || aiResponse.getIssues() == null) {
                throw new IllegalStateException("AI response returned empty result");
            }
        } catch (Exception e) {
            log.info("AI service unavailable. Using mock static engine. Details: {}", e.getMessage());
            aiResponse = mockService.analyzeMock(request);
        }

        // 3. Aggregate Results
        return aggregateResults(staticResult, aiResponse);
    }

    private BugReportResponse aggregateResults(AnalysisResult staticResult, BugReportResponse aiResponse) {
        if (staticResult != null) {
            aiResponse.setCompileStatus(staticResult.compileStatus());

            // Merge static issues into the overall issues list
            List<Issue> mergedIssues = new ArrayList<>();
            
            // Prioritize static/compiler errors
            if (staticResult.issues() != null) {
                mergedIssues.addAll(staticResult.issues());
            }

            // Then add AI issues, making sure they are marked as AI
            if (aiResponse.getIssues() != null) {
                for (Issue aiIssue : aiResponse.getIssues()) {
                    if (aiIssue.getSource() == null || aiIssue.getSource().isEmpty()) {
                        aiIssue.setSource("AI");
                    }
                    mergedIssues.add(aiIssue);
                }
            }
            aiResponse.setIssues(mergedIssues);

            // Re-calculate Score based on critical compiler issues
            long criticalCompilerErrors = mergedIssues.stream()
                .filter(i -> "COMPILER".equals(i.getSource()) && "CRITICAL".equals(i.getSeverity()))
                .count();

            if (criticalCompilerErrors > 0 && aiResponse.getScore() != null) {
                int newScore = Math.max(0, aiResponse.getScore() - (int)(criticalCompilerErrors * 15));
                aiResponse.setScore(newScore);
            }
        } else {
            aiResponse.setCompileStatus("SKIPPED: No toolchain configured");
            if (aiResponse.getIssues() != null) {
                aiResponse.getIssues().forEach(i -> {
                    if(i.getSource() == null) i.setSource("AI");
                });
            }
        }
        return aiResponse;
    }
}
