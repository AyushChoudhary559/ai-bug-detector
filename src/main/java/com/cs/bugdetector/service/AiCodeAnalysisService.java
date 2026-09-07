package com.cs.bugdetector.service;

import com.cs.bugdetector.dto.BugReportResponse;
import com.cs.bugdetector.dto.CodeAnalysisRequest;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.converter.BeanOutputConverter;
import org.springframework.stereotype.Service;

@Service
public class AiCodeAnalysisService {

    private final ChatClient chatClient;

    public AiCodeAnalysisService(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    public BugReportResponse analyzeCode(CodeAnalysisRequest request) {
        // 1. Tell Spring AI what Java class we expect back
        BeanOutputConverter<BugReportResponse> converter = new BeanOutputConverter<>(BugReportResponse.class);

        // 2. The Detailed System Prompt (with Spring AI injecting the JSON schema automatically)
        String systemPrompt = """
            You are an elite Static Application Security Testing (SAST) engine and Senior Software Architect.
            Analyze the code for Syntax Errors, Logical Flaws, Security Vulnerabilities, Resource Leaks, and Performance Bottlenecks.
            
            CRITICAL: You MUST respond ONLY in valid JSON. Do not include markdown code blocks.
            Categorize issueType as: SYNTAX, LOGIC, SECURITY, RESOURCE_LEAK, PERFORMANCE.
            Categorize severity as: CRITICAL, HIGH, MEDIUM, LOW.
            
            {format}
            """;

        // 3. The User Prompt
        String userPrompt = """
            Target Language: %s
            
            Source Code to Analyze:
            %s
            """.formatted(request.getLanguage(), request.getSourceCode());

        // 4. Execute Call and map directly to DTO without errors
        return chatClient.prompt()
                .system(sys -> sys.text(systemPrompt).param("format", converter.getFormat()))
                .user(userPrompt)
                .call()
                .entity(BugReportResponse.class);
    }
}
