import re

def update_pipeline():
    with open('src/main/java/com/cs/bugdetector/service/AnalysisPipeline.java', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where BugReportResponse is built and add executionOutput
    if "executionOutput" not in content:
        old_block = """response.setCompileStatus(result.compileStatus());
            
            // Apply issues
            response.getIssues().addAll(result.issues());"""
            
        new_block = """response.setCompileStatus(result.compileStatus());
            response.setExecutionOutput(result.executionOutput());
            
            // Apply issues
            response.getIssues().addAll(result.issues());"""
        
        content = content.replace(old_block, new_block)
        
        with open('src/main/java/com/cs/bugdetector/service/AnalysisPipeline.java', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated pipeline")
    else:
        print("Pipeline already updated")

if __name__ == "__main__":
    update_pipeline()
