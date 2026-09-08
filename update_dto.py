import re

def update_dto():
    with open('src/main/java/com/cs/bugdetector/dto/BugReportResponse.java', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add compileStatus
    if "private String compileStatus;" not in content:
        content = content.replace("private String status;", "private String status;\n    private String compileStatus;")

    # Add source to Issue
    if "private String source;" not in content:
        content = content.replace("private Integer lineNumber;", "private Integer lineNumber;\n        private String source;")

    with open('src/main/java/com/cs/bugdetector/dto/BugReportResponse.java', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated BugReportResponse")

if __name__ == "__main__":
    update_dto()
