import re
import os

def update_analyzer_interface():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/LanguageAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "String executionOutput" not in content:
        content = content.replace("record AnalysisResult(boolean compileSuccess, String compileStatus, List<Issue> issues) {}", 
                                  "record AnalysisResult(boolean compileSuccess, String compileStatus, List<Issue> issues, String executionOutput) {}")
        with open('src/main/java/com/cs/bugdetector/service/analyzers/LanguageAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_java():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/JavaAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"javac", "Main.java"}, sourceCode, "Main.java"
        );

        if (result.isTimeout()) {
            return new AnalysisResult(false, "TIMEOUT", List.of());
        }

        List<Issue> issues = parseOutput(result.output());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues);"""
    
    new_call = """CompilerService.CompilerResult result = compilerService.executeMultipleCommands(
                new String[][]{{"javac", "Main.java"}, {"java", "Main"}}, sourceCode, "Main.java"
        );

        if (result.isTimeout()) {
            return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");
        }

        List<Issue> issues = parseOutput(result.output());
        String out = result.success() ? result.output() : (issues.isEmpty() ? result.output() : "");
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, out);"""
    
    if "executeMultipleCommands" not in content:
        content = content.replace(old_call, new_call)
        with open('src/main/java/com/cs/bugdetector/service/analyzers/JavaAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_python():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/PythonAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()

    old_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"python", "-m", "py_compile", "source.py"}, 
                sourceCode, "source.py"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", parseOutput(result.output()));"""
    
    new_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"python", "source.py"}, 
                sourceCode, "source.py"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");
        
        List<Issue> issues = parseOutput(result.output());
        String out = issues.isEmpty() ? result.output() : "";
        return new AnalysisResult(issues.isEmpty(), issues.isEmpty() ? "PASSED" : "FAILED", issues, out);"""
    
    if 'new String[]{"python", "source.py"}' not in content:
        content = content.replace(old_call, new_call)
        with open('src/main/java/com/cs/bugdetector/service/analyzers/PythonAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_c():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/CAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"gcc", "-Wall", "-Wextra", "-Wpedantic", "-fsyntax-only", "source.c"}, 
                sourceCode, "source.c"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", parseOutput(result.output()));"""
    
    new_call = """CompilerService.CompilerResult result = compilerService.executeMultipleCommands(
                new String[][]{{"gcc", "-Wall", "-Wextra", "-Wpedantic", "source.c", "-o", "out.exe"}, {"./out.exe"}}, 
                sourceCode, "source.c"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");
        
        List<Issue> issues = parseOutput(result.output());
        String out = result.success() ? result.output() : "";
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, out);"""
    
    if "out.exe" not in content:
        content = content.replace(old_call, new_call)
        with open('src/main/java/com/cs/bugdetector/service/analyzers/CAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_cpp():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/CppAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"g++", "-Wall", "-Wextra", "-Wpedantic", "-fsyntax-only", "source.cpp"}, 
                sourceCode, "source.cpp"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", parseOutput(result.output()));"""
    
    new_call = """CompilerService.CompilerResult result = compilerService.executeMultipleCommands(
                new String[][]{{"g++", "-Wall", "-Wextra", "-Wpedantic", "source.cpp", "-o", "out.exe"}, {"./out.exe"}}, 
                sourceCode, "source.cpp"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");
        
        List<Issue> issues = parseOutput(result.output());
        String out = result.success() ? result.output() : "";
        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, out);"""
    
    if "out.exe" not in content:
        content = content.replace(old_call, new_call)
        with open('src/main/java/com/cs/bugdetector/service/analyzers/CppAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_js():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/JsAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"node", "--check", "source.js"}, 
                sourceCode, "source.js"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of());

        List<Issue> issues = new ArrayList<>();
        if (!result.success()) {
             issues.add(Issue.builder()
                .source("COMPILER")
                .issueType("SYNTAX")
                .severity("CRITICAL")
                .title("JavaScript Syntax Error")
                .description(result.output().length() > 500 ? result.output().substring(0, 500) + "..." : result.output())
                .build());
        }

        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues);"""
    
    new_call = """CompilerService.CompilerResult result = compilerService.executeWithTimeout(
                new String[]{"node", "source.js"}, 
                sourceCode, "source.js"
        );

        if (result.isTimeout()) return new AnalysisResult(false, "TIMEOUT", List.of(), "Execution Timed Out (>10s)");

        List<Issue> issues = new ArrayList<>();
        if (!result.success()) {
             issues.add(Issue.builder()
                .source("COMPILER")
                .issueType("SYNTAX")
                .severity("CRITICAL")
                .title("JavaScript Error")
                .description(result.output().length() > 500 ? result.output().substring(0, 500) + "..." : result.output())
                .build());
        }

        return new AnalysisResult(result.success(), result.success() ? "PASSED" : "FAILED", issues, result.success() ? result.output() : "");"""
    
    if 'new String[]{"node", "source.js"}' not in content:
        content = content.replace(old_call, new_call)
        with open('src/main/java/com/cs/bugdetector/service/analyzers/JsAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_html():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/HtmlAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues);" in content:
        content = content.replace("return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues);",
                                  "return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues, \"Valid HTML Document\");")
        with open('src/main/java/com/cs/bugdetector/service/analyzers/HtmlAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def update_sql():
    with open('src/main/java/com/cs/bugdetector/service/analyzers/SqlAnalyzer.java', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues);" in content:
        content = content.replace("return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues);",
                                  "return new AnalysisResult(success, success ? \"PASSED\" : \"FAILED\", issues, \"Valid SQL Syntax\");")
        with open('src/main/java/com/cs/bugdetector/service/analyzers/SqlAnalyzer.java', 'w', encoding='utf-8') as f:
            f.write(content)

def fix_return_types():
    for file in ["JavaAnalyzer.java", "PythonAnalyzer.java", "CAnalyzer.java", "CppAnalyzer.java", "JsAnalyzer.java", "HtmlAnalyzer.java", "SqlAnalyzer.java"]:
        path = f"src/main/java/com/cs/bugdetector/service/analyzers/{file}"
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace occurrences of List.of() being returned with List.of(), ""
        content = content.replace('List.of());', 'List.of(), "");')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    update_analyzer_interface()
    update_java()
    update_python()
    update_c()
    update_cpp()
    update_js()
    update_html()
    update_sql()
    fix_return_types()
    print("Updated all analyzers")
