import re

def update_controller():
    with open('src/main/java/com/cs/bugdetector/controller/AuditController.java', 'r', encoding='utf-8') as f:
        content = f.read()

    # Import pipeline
    content = content.replace("import com.cs.bugdetector.service.MockStaticAnalysisService;", "import com.cs.bugdetector.service.MockStaticAnalysisService;\nimport com.cs.bugdetector.service.AnalysisPipeline;")

    # Replace injected services
    old_fields = """    private final AiCodeAnalysisService aiService;
    private final MockStaticAnalysisService mockService;"""
    new_fields = """    private final AnalysisPipeline pipeline;"""
    content = content.replace(old_fields, new_fields)

    # Replace logic
    old_logic = """        BugReportResponse response;
        try {
            // Attempt real AI analysis
            response = aiService.analyzeCode(request);
            if (response == null || response.getIssues() == null) {
                throw new IllegalStateException("AI response returned empty result");
            }
        } catch (Exception e) {
            log.info("AI service unavailable or not configured. Using static analysis engine. Details: {}", e.getMessage());
            response = mockService.analyzeMock(request);
        }"""
    
    new_logic = """        BugReportResponse response = pipeline.runPipeline(request);"""
    content = content.replace(old_logic, new_logic)

    with open('src/main/java/com/cs/bugdetector/controller/AuditController.java', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated AuditController")

if __name__ == "__main__":
    update_controller()
