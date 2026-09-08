package com.cs.bugdetector.controller;

import com.cs.bugdetector.entity.AuditRecord;
import com.cs.bugdetector.entity.User;
import com.cs.bugdetector.repository.AuditRecordRepository;
import com.cs.bugdetector.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequiredArgsConstructor
public class AuditHistoryController {

    private final AuditRecordRepository auditRecordRepository;
    private final UserRepository userRepository;

    private User getAuthenticatedUser() {
        if (SecurityContextHolder.getContext().getAuthentication() == null) return null;
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        if (principal instanceof UserDetails userDetails) {
            return userRepository.findByUsername(userDetails.getUsername()).orElse(null);
        }
        return null;
    }

    @GetMapping("/api/audits")
    public ResponseEntity<?> getUserAudits() {
        User user = getAuthenticatedUser();
        List<AuditRecord> records;
        if (user != null) {
            records = auditRecordRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
        } else {
            // Return recent public/guest audits or empty list
            records = auditRecordRepository.findAll().stream()
                    .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
                    .limit(20)
                    .toList();
        }
        return ResponseEntity.ok(records);
    }

    @GetMapping("/api/audits/{id}")
    public ResponseEntity<?> getAuditById(@PathVariable Long id) {
        Optional<AuditRecord> recordOpt = auditRecordRepository.findById(id);
        if (recordOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        AuditRecord record = recordOpt.get();
        User user = getAuthenticatedUser();
        if (record.getUser() != null && user != null && !record.getUser().getId().equals(user.getId())) {
            return ResponseEntity.status(403).body(Map.of("error", "Access denied to this audit record"));
        }

        return ResponseEntity.ok(record);
    }

    @DeleteMapping("/api/audits/{id}")
    public ResponseEntity<?> deleteAuditById(@PathVariable Long id) {
        Optional<AuditRecord> recordOpt = auditRecordRepository.findById(id);
        if (recordOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        AuditRecord record = recordOpt.get();
        User user = getAuthenticatedUser();
        if (record.getUser() != null && user != null && !record.getUser().getId().equals(user.getId())) {
            return ResponseEntity.status(403).body(Map.of("error", "Access denied"));
        }

        auditRecordRepository.delete(record);
        return ResponseEntity.ok(Map.of("success", true, "message", "Audit record deleted successfully"));
    }

    @GetMapping({"/api/dashboard/stats", "/api/audits/stats"})
    public ResponseEntity<?> getDashboardStats() {
        User user = getAuthenticatedUser();
        List<AuditRecord> records;
        if (user != null) {
            records = auditRecordRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
        } else {
            records = auditRecordRepository.findAll();
        }

        long total = records.size();
        double avgScore = records.stream().mapToInt(r -> r.getScore() != null ? r.getScore() : 0).average().orElse(0.0);
        long bugsFound = records.stream().mapToLong(r -> r.getBugsCount() != null ? r.getBugsCount() : 0).sum();
        long securityIssues = records.stream().mapToLong(r -> r.getSecurityCount() != null ? r.getSecurityCount() : 0).sum();

        Map<String, Object> stats = new HashMap<>();
        stats.put("totalAudits", total);
        stats.put("averageScore", Math.round(avgScore));
        stats.put("bugsFound", bugsFound);
        stats.put("securityIssues", securityIssues);
        stats.put("recentAudits", records.stream().limit(5).toList());

        return ResponseEntity.ok(stats);
    }

    @GetMapping("/api/reports/{auditId}")
    public ResponseEntity<?> getReport(@PathVariable Long auditId) {
        Optional<AuditRecord> recordOpt = auditRecordRepository.findById(auditId);
        if (recordOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        AuditRecord record = recordOpt.get();

        Map<String, Object> report = new HashMap<>();
        report.put("auditId", record.getId());
        report.put("language", record.getLanguage());
        report.put("fileName", record.getFileName());
        report.put("score", record.getScore());
        report.put("status", record.getStatus());
        report.put("createdAt", record.getCreatedAt());
        report.put("codeLength", record.getCode() != null ? record.getCode().length() : 0);
        report.put("timeComplexity", record.getTimeComplexity());
        report.put("spaceComplexity", record.getSpaceComplexity());
        report.put("rawResult", record.getRawResultJson());

        return ResponseEntity.ok(report);
    }
}