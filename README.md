# DevSentry AI 🛡️
> **AI-Powered Code Bug, Security Vulnerability & SAST Analysis Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Java](https://img.shields.io/badge/Java-17%2B-orange.svg)](https://www.oracle.com/java/)
[![Spring AI](https://img.shields.io/badge/Spring%20AI-Framework-green.svg)](https://spring.io/projects/spring-ai)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)

DevSentry AI is a developer-centric Static Application Security Testing (SAST) and code intelligence platform. It analyzes source code in real-time to detect syntax errors, logical bugs, security vulnerabilities (like SQL Injections, XSS, and SSRF), resource leaks, and performance bottlenecks, providing actionable fix recommendations and clean, corrected code.

---

## ✨ Features

- 🔍 **Multi-Vector Bug Analysis**: Detects issues categorized across **SYNTAX**, **LOGIC**, **SECURITY**, **RESOURCE_LEAK**, and **PERFORMANCE**.
- 🚦 **Severity Grading**: Issues are flagged with severity levels: **CRITICAL**, **HIGH**, **MEDIUM**, and **LOW**.
- 📊 **Health & Quality Score**: Instant calculation of codebase quality on a 0–100 scale.
- 💡 **AI Fix Recommendations**: Provides clear, actionable solutions alongside an auto-corrected version of the analyzed code.
- 💻 **Interactive Monaco Code Editor**: Powered by the Monaco Editor engine (the core of VS Code) with full syntax highlighting for Java, Python, C++, and JavaScript.
- 🎨 **Modern Dark UI**: Designed with glassmorphism, responsive grid layout, and Lucide icons for maximum developer productivity.

---

## 🛠️ Technologies Used

### Frontend
- **HTML5 & Vanilla JavaScript**: Lightweight, responsive client logic.
- **Tailwind CSS (CDN)**: Modern utility-first CSS styling and dark theme.
- **Monaco Editor**: High-performance browser-based code editing.
- **Lucide Icons**: Crisp, modern icon set.

### Backend
- **Java 17+**: Robust, strongly-typed backend architecture.
- **Spring Boot & Spring AI**: Enterprise AI orchestration using `ChatClient` and `BeanOutputConverter` for schema-enforced structured JSON output.

---

## 📂 Project Structure

```text
ai-bug-detector/
├── .gitignore                                          # Git ignore configuration
├── README.md                                           # Comprehensive project documentation
├── index.html                                          # Interactive DevSentry AI frontend dashboard
└── src/
    └── main/
        └── java/
            └── com/
                └── cs/
                    └── bugdetector/
                        ├── dto/
                        │   ├── CodeAnalysisRequest.java  # Request DTO (language, sourceCode)
                        │   └── BugReportResponse.java    # Structured Response Record DTO
                        └── service/
                            └── AiCodeAnalysisService.java # Spring AI SAST prompt engine & logic
```

---

## 📋 Requirements & Prerequisites

To run and extend the complete backend service, ensure you have:
- **Java Development Kit (JDK)**: Version 17 or higher.
- **Maven** or **Gradle**: For building the Spring Boot project.
- **Modern Web Browser**: Chrome, Edge, Firefox, or Safari.
- **AI Model Access**: OpenAI, Gemini, or Ollama API key configured with Spring AI.

---

## 🚀 Getting Started & How to Run

### 1. Running the Frontend Dashboard
Simply open `index.html` in your web browser:
```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

### 2. Integrating with Spring AI Backend
1. Include the Java classes in your Spring Boot application under `com.cs.bugdetector`.
2. Configure your AI model provider in `application.yml` (e.g. OpenAI, Azure OpenAI, or Ollama):
   ```yaml
   spring:
     ai:
       openai:
         api-key: ${OPENAI_API_KEY}
         chat:
           options:
             model: gpt-4o
   ```
3. Expose a REST Controller that delegates to `AiCodeAnalysisService`:
   ```java
   @PostMapping("/api/analyze")
   public ResponseEntity<BugReportResponse> analyze(@RequestBody CodeAnalysisRequest request) {
       return ResponseEntity.ok(aiCodeAnalysisService.analyzeCode(request));
   }
   ```

---

## 🖥️ Usage Workflow

1. Select your target programming language (Java, C++, Python, or JavaScript) from the top navigation bar.
2. Paste or type your code into the left editor pane.
3. Click **"Run AI Audit"**.
4. Review the generated **Quality Score**, detected issues list, severity badges, and the **Corrected Code** tab.

---

## 📸 Screenshots

| Feature | Preview |
| :--- | :--- |
| **Main Dashboard & Code Editor** | *Monaco editor with multi-language code input and custom theme* |
| **Audit Results & Quality Score** | *Detailed issue cards with severity, lines, and fix recommendations* |
| **Corrected Code Output** | *Full auto-remediated version of submitted source code* |

---

## 🔮 Future Improvements

- [ ] Add support for multi-file repository scanning and ZIP uploads.
- [ ] Implement automated CI/CD GitHub Action integrations.
- [ ] Add PDF and Markdown export for security compliance reports.
- [ ] Support local offline LLMs via Ollama.

---

## 👤 Author

**Ayush Choudhary**
- GitHub: [@AyushChoudhary559](https://github.com/AyushChoudhary559)

---

## 📄 License

This project is licensed under the MIT License.
