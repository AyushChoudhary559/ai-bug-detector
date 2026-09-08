package com.cs.bugdetector.service;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class MockStaticAnalysisService {

    public BugReportResponse analyzeMock(CodeAnalysisRequest request) {
        String lang = request.getLanguage() != null ? request.getLanguage().toLowerCase().trim() : "java";
        String code = request.getSourceCode() != null ? request.getSourceCode() : "";

        List<BugReportResponse.Issue> issues = new ArrayList<>();
        List<String> recommendations = new ArrayList<>();
        List<String> performance = new ArrayList<>();

        if ("java".equals(lang)) {
            analyzeJava(code, issues, recommendations, performance);
        } else if ("cpp".equals(lang) || "c++".equals(lang) || "c".equals(lang)) {
            analyzeCpp(code, issues, recommendations, performance);
        } else if ("python".equals(lang) || "py".equals(lang)) {
            analyzePython(code, issues, recommendations, performance);
        } else {
            analyzeGeneric(code, issues, recommendations, performance);
        }

        // Separate issues by category for frontend convenience
        List<BugReportResponse.Issue> bugs = new ArrayList<>();
        List<BugReportResponse.Issue> securityIssues = new ArrayList<>();
        List<BugReportResponse.Issue> performanceIssues = new ArrayList<>();

        int critical = 0, high = 0, medium = 0, low = 0;
        for (BugReportResponse.Issue issue : issues) {
            String type = issue.getIssueType();
            if ("SECURITY".equalsIgnoreCase(type)) {
                securityIssues.add(issue);
            } else if ("PERFORMANCE".equalsIgnoreCase(type) || "RESOURCE_LEAK".equalsIgnoreCase(type)) {
                performanceIssues.add(issue);
            } else {
                bugs.add(issue);
            }

            if ("CRITICAL".equalsIgnoreCase(issue.getSeverity())) critical++;
            else if ("HIGH".equalsIgnoreCase(issue.getSeverity())) high++;
            else if ("MEDIUM".equalsIgnoreCase(issue.getSeverity())) medium++;
            else low++;
        }

        int deduction = (critical * 25) + (high * 15) + (medium * 10) + (low * 5);
        int calculatedScore = issues.isEmpty() ? 96 : Math.max(15, 100 - deduction);

        int maxLoopDepth = calculateLoopDepth(code);
        String timeComplexity = maxLoopDepth == 0 ? "O(1)" : maxLoopDepth == 1 ? "O(n)" : maxLoopDepth == 2 ? "O(n^2)" : "O(n^" + maxLoopDepth + ")";
        String spaceComplexity = code.contains("new ") || code.contains("malloc") || code.contains("[") ? "O(n)" : "O(1)";

        BugReportResponse.Complexity complexity = BugReportResponse.Complexity.builder()
                .time(timeComplexity)
                .timeComplexity(timeComplexity)
                .timeExplanation(maxLoopDepth > 1 ? "Nested iteration loops increase complexity to " + timeComplexity : "Single pass or constant time operations.")
                .space(spaceComplexity)
                .spaceComplexity(spaceComplexity)
                .spaceExplanation(spaceComplexity.equals("O(n)") ? "Memory allocation proportional to input collection." : "Operates in constant auxiliary space.")
                .build();

        BugReportResponse.Quality quality = BugReportResponse.Quality.builder()
                .readability(Math.max(40, 95 - (issues.size() * 5)))
                .maintainability(Math.max(30, 90 - (issues.size() * 8)))
                .reliability(Math.max(25, calculatedScore))
                .smells(issues.size())
                .build();

        List<BugReportResponse.TestCase> testCases = new ArrayList<>();
        if (!securityIssues.isEmpty()) {
            testCases.add(BugReportResponse.TestCase.builder()
                    .input("' OR '1'='1' --")
                    .expected("Rejection / Parameterized query validation")
                    .purpose("SQL Injection bypass test")
                    .build());
        }
        testCases.add(BugReportResponse.TestCase.builder()
                .input("null or empty payload")
                .expected("Graceful validation without NullPointerException")
                .purpose("Edge case validation")
                .build());
        testCases.add(BugReportResponse.TestCase.builder()
                .input("High load / concurrent requests (10,000 req/s)")
                .expected("Bounded memory & resource consumption")
                .purpose("Stress and leak resilience verification")
                .build());

        String summary = issues.isEmpty()
                ? "Code passed static inspection cleanly. No severe bugs, vulnerabilities, or resource leaks were detected."
                : String.format("Audit completed: detected %d issue(s) (%d security, %d performance/resource, %d logic/syntax). Quality score is %d/100.",
                issues.size(), securityIssues.size(), performanceIssues.size(), bugs.size(), calculatedScore);

        return BugReportResponse.builder()
                .language(lang)
                .score(calculatedScore)
                .qualityScore(String.valueOf(calculatedScore))
                .summary(summary)
                .status("COMPLETED")
                .totalBugsFound(issues.size())
                .issues(issues)
                .bugs(bugs)
                .securityIssues(securityIssues)
                .performanceIssues(performanceIssues)
                .recommendations(recommendations)
                .performance(performance)
                .complexity(complexity)
                .quality(quality)
                .testCases(testCases)
                .correctedCode(generateQuickFix(code, lang))
                .build();
    }

    private void analyzeJava(String code, List<BugReportResponse.Issue> issues, List<String> recs, List<String> perf) {
        String[] lines = code.split("\r?\n");
        for (int i = 0; i < lines.length; i++) {
            int lineNum = i + 1;
            String line = lines[i];

            // 1. SQL Injection via string concatenation
            if (Pattern.compile("(?i)(select|insert|update|delete|where)\\s+.*\\+").matcher(line).find() ||
                Pattern.compile("(?i)executeQuery\\s*\\(.*\\+").matcher(line).find()) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("SECURITY")
                        .severity("CRITICAL")
                        .title("SQL Injection Vulnerability")
                        .description("Dynamic SQL query constructed using string concatenation instead of parameterized placeholders.")
                        .recommendation("Use PreparedStatement with parameterized queries (? placeholders).")
                        .fixCode("PreparedStatement stmt = conn.prepareStatement(\"SELECT * FROM users WHERE username = ?\");\nstmt.setString(1, username);")
                        .build());
                recs.add("Sanitize all external parameters and enforce PreparedStatement across all data queries.");
            }

            // 2. Resource leak without try-with-resources
            if (Pattern.compile("\\b(FileInputStream|FileOutputStream|Connection|Statement|ResultSet|BufferedReader)\\s+\\w+\\s*=").matcher(line).find() &&
                !code.contains("try (") && !code.contains("try(")) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("RESOURCE_LEAK")
                        .severity("HIGH")
                        .title("Unclosed Resource Leak")
                        .description("Resource initialized without try-with-resources statement, potentially leaking OS file descriptors or DB connections.")
                        .recommendation("Wrap resource creation in try-with-resources block.")
                        .fixCode("try (var resource = new FileInputStream(file)) {\n    // Use resource safely\n}")
                        .build());
                recs.add("Refactor I/O and database handlers to standard try-with-resources.");
            }

            // 3. Empty catch block
            if (Pattern.compile("catch\\s*\\([^)]+\\)\\s*\\{\\s*\\}").matcher(line).find()) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("LOGIC")
                        .severity("MEDIUM")
                        .title("Empty Catch Block")
                        .description("Exception caught and completely swallowed with no logging or recovery action.")
                        .recommendation("Log the exception or rethrow as a custom runtime exception.")
                        .fixCode("catch (Exception e) {\n    log.error(\"Operation failed\", e);\n    throw new ServiceException(e);\n}")
                        .build());
            }

            // 4. Hardcoded secrets / password
            if (Pattern.compile("(?i)(password|secret|api_?key|jwt_?secret)\\s*=\\s*[\"'][^\"']+[\"']").matcher(line).find()) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("SECURITY")
                        .severity("CRITICAL")
                        .title("Hardcoded Secret / Password")
                        .description("Sensitive credential or secret key stored directly in source code.")
                        .recommendation("Extract secrets into environment variables or secrets manager.")
                        .fixCode("String secret = System.getenv(\"APP_SECRET\");")
                        .build());
            }

            // 5. Inefficient String concatenation in loop
            if ((line.contains("+=") || line.contains(".concat(")) && isInsideLoop(lines, i)) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("PERFORMANCE")
                        .severity("MEDIUM")
                        .title("Inefficient String Concatenation in Loop")
                        .description("String concatenation creates repeated temporary String objects causing excessive GC pressure.")
                        .recommendation("Use StringBuilder for repeated string accumulation.")
                        .fixCode("StringBuilder sb = new StringBuilder();\nsb.append(item);")
                        .build());
                perf.add("Replace String += loops with StringBuilder.");
            }

            // 6. Generic catch Throwable / Exception
            if (Pattern.compile("catch\\s*\\(\\s*(Throwable|Exception)\\s+\\w+\\s*\\)").matcher(line).find() && !line.contains("ServletException")) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("LOGIC")
                        .severity("LOW")
                        .title("Overly Broad Exception Catching")
                        .description("Catching generic Exception or Throwable masks unexpected runtime bugs and Errors.")
                        .recommendation("Catch specific checked exceptions where possible.")
                        .fixCode("catch (IOException | SQLException e) {\n    log.warn(\"Recoverable error: {}\", e.getMessage());\n}")
                        .build());
            }
        }
    }

    private void analyzeCpp(String code, List<BugReportResponse.Issue> issues, List<String> recs, List<String> perf) {
        String[] lines = code.split("\r?\n");
        boolean hasNew = code.contains("new ") || code.contains("malloc(");
        boolean hasDelete = code.contains("delete ") || code.contains("delete[]") || code.contains("free(");

        for (int i = 0; i < lines.length; i++) {
            int lineNum = i + 1;
            String line = lines[i];

            if (Pattern.compile("\\b(gets|strcpy|strcat|sprintf)\\s*\\(").matcher(line).find()) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("SECURITY")
                        .severity("CRITICAL")
                        .title("Unsafe C-String Function")
                        .description("Function does not perform buffer boundary checks and is prone to buffer overflow exploits.")
                        .recommendation("Use std::string or safe functions like snprintf / strncpy.")
                        .fixCode("snprintf(buffer, sizeof(buffer), \"%s\", input);")
                        .build());
            }

            if ((line.contains("new ") || line.contains("malloc(")) && (!hasDelete)) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("RESOURCE_LEAK")
                        .severity("HIGH")
                        .title("Memory Leak Detected")
                        .description("Dynamic heap memory allocated without corresponding delete / free statement.")
                        .recommendation("Adopt smart pointers (std::unique_ptr or std::shared_ptr) or RAII containers.")
                        .fixCode("auto buffer = std::make_unique<char[]>(1024);")
                        .build());
                recs.add("Modernize memory management using C++17 smart pointers.");
            }
        }
    }

    private void analyzePython(String code, List<BugReportResponse.Issue> issues, List<String> recs, List<String> perf) {
        String[] lines = code.split("\r?\n");
        for (int i = 0; i < lines.length; i++) {
            int lineNum = i + 1;
            String line = lines[i];

            if (line.trim().startsWith("except:")) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("LOGIC")
                        .severity("MEDIUM")
                        .title("Bare Except Clause")
                        .description("Bare except intercepts SystemExit and KeyboardInterrupt, preventing graceful process termination.")
                        .recommendation("Catch specific exceptions like except Exception: or specific subclasses.")
                        .fixCode("except Exception as e:\n    logger.error(f'Error: {e}')")
                        .build());
            }

            if (Pattern.compile("open\\s*\\([^)]+\\)").matcher(line).find() && !line.contains("with ")) {
                issues.add(BugReportResponse.Issue.builder()
                        .lineNumber(lineNum)
                        .issueType("RESOURCE_LEAK")
                        .severity("MEDIUM")
                        .title("Unmanaged File Handle")
                        .description("File opened without context manager ('with open(...) as f:'). File descriptor may stay open upon exceptions.")
                        .recommendation("Use Python context manager ('with open(...) as f:').")
                        .fixCode("with open(filename, 'r') as f:\n    content = f.read()")
                        .build());
            }
        }
    }

    private void analyzeGeneric(String code, List<BugReportResponse.Issue> issues, List<String> recs, List<String> perf) {
        if (code.contains("TODO") || code.contains("FIXME")) {
            issues.add(BugReportResponse.Issue.builder()
                    .lineNumber(1)
                    .issueType("LOGIC")
                    .severity("LOW")
                    .title("Unresolved TODO/FIXME annotations")
                    .description("Code contains incomplete implementation notes.")
                    .recommendation("Address pending TODO items before merging to production.")
                    .fixCode("// Implementation completed")
                    .build());
        }
    }

    private boolean isInsideLoop(String[] lines, int currentIndex) {
        for (int i = Math.max(0, currentIndex - 15); i <= currentIndex; i++) {
            String l = lines[i].trim();
            if (l.startsWith("for ") || l.startsWith("for(") || l.startsWith("while ") || l.startsWith("while(")) {
                return true;
            }
        }
        return false;
    }

    private int calculateLoopDepth(String code) {
        int depth = 0;
        int max = 0;
        for (String line : code.split("\r?\n")) {
            String t = line.trim();
            if (t.startsWith("for ") || t.startsWith("for(") || t.startsWith("while ") || t.startsWith("while(")) {
                depth++;
                if (depth > max) max = depth;
            }
            if (t.endsWith("}") && depth > 0) {
                depth--;
            }
        }
        return max;
    }

    private String generateQuickFix(String originalCode, String lang) {
        if (originalCode.contains("SELECT") && originalCode.contains("+")) {
            return originalCode.replaceFirst("(?i)String query = \"SELECT.*\\+.*",
                    "String query = \"SELECT * FROM users WHERE username = ?\";\nPreparedStatement pstmt = conn.prepareStatement(query);\npstmt.setString(1, username);");
        }
        return originalCode;
    }
}