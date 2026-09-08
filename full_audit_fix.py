import os
import re

def fix_frontend():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove forceMock entirely
    content = content.replace("function runAudit(forceMock = false) {", "function runAudit() {")
    content = content.replace("runAudit(forceMock = false)", "runAudit()")
    content = content.replace("if (forceMock) {", "if (false) {")

    # Clean up mock logic in showEmpty/runAudit if possible
    # We will just replace generateMockData with throwing an error or completely empty it out.
    mock_func_pattern = re.compile(r'generateMockData\(lang,\s*code\)\s*\{.*?(?=\n\s*//|[a-zA-Z]+\(\)\s*\{)', re.DOTALL)
    content = re.sub(mock_func_pattern, '', content)

    # 2. Fix Default Templates
    template_block_old = r"""templates: {
                    java: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello DevSentry AI");
    }
}`,
                    c: `#include <stdio.h>
int main() {
    printf("Hello DevSentry AI\\n");
    return 0;
}`,
                    cpp: `#include <iostream>
int main() {
    std::cout << "Hello DevSentry AI\\n";
    return 0;
}`,
                    python: `print("Hello DevSentry AI")`,
                    javascript: `console.log("Hello DevSentry AI");`,
                    html: `<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>Hello DevSentry AI</h1></body>
</html>`,
                    sql: `SELECT * FROM users;`
                },"""
                
    template_block_new = """templates: {
                    java: `public class Main {\\n    public static void main(String[] args) {\\n        System.out.println("Hello DevSentry AI");\\n    }\\n}`,
                    c: `#include <stdio.h>\\n\\nint main() {\\n    printf("Hello DevSentry AI\\\\n");\\n    return 0;\\n}`,
                    cpp: `#include <iostream>\\n\\nint main() {\\n    std::cout << "Hello DevSentry AI\\\\n";\\n    return 0;\\n}`,
                    python: `print("Hello DevSentry AI")`,
                    javascript: `console.log("Hello DevSentry AI");`,
                    html: `<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Test</title>\\n</head>\\n<body>\\n    <h1>Hello DevSentry AI</h1>\\n</body>\\n</html>`,
                    sql: `SELECT * FROM users WHERE active = 1;`
                },"""
    
    # We will just replace it if we find the `templates: {` block
    # Actually, it's easier to just use regex to replace the whole templates dict.
    content = re.sub(r'templates:\s*\{.*?(?=\n\s*\},)', template_block_new, content, flags=re.DOTALL)

    # 3. Fix highlightLine and applyFixCode
    apply_fix_old = """applyFixCode(codeToApply, issueId) {
                this.showAlert("Review Fix", "For safety, please copy the suggested fix and paste it into the exact line.", "alert-circle", "brand");
                if(issueId) this.showFixUI(issueId);
            },"""
    
    apply_fix_new = """applyFixCode(fixCode, lineNumber, issueId) {
                if (!this.editor) return;
                const model = this.editor.getModel();
                if (!model) return;
                
                if (lineNumber && lineNumber > 0 && lineNumber <= model.getLineCount()) {
                    // Replace the specific line
                    const lineContent = model.getLineContent(lineNumber);
                    const range = new monaco.Range(lineNumber, 1, lineNumber, lineContent.length + 1);
                    this.editor.executeEdits("DevSentry Fix", [{ range: range, text: fixCode, forceMoveMarkers: true }]);
                } else {
                    // Replace whole file if no line number or if it's a global fix
                    this.editor.setValue(fixCode);
                }
                
                this.showAlert("Fix Applied", "The suggested code has been applied.", "check-circle", "success");
            },"""
            
    content = content.replace(apply_fix_old, apply_fix_new)
    
    # Update HTML to call applyFixCode properly
    fix_btn_old = """<div class="bg-charcoal-900 text-ivory-50 p-4 rounded-sm font-mono text-sm overflow-x-auto shadow-panel">
                            <pre><code>${fixCodeSafe}</code></pre>
                        </div>` : ''}"""
                        
    fix_btn_new = """<div class="bg-charcoal-900 text-ivory-50 p-4 rounded-sm font-mono text-sm overflow-x-auto shadow-panel relative group">
                            <button onclick="app.applyFixCode(\`${issue.fixCode ? issue.fixCode.replace(/\`/g, '\\\\`').replace(/\\$/g, '\\\\$') : ''}\`, ${issue.lineNumber || 'null'})" class="absolute top-2 right-2 bg-brand-500 hover:bg-brand-600 text-white text-xs px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition">Apply Fix</button>
                            <pre><code>${fixCodeSafe}</code></pre>
                        </div>` : ''}"""
    content = content.replace(fix_btn_old, fix_btn_new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
def fix_backend():
    pipeline_path = 'src/main/java/com/cs/bugdetector/service/AnalysisPipeline.java'
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace Mock static analysis entirely
    content = content.replace("private final MockStaticAnalysisService mockService;", "")
    
    # Replace catch block
    catch_old = """} catch (Exception e) {
            log.info("AI service unavailable. Using mock static engine. Details: {}", e.getMessage());
            aiResponse = mockService.analyzeMock(request);
        }"""
        
    catch_new = """} catch (Exception e) {
            log.info("AI service unavailable or failed. Details: {}", e.getMessage());
            aiResponse = new BugReportResponse();
            aiResponse.setLanguage(lang);
            aiResponse.setSummary("AI analysis unavailable. Displaying toolchain results only.");
            aiResponse.setScore(0);
        }"""
        
    content = content.replace(catch_old, catch_new)
    
    with open(pipeline_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_frontend()
    fix_backend()
    print("Full audit fixes applied.")
