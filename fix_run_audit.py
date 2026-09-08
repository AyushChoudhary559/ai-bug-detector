import re

def fix_run_audit():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the runAudit method and replace it
    pattern = re.compile(r'async runAudit\(\) \{.*?(?=showEmpty\(\) \{)', re.DOTALL)
    
    new_run_audit = """async runAudit() {
                if (this.isAuditing) return;
                if (!this.editor) return;

                const code = this.editor.getValue();
                if (!code.trim()) { 
                    this.showAlert("No code detected", "Please paste your code before starting the audit.", "alert-circle", "rose");
                    return; 
                }

                const langSelect = document.getElementById('language-select');
                const lang = langSelect ? langSelect.value : 'java';

                this.isAuditing = true;
                ['audit-empty', 'audit-error', 'audit-results'].forEach(id => { const el = document.getElementById(id); if (el) el.classList.add('hidden'); });
                document.getElementById('audit-loading').classList.remove('hidden');
                
                const btnRun = document.getElementById('btn-run-audit');
                const btnRunText = document.getElementById('btn-run-text');
                if(btnRun) btnRun.disabled = true;
                if(btnRunText) btnRunText.textContent = "Analyzing...";
                lucide.createIcons();

                try {
                    let data;
                    const headers = { 'Content-Type': 'application/json' };
                    if (this.user && this.user.token) {
                        headers['Authorization'] = 'Bearer ' + this.user.token;
                    }
                    const response = await fetch(`${API_BASE_URL}/v1/detector/analyze`, {
                        method: 'POST', headers: headers,
                        body: JSON.stringify({ language: lang, sourceCode: code })
                    });
                    
                    if (!response.ok) {
                        let errMsg = "Audit failed due to server error.";
                        if(response.status === 401) errMsg = "Unauthorized. Please login again.";
                        if(response.status === 403) errMsg = "Forbidden. Invalid token.";
                        throw new Error(errMsg);
                    }
                    data = await response.json();
                    
                    this.currentAuditData = data;
                    this.renderResults(data, code, false);
                    this.saveAuditToHistory(data, lang, code);
                } catch (err) {
                    console.error("Backend API Error:", err);
                    let userMsg = err.message;
                    if (err.name === 'TypeError' || err.message.includes('Failed to fetch')) {
                        userMsg = "Unable to connect to DevSentry backend. Please make sure the server is running.";
                    }
                    
                    document.getElementById('audit-loading').classList.add('hidden');
                    document.getElementById('audit-error').classList.remove('hidden');
                    const errTitle = document.querySelector('#audit-error h3');
                    if(errTitle) errTitle.textContent = "Analysis Failed";
                    const errDesc = document.querySelector('#audit-error p');
                    if(errDesc) errDesc.textContent = userMsg;
                } finally {
                    this.isAuditing = false;
                    if(btnRun) btnRun.disabled = false;
                    if(btnRunText) btnRunText.textContent = "Run Audit";
                }
            },
            
            """
    
    content = re.sub(pattern, new_run_audit, content)

    # Let's also fix export report to export more robustly
    export_pattern = re.compile(r'downloadCurrentReport\(\)\s*\{.*?(?=\n\s*loadHistory)', re.DOTALL)
    new_export = """downloadCurrentReport() {
                if(!this.currentAuditData) {
                    this.showAlert("Error", "No audit data to export.", "alert-triangle", "rose");
                    return;
                }
                const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.currentAuditData, null, 2));
                const node = document.createElement('a');
                node.setAttribute("href", dataStr);
                node.setAttribute("download", "DevSentry_Audit_Report.json");
                document.body.appendChild(node);
                node.click();
                document.body.removeChild(node);
            },
            """
    content = re.sub(export_pattern, new_export, content)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_run_audit()
    print("Fixed runAudit and export")
