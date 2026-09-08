package com.cs.bugdetector.controller;

import com.cs.bugdetector.service.analyzers.LanguageAnalyzer;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequiredArgsConstructor
public class HealthController {

    private final List<LanguageAnalyzer> analyzers;

    @GetMapping("/api/health/toolchain")
    public ResponseEntity<?> getToolchainHealth() {
        Map<String, Object> toolStatus = new HashMap<>();

        for (LanguageAnalyzer analyzer : analyzers) {
            Map<String, Object> details = new HashMap<>();
            details.put("available", analyzer.isAvailable());
            details.put("type", analyzer.getClass().getSimpleName());
            toolStatus.put(analyzer.getLanguage(), details);
        }

        return ResponseEntity.ok(toolStatus);
    }
}
