package com.cs.bugdetector.service;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class MockStaticAnalysisService {

    private final ObjectMapper mapper = new ObjectMapper();

    public BugReportResponse analyzeMock(CodeAnalysisRequest request) {
        String lang = request.getLanguage().toLowerCase();
        
        String jsonResponse = "";
        
        if (lang.equals("java")) {
            jsonResponse = """
            {
              "score": 45,
              "summary": "The Java codebase contains critical SQL Injection vulnerabilities and logical leaks.",
              "issues": [
                { "lineNumber": 1, "issueType": "SECURITY", "severity": "CRITICAL", "title": "SQL Injection Vector", "description": "Unsafe concatenation.", "recommendation": "Use PreparedStatement.", "fixCode": "PreparedStatement pstmt = conn.prepareStatement(query);" }
              ],
              "complexity": { "time": "O(n)", "timeExplanation": "Linear loop.", "space": "O(1)", "spaceExplanation": "No extra space." },
              "performance": ["Use StringBuilder instead of String concatenation."],
              "quality": { "readability": 80, "maintainability": 40, "reliability": 45, "smells": 2 },
              "testCases": [ { "input": "'admin\\' OR \\'1\\'=\\'1'", "expected": "Exception", "purpose": "Test SQL Injection" } ]
            }
            """;
        } else if (lang.equals("cpp")) {
            jsonResponse = """
            {
              "score": 60,
              "summary": "The C++ code has memory management issues.",
              "issues": [
                { "lineNumber": 1, "issueType": "MEMORY", "severity": "HIGH", "title": "Memory Leak", "description": "Missing delete for dynamically allocated array.", "recommendation": "Use std::vector or delete[] buffer.", "fixCode": "std::vector<char> buffer(1024);" }
              ],
              "complexity": { "time": "O(N^2)", "timeExplanation": "Nested loops.", "space": "O(N)", "spaceExplanation": "Dynamic array." },
              "performance": ["Avoid raw pointers when possible."],
              "quality": { "readability": 60, "maintainability": 50, "reliability": 60, "smells": 1 },
              "testCases": [ { "input": "Large file input", "expected": "Clean exit without memory crash", "purpose": "Leak check" } ]
            }
            """;
        } else {
            jsonResponse = """
            {
              "score": 85,
              "summary": "The Python script is mostly clean but has an IndexError risk.",
              "issues": [
                { "lineNumber": 1, "issueType": "LOGIC", "severity": "MEDIUM", "title": "IndexError Risk", "description": "Accessing element without checking bounds.", "recommendation": "Check list length.", "fixCode": "if len(items) > 5:\\n    val = items[5]" }
              ],
              "complexity": { "time": "O(1)", "timeExplanation": "Direct access.", "space": "O(1)", "spaceExplanation": "None." },
              "performance": [],
              "quality": { "readability": 90, "maintainability": 85, "reliability": 70, "smells": 0 },
              "testCases": [ { "input": "[]", "expected": "Graceful handle", "purpose": "Empty list" } ]
            }
            """;
        }

        try {
            return mapper.readValue(jsonResponse, BugReportResponse.class);
        } catch (Exception e) {
            throw new RuntimeException("Mock parsing failed", e);
        }
    }
}
