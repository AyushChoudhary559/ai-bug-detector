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

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/audits")
@RequiredArgsConstructor
public class AuditHistoryController {

    private final AuditRecordRepository auditRecordRepository;
    private final UserRepository userRepository;

    @GetMapping
    public ResponseEntity<?> getUserAudits() {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        if (!(principal instanceof UserDetails)) {
            return ResponseEntity.status(401).body("Unauthorized");
        }
        String username = ((UserDetails) principal).getUsername();
        User user = userRepository.findByUsername(username).orElse(null);
        if (user == null) {
            return ResponseEntity.status(401).body("Unauthorized");
        }

        List<AuditRecord> records = auditRecordRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
        return ResponseEntity.ok(records);
    }
    
    @GetMapping("/stats")
    public ResponseEntity<?> getStats() {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        if (!(principal instanceof UserDetails)) return ResponseEntity.status(401).body("Unauthorized");
        String username = ((UserDetails) principal).getUsername();
        User user = userRepository.findByUsername(username).orElse(null);
        if (user == null) return ResponseEntity.status(401).body("Unauthorized");

        long total = auditRecordRepository.countByUserId(user.getId());
        List<AuditRecord> records = auditRecordRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
        
        double avgScore = records.stream().mapToInt(AuditRecord::getScore).average().orElse(0.0);
        
        return ResponseEntity.ok(Map.of(
            "totalAudits", total,
            "averageScore", Math.round(avgScore),
            "recent", records.size() > 0 ? records.get(0) : null
        ));
    }
}
