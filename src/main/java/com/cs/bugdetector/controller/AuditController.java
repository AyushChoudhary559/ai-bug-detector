package com.cs.bugdetector.controller;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import com.cs.bugdetector.entity.AuditRecord;
import com.cs.bugdetector.entity.User;
import com.cs.bugdetector.repository.AuditRecordRepository;
import com.cs.bugdetector.repository.UserRepository;
import com.cs.bugdetector.service.AiCodeAnalysisService;
import com.cs.bugdetector.service.MockStaticAnalysisService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/detector")
@RequiredArgsConstructor
@Slf4j
public class AuditController {

    private final AiCodeAnalysisService aiService;
    private final MockStaticAnalysisService mockService;
    private final AuditRecordRepository auditRecordRepository;
    private final UserRepository userRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @PostMapping("/analyze")
    public ResponseEntity<?> analyzeCode(@RequestBody CodeAnalysisRequest request) {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = null;
        if (principal instanceof UserDetails) {
            String username = ((UserDetails) principal).getUsername();
            user = userRepository.findByUsername(username).orElse(null);
        }

        if (user == null) {
            return ResponseEntity.status(401).body("Unauthorized");
        }

        BugReportResponse response;
        try {
            // Attempt real AI analysis
            response = aiService.analyzeCode(request);
        } catch (Exception e) {
            log.warn("Real AI API failed, using mock provider. Error: {}", e.getMessage());
            response = mockService.analyzeMock(request);
        }

        try {
            String jsonRaw = objectMapper.writeValueAsString(response);
            AuditRecord record = AuditRecord.builder()
                    .user(user)
                    .language(request.getLanguage())
                    .fileName("Unknown")
                    .code(request.getSourceCode())
                    .score(response.getScore())
                    .status("COMPLETED")
                    .rawResultJson(jsonRaw)
                    .build();
            auditRecordRepository.save(record);
        } catch (Exception e) {
            log.error("Failed to save audit record", e);
        }

        return ResponseEntity.ok(response);
    }
}
