import re

def update_bug_report():
    with open('src/main/java/com/cs/bugdetector/dto/BugReportResponse.java', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add executionOutput
    if "private String executionOutput;" not in content:
        content = content.replace("private String compileStatus;", "private String compileStatus;\n    private String executionOutput;")

    with open('src/main/java/com/cs/bugdetector/dto/BugReportResponse.java', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated BugReportResponse")

if __name__ == "__main__":
    update_bug_report()
