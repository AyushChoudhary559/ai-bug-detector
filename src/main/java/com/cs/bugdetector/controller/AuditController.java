package com.cs.bugdetector.controller;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import com.cs.bugdetector.entity.AuditRecord;
import com.cs.bugdetector.entity.User;
import com.cs.bugdetector.repository.AuditRecordRepository;
import com.cs.bugdetector.repository.UserRepository;
import com.cs.bugdetector.service.AnalysisPipeline;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@Slf4j
public class AuditController {

    private final AnalysisPipeline pipeline;
    private final AuditRecordRepository auditRecordRepository;
    private final UserRepository userRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @PostMapping({"/api/v1/detector/analyze", "/api/audit"})
    public ResponseEntity<?> analyzeCode(@RequestBody CodeAnalysisRequest request) {
        String code = request.getSourceCode();
        if (code == null || code.trim().isEmpty()) {
            return ResponseEntity.badRequest().body("Source code is required");
        }

        User user = null;
        Object principal = SecurityContextHolder.getContext().getAuthentication() != null
                ? SecurityContextHolder.getContext().getAuthentication().getPrincipal()
                : null;

        if (principal instanceof UserDetails userDetails) {
            user = userRepository.findByUsername(userDetails.getUsername()).orElse(null);
        }

        BugReportResponse response = pipeline.runPipeline(request);

        try {
            int score = response.getScore() != null ? response.getScore() : 0;
            int bugsCount = response.getBugs() != null ? response.getBugs().size() : 0;
            int securityCount = response.getSecurityIssues() != null ? response.getSecurityIssues().size() : 0;
            String timeComp = response.getComplexity() != null ? response.getComplexity().getTimeComplexity() : null;
            String spaceComp = response.getComplexity() != null ? response.getComplexity().getSpaceComplexity() : null;

            String jsonRaw = objectMapper.writeValueAsString(response);
            AuditRecord record = AuditRecord.builder()
                    .user(user)
                    .language(request.getLanguage() != null ? request.getLanguage() : "java")
                    .fileName(request.getFileName() != null ? request.getFileName() : "code-snippet")
                    .code(code)
                    .score(score)
                    .status("COMPLETED")
                    .bugsCount(bugsCount)
                    .securityCount(securityCount)
                    .timeComplexity(timeComp)
                    .spaceComplexity(spaceComp)
                    .rawResultJson(jsonRaw)
                    .build();

            AuditRecord saved = auditRecordRepository.save(record);
            response.setAuditId(saved.getId());
            response.setStatus("COMPLETED");
        } catch (Exception e) {
            log.error("Failed to save audit record: {}", e.getMessage());
            response.setStatus("COMPLETED");
        }

        return ResponseEntity.ok(response);
    }
}
