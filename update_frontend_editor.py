import re

def update_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the layout of view-audit
    old_audit = """            <section id="view-audit" class="view-section pt-12 pb-32">
                <div class="px-8 lg:px-16 max-w-[1800px] mx-auto flex flex-col xl:flex-row gap-16">
                    <div class="xl:w-7/12 flex flex-col h-[80vh]">
                        <h2 class="text-editorial-h2 text-charcoal-600 mb-8">SHOW ME<br>YOUR CODE.</h2>
                        <div class="flex items-center justify-between mb-6">
                            <select id="language-select" class="bg-transparent border-b-2 border-charcoal-600 py-2 pr-8 text-lg font-bold text-charcoal-600 outline-none">
        <option value="java">Java</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="html">HTML</option>
        <option value="sql">SQL</option>
    </select>
                            <div class="flex gap-4">
                                <button onclick="app.clearEditor()" class="text-sm font-bold uppercase tracking-widest text-charcoal-400">Clear</button>
                                <button id="btn-run-audit" onclick="app.runAudit()" class="interactive-btn dark-ripple bg-charcoal-600 text-ivory-50 px-6 py-3 text-sm font-bold uppercase tracking-widest"><span id="btn-run-text">Run Audit</span></button>
                            </div>
                        </div>
                        <div class="flex-1 bg-ivory-50 shadow-panel p-1 relative group"><div id="editor-container" class="w-full h-full"></div></div>
                    </div>
                    <div class="xl:w-5/12 h-[80vh] flex flex-col pt-24">
                        <div id="audit-results" class="hidden h-full flex flex-col opacity-0 transition-opacity duration-700">
        <div class="flex gap-4 mb-8 border-b hairline-border pb-4" id="analysis-breakdown">
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-charcoal-400">
                <i data-lucide="check-circle" class="w-4 h-4 text-success-500" id="check-compiler"></i> Compiler
            </div>
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-charcoal-400">
                <i data-lucide="check-circle" class="w-4 h-4 text-success-500" id="check-static"></i> Static Analysis
            </div>
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-charcoal-400">
                <i data-lucide="check-circle" class="w-4 h-4 text-success-500" id="check-ai"></i> AI Engine
            </div>
        </div>
                            <div class="mb-16">
                                <p class="text-xs font-bold uppercase tracking-widest text-charcoal-400 mb-6">Score</p>
                                <span id="res-score" class="text-8xl font-black text-brand-500 tracking-tighter leading-none">0</span><span class="text-2xl font-bold text-charcoal-400">/100</span>
                                <div class="w-full h-1 bg-ivory-300 mt-8 relative"><div id="res-score-bar" class="absolute left-0 top-0 h-full bg-brand-500 transition-all duration-1000 w-0"></div></div>
                            </div>
                            <div class="mb-12">
                                <h3 class="text-2xl font-bold text-charcoal-600 mb-2" id="res-summary-title">Analysis Complete</h3>
                                <p class="text-lg text-charcoal-400" id="res-summary-text">...</p>
                            </div>
                            <div class="flex-1 overflow-y-auto pr-4 space-y-6" id="issue-list"></div>
                        </div>
                        <div id="audit-empty" class="h-full flex flex-col items-center justify-center text-center opacity-100 transition-opacity duration-500">
                            <h3 class="text-3xl font-extrabold text-charcoal-600 mb-4 tracking-tight">Awaiting Code</h3>
                        </div>
                        <div id="audit-loading" class="hidden h-full flex flex-col items-center justify-center text-center">
                            <i data-lucide="loader" class="w-12 h-12 text-brand-500 animate-spin mb-6"></i>
                            <h3 class="text-2xl font-bold text-charcoal-600 mb-2">Analyzing...</h3>
                            <p class="text-charcoal-400" id="loading-text">Inspecting code logic and security...</p>
                        </div>
                        <div id="audit-error" class="hidden h-full flex flex-col items-center justify-center text-center">
                            <i data-lucide="alert-triangle" class="w-12 h-12 text-danger-500 mb-6"></i>
                            <h3 class="text-2xl font-bold text-charcoal-600 mb-2" id="error-title">Analysis Failed</h3>
                            <p class="text-charcoal-400" id="error-desc">Unable to connect to the backend.</p>
                        </div>
                    </div>
                </div>
            </section>"""

    new_audit = """            <section id="view-audit" class="view-section pt-12 pb-32">
                <div class="px-8 lg:px-16 max-w-[1800px] mx-auto flex flex-col gap-12">
                    <!-- Top controls -->
                    <div>
                        <h2 class="text-editorial-h2 text-charcoal-600 mb-8">SHOW ME<br>YOUR CODE.</h2>
                        <div class="flex items-center justify-between mb-6">
                            <select id="language-select" class="bg-transparent border-b-2 border-charcoal-600 py-2 pr-8 text-lg font-bold text-charcoal-600 outline-none" onchange="app.changeLanguage(this.value, true)">
                                <option value="java">Java</option>
                                <option value="c">C</option>
                                <option value="cpp">C++</option>
                                <option value="python">Python</option>
                                <option value="javascript">JavaScript</option>
                                <option value="html">HTML</option>
                                <option value="sql">SQL</option>
                            </select>
                            <div class="flex gap-4">
                                <button onclick="app.clearEditor()" class="text-sm font-bold uppercase tracking-widest text-charcoal-400 hover:text-charcoal-600 transition">Clear</button>
                                <button id="btn-run-audit" onclick="app.runAudit()" class="interactive-btn dark-ripple bg-charcoal-600 text-ivory-50 px-6 py-3 text-sm font-bold uppercase tracking-widest shadow-panel hover:bg-charcoal-900 transition flex gap-2 items-center"><i data-lucide="play" class="w-4 h-4"></i><span id="btn-run-text">Run Audit</span></button>
                            </div>
                        </div>
                    </div>

                    <!-- Editor and Output Side-by-side -->
                    <div class="flex flex-col lg:flex-row gap-6 h-[60vh] min-h-[500px]">
                        <!-- Code Editor (60%) -->
                        <div class="lg:w-3/5 bg-[#F7F5F0] border hairline-border shadow-panel relative group flex flex-col">
                            <div id="editor-loading" class="hidden"></div>
                            <div id="editor-container" class="w-full flex-1"></div>
                        </div>
                        
                        <!-- Output Panel (40%) -->
                        <div class="lg:w-2/5 bg-ivory-50 border hairline-border shadow-panel p-6 flex flex-col relative">
                            <div class="flex justify-between items-center border-b hairline-border pb-4 mb-4">
                                <h3 class="text-sm font-bold uppercase tracking-widest text-charcoal-600">OUTPUT</h3>
                                <button onclick="app.copyOutputData()" class="text-xs font-bold text-charcoal-400 hover:text-brand-600 transition flex items-center gap-1">
                                    <i data-lucide="copy" class="w-4 h-4"></i> COPY
                                </button>
                            </div>
                            <div id="output-status" class="mb-4 text-xs font-bold uppercase tracking-widest text-charcoal-400">STATUS: <span class="text-charcoal-600">READY</span></div>
                            <div class="flex-1 overflow-y-auto bg-transparent p-0 m-0">
                                <pre id="output-console" class="text-sm font-mono text-charcoal-600 whitespace-pre-wrap">Awaiting execution...</pre>
                            </div>
                        </div>
                    </div>

                    <!-- Status displays for UI flow -->
                    <div id="audit-loading" class="hidden py-16 flex flex-col items-center justify-center text-center">
                        <i data-lucide="loader" class="w-12 h-12 text-brand-500 animate-spin mb-6"></i>
                        <h3 class="text-2xl font-bold text-charcoal-600 mb-2">Analyzing...</h3>
                        <p class="text-charcoal-400" id="loading-text">Inspecting code logic and security...</p>
                    </div>

                    <div id="audit-error" class="hidden py-16 flex flex-col items-center justify-center text-center">
                        <i data-lucide="alert-triangle" class="w-12 h-12 text-danger-500 mb-6"></i>
                        <h3 class="text-2xl font-bold text-charcoal-600 mb-2" id="error-title">Analysis Failed</h3>
                        <p class="text-charcoal-400" id="error-desc">Unable to connect to the backend.</p>
                        <button onclick="app.runAudit()" class="mt-6 border-b border-charcoal-600 text-charcoal-600 font-bold text-sm uppercase tracking-widest">Retry Audit</button>
                    </div>

                    <!-- Audit Results Section -->
                    <div id="audit-results" class="hidden pt-12 border-t hairline-border flex-col opacity-0 transition-opacity duration-700">
                        <h3 class="text-3xl font-extrabold text-charcoal-600 tracking-tight mb-12">AUDIT RESULTS</h3>
                        
                        <div class="flex flex-col xl:flex-row gap-12">
                            <div class="xl:w-1/3">
                                <div class="mb-12">
                                    <p class="text-xs font-bold uppercase tracking-widest text-charcoal-400 mb-6">Score</p>
                                    <span id="res-score" class="text-8xl font-black text-brand-500 tracking-tighter leading-none">0</span><span class="text-2xl font-bold text-charcoal-400">/100</span>
                                    <div class="w-full h-1 bg-ivory-300 mt-8 relative"><div id="res-score-bar" class="absolute left-0 top-0 h-full bg-brand-500 transition-all duration-1000 w-0"></div></div>
                                </div>
                                <div class="flex gap-4 mb-10 flex-col" id="analysis-breakdown">
                                    <div class="flex items-center gap-3 text-sm font-bold uppercase tracking-widest text-charcoal-400">
                                        <i data-lucide="check-circle" class="w-5 h-5 text-success-500" id="check-compiler"></i> Compiler
                                    </div>
                                    <div class="flex items-center gap-3 text-sm font-bold uppercase tracking-widest text-charcoal-400">
                                        <i data-lucide="check-circle" class="w-5 h-5 text-success-500" id="check-static"></i> Static Analysis
                                    </div>
                                    <div class="flex items-center gap-3 text-sm font-bold uppercase tracking-widest text-charcoal-400">
                                        <i data-lucide="check-circle" class="w-5 h-5 text-success-500" id="check-ai"></i> AI Engine
                                    </div>
                                </div>
                            </div>
                            
                            <div class="xl:w-2/3">
                                <div class="mb-12">
                                    <h3 class="text-2xl font-bold text-charcoal-600 mb-2" id="res-summary-title">Analysis Complete</h3>
                                    <p class="text-lg text-charcoal-400 leading-relaxed" id="res-summary-text">...</p>
                                </div>
                                <div class="space-y-6" id="issue-list"></div>
                            </div>
                        </div>
                    </div>

                </div>
            </section>"""
            
    if "SHOW ME YOUR CODE" in old_audit and old_audit in content:
        content = content.replace(old_audit, new_audit)
    
    # 2. Update JavaScript inside <script>
    
    js_editor_setup = """            setupEditor() {
                if(typeof require === 'undefined') return;
                require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' } });
                require(['vs/editor/editor.main'], () => {
                    monaco.editor.defineTheme('devsentry-theme', {
                        base: 'vs',
                        inherit: true,
                        rules: [
                            { background: 'F7F5F0' }
                        ],
                        colors: {
                            'editor.background': '#F7F5F0',
                            'editor.lineHighlightBackground': '#FDFBF7',
                            'editorLineNumber.foreground': '#8A877F',
                            'editor.selectionBackground': '#EAE3D7'
                        }
                    });
                    
                    const el = document.getElementById('editor-loading');
                    if(el) el.style.display = 'none';
                    
                    this.editor = monaco.editor.create(document.getElementById('editor-container'), {
                        value: "", language: 'java', theme: 'devsentry-theme', automaticLayout: true,
                        fontFamily: '"Fira Code", monospace', fontSize: 15, minimap: { enabled: false }, padding: { top: 24, bottom: 24 }, scrollBeyondLastLine: false,
                        renderLineHighlight: 'all', roundedSelection: true
                    });
                    
                    this.loadTemplate('java');
                });
            },"""
            
    old_editor_setup = """            setupEditor() {
                if(typeof require === 'undefined') return;
                require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' } });
                require(['vs/editor/editor.main'], () => {
                    document.getElementById('editor-loading').style.display = 'none';
                    this.editor = monaco.editor.create(document.getElementById('editor-container'), {
                        value: "", language: 'java', theme: 'vs', automaticLayout: true,
                        fontFamily: '"Fira Code", monospace', fontSize: 14, minimap: { enabled: false }, padding: { top: 16 }, scrollBeyondLastLine: false
                    });
                });
            },"""
            
    content = content.replace(old_editor_setup, js_editor_setup)
    
    js_change_lang = """            changeLanguage(val, loadTemplate = false) {
                const select = document.getElementById('language-select');
                if(select) select.value = val;
                
                let monacoLang = val;
                if(val === 'c' || val === 'cpp') monacoLang = 'cpp';
                
                if (this.editor) monaco.editor.setModelLanguage(this.editor.getModel(), monacoLang);
                if (loadTemplate) this.loadTemplate(val);
            },"""
    
    old_change_lang = """            changeLanguage(val) {
                const select = document.getElementById('language-select');
                if(select) select.value = val;
                if (this.editor) monaco.editor.setModelLanguage(this.editor.getModel(), val);
            },"""
            
    content = content.replace(old_change_lang, js_change_lang)
    
    js_load_template = """            loadTemplate(lang) {
                if (this.editor) {
                    if (lang === 'java') this.editor.setValue(`public class Main {\\n    public static void main(String[] args) {\\n        System.out.println("Hello DevSentry AI");\\n    }\\n}`);
                    else if (lang === 'cpp') this.editor.setValue(`#include <iostream>\\nusing namespace std;\\n\\nint main() {\\n    cout << "Hello DevSentry AI";\\n    return 0;\\n}`);
                    else if (lang === 'c') this.editor.setValue(`#include <stdio.h>\\n\\nint main() {\\n    printf("Hello DevSentry AI\\n");\\n    return 0;\\n}`);
                    else if (lang === 'python') this.editor.setValue(`print("Hello DevSentry AI")`);
                    else if (lang === 'javascript') this.editor.setValue(`console.log("Hello DevSentry AI");`);
                    else if (lang === 'html') this.editor.setValue(`<!DOCTYPE html>\\n<html>\\n<head>\\n<title>Test</title>\\n</head>\\n<body>\\n<h1>Hello DevSentry AI</h1>\\n</body>\\n</html>`);
                    else if (lang === 'sql') this.editor.setValue(`SELECT * FROM users;`);
                }
            },"""
            
    old_load_template = """            loadTemplate(lang) {
                this.navigate('audit');
                this.changeLanguage(lang);
                if (this.editor) {
                    if (lang === 'java') this.editor.setValue(`public class UserAuth {\\n    public boolean login(String user, String pass) {\\n        // Vulnerable to SQL Injection\\n        String query = "SELECT * FROM users WHERE uname='" + user + "' AND pword='" + pass + "'";\\n        \\n        // Resource Leak\\n        Connection conn = dataSource.getConnection();\\n        Statement stmt = conn.createStatement();\\n        ResultSet rs = stmt.executeQuery(query);\\n        \\n        return rs.next();\\n    }\\n}`);
                    else if (lang === 'cpp') this.editor.setValue(`#include <iostream>\\nusing namespace std;\\n\\nint main() {\\n    int arr[3] = {1, 2, 3};\\n    for(int i = 0; i <= 3; i++) {\\n        cout << arr[i] << endl;\\n    }\\n    return 0;\\n}`);
                    else if (lang === 'python') this.editor.setValue(`numbers = [1, 2, 3]\\nfor i in range(4):\\n    print(numbers[i])`);
                    this.showEmpty();
                }
            },"""
            
    content = content.replace(old_load_template, js_load_template)
    
    js_clear = """            clearEditor() {
                if (this.editor) this.editor.setValue("");
                document.getElementById('output-status').innerHTML = `STATUS: <span class="text-charcoal-600">READY</span>`;
                document.getElementById('output-console').textContent = "Awaiting execution...";
                
                document.getElementById('audit-results').classList.add('hidden');
                document.getElementById('audit-results').classList.remove('flex');
                document.getElementById('audit-error').classList.add('hidden');
                document.getElementById('audit-loading').classList.add('hidden');
                
                if (this.editor) this.editor.focus();
            },"""
            
    old_clear = """            clearEditor() {
                if (this.editor) this.editor.setValue("");
                this.showEmpty();
            },"""
            
    content = content.replace(old_clear, js_clear)
    
    js_copy_output = """            copyOutputData() {
                const out = document.getElementById('output-console').textContent;
                navigator.clipboard.writeText(out).then(() => {
                    this.showAlert("Copied", "Output copied to clipboard.", "copy", "emerald");
                });
            },"""
            
    if "copyOutputData" not in content:
        content = content.replace("copyCode() {", js_copy_output + "\n            copyCode() {")
        
    js_run_audit = """            async runAudit(skipNav = false) {
                if(!skipNav) this.navigate('audit');
                if(!this.editor) return;
                
                const code = this.editor.getValue().trim();
                if(!code) {
                    this.showAlert("Error", "Please enter code before running the audit.", "alert-triangle", "error");
                    this.editor.focus();
                    return;
                }
                
                if(this.isAuditing) return;
                this.isAuditing = true;
                
                const btn = document.getElementById('btn-run-audit');
                const btnText = document.getElementById('btn-run-text');
                btn.classList.add('opacity-80', 'cursor-not-allowed');
                btnText.innerText = "ANALYZING...";
                
                // Reset UI
                document.getElementById('audit-results').classList.add('hidden');
                document.getElementById('audit-results').classList.remove('flex');
                document.getElementById('audit-error').classList.add('hidden');
                document.getElementById('audit-loading').classList.remove('hidden');
                
                document.getElementById('output-status').innerHTML = `STATUS: <span class="text-brand-500 animate-pulse">ANALYZING...</span>`;
                document.getElementById('output-console').textContent = "Running code in isolated environment...";
                
                const lang = document.getElementById('language-select').value;
                
                const extMap = { 'java': 'Main.java', 'python': 'source.py', 'cpp': 'source.cpp', 'c': 'source.c', 'html': 'index.html', 'javascript': 'source.js', 'sql': 'query.sql' };
                const payload = { language: lang, sourceCode: code, fileName: extMap[lang] || 'source.txt' };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/v1/detector/analyze`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    
                    if(!response.ok) throw new Error("Backend connection failed.");
                    
                    const data = await response.json();
                    this.currentAuditData = data;
                    
                    this.renderAuditResults(data);
                    
                } catch (e) {
                    document.getElementById('audit-loading').classList.add('hidden');
                    document.getElementById('audit-error').classList.remove('hidden');
                    
                    document.getElementById('output-status').innerHTML = `STATUS: <span class="text-danger-500 font-bold">ERROR</span>`;
                    document.getElementById('output-console').textContent = "Connection to DevSentry backend failed.";
                } finally {
                    this.isAuditing = false;
                    btn.classList.remove('opacity-80', 'cursor-not-allowed');
                    btnText.innerText = "RUN AUDIT";
                    lucide.createIcons();
                }
            },"""
            
    old_run_audit = """            async runAudit(skipNav = false) {
                if(!skipNav) this.navigate('audit');
                if(this.isAuditing) return;
                
                const code = this.editor ? this.editor.getValue().trim() : "";
                if(!code) { this.showAlert("Empty", "Please provide some code to audit."); return; }
                
                this.isAuditing = true;
                const btnText = document.getElementById('btn-run-text');
                btnText.innerText = "Analyzing...";
                
                document.getElementById('audit-empty').classList.add('hidden');
                document.getElementById('audit-results').classList.add('hidden');
                document.getElementById('audit-error').classList.add('hidden');
                document.getElementById('audit-loading').classList.remove('hidden');
                
                const lang = document.getElementById('language-select').value;
                const extMap = { 'java': 'Main.java', 'python': 'source.py', 'cpp': 'source.cpp', 'c': 'source.c', 'html': 'index.html', 'javascript': 'source.js', 'sql': 'query.sql' };
                const payload = { language: lang, sourceCode: code, fileName: extMap[lang] || 'source.txt' };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/v1/detector/analyze`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    
                    if(!response.ok) throw new Error("Backend connection failed");
                    
                    const data = await response.json();
                    this.currentAuditData = data;
                    this.renderAuditResults(data);
                } catch (e) {
                    console.error(e);
                    document.getElementById('audit-loading').classList.add('hidden');
                    document.getElementById('audit-error').classList.remove('hidden');
                } finally {
                    this.isAuditing = false;
                    btnText.innerText = "Run Audit";
                }
            },"""
            
    content = content.replace(old_run_audit, js_run_audit)
    
    js_render = """            renderAuditResults(data) {
                document.getElementById('audit-loading').classList.add('hidden');
                const resultsEl = document.getElementById('audit-results');
                resultsEl.classList.remove('hidden');
                resultsEl.classList.add('flex');
                
                // Update Output Panel
                const outStatus = document.getElementById('output-status');
                const outConsole = document.getElementById('output-console');
                
                let statusColor = "text-success-500";
                let statusText = "SUCCESS";
                if(data.compileStatus !== 'PASSED' && data.compileStatus !== 'SUCCESS') {
                    statusColor = "text-danger-500";
                    statusText = "COMPILATION ERROR";
                }
                
                outStatus.innerHTML = `STATUS: <span class="${statusColor} font-bold">${statusText}</span>`;
                
                if (data.executionOutput) {
                    outConsole.textContent = data.executionOutput;
                } else {
                    outConsole.textContent = "No standard output.";
                }
                
                if (data.compileStatus === 'FAILED' && !data.executionOutput) {
                    const errIssue = data.issues.find(i => i.source === 'COMPILER');
                    if (errIssue) outConsole.textContent = `COMPILATION ERROR\\n\\n${errIssue.title}\\n${errIssue.description}\\nLine: ${errIssue.lineNumber || 'Unknown'}`;
                }
                
                // Status checks (Compiler, Static, AI)
                const cCompiler = document.getElementById('check-compiler');
                const cStatic = document.getElementById('check-static');
                const cAi = document.getElementById('check-ai');
                
                // Reset them to success
                [cCompiler, cStatic, cAi].forEach(el => {
                    el.className = "w-5 h-5 shrink-0"; 
                    el.setAttribute("data-lucide", "check-circle");
                    el.classList.add('text-success-500');
                });
                
                const hasCompileErr = data.issues.some(i => i.source === 'COMPILER' && i.severity === 'CRITICAL');
                const hasStaticErr = data.issues.some(i => i.source === 'STATIC_ANALYZER');
                const hasAiErr = data.issues.some(i => i.source === 'AI');
                
                if(hasCompileErr) { cCompiler.setAttribute("data-lucide", "alert-circle"); cCompiler.classList.replace('text-success-500', 'text-danger-500'); }
                if(hasStaticErr) { cStatic.setAttribute("data-lucide", "alert-circle"); cStatic.classList.replace('text-success-500', 'text-warning-500'); }
                if(hasAiErr) { cAi.setAttribute("data-lucide", "alert-circle"); cAi.classList.replace('text-success-500', 'text-brand-500'); }
                
                // Score animation
                setTimeout(() => {
                    document.getElementById('res-score').textContent = data.score;
                    const bar = document.getElementById('res-score-bar');
                    bar.style.width = `${data.score}%`;
                    if(data.score < 60) bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-danger-500";
                    else if(data.score < 80) bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-warning-500";
                    else bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-success-500";
                    
                    resultsEl.classList.remove('opacity-0');
                    resultsEl.classList.add('opacity-100');
                }, 100);
                
                document.getElementById('res-summary-text').innerHTML = data.summary || "Code analyzed successfully.";
                
                // Build issue list
                const list = document.getElementById('issue-list');
                list.innerHTML = "";
                
                if (!data.issues || data.issues.length === 0) {
                    list.innerHTML = `<div class="p-6 bg-ivory-100 border hairline-border text-center"><i data-lucide="check-circle" class="w-8 h-8 text-success-500 mx-auto mb-4"></i><h4 class="font-bold text-charcoal-600">No issues found</h4><p class="text-sm text-charcoal-400">Excellent code quality.</p></div>`;
                } else {
                    data.issues.forEach((issue, idx) => {
                        const badgeColor = issue.source === 'COMPILER' ? 'bg-danger-500' : (issue.source === 'STATIC_ANALYZER' ? 'bg-warning-500' : 'bg-brand-500');
                        
                        let html = `
                            <div class="bg-ivory-100 border hairline-border p-6 hover-lift relative overflow-hidden group">
                                <div class="absolute top-0 left-0 w-1 h-full ${badgeColor}"></div>
                                <div class="flex justify-between items-start mb-4">
                                    <div class="flex items-center gap-3">
                                        <span class="text-[10px] font-bold uppercase tracking-widest text-ivory-50 ${badgeColor} px-2 py-1">${issue.source}</span>
                                        <h4 class="font-bold text-charcoal-600">${issue.title}</h4>
                                    </div>
                                    ${issue.lineNumber ? `<button onclick="app.highlightLine(${issue.lineNumber})" class="text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition">Line ${issue.lineNumber}</button>` : ''}
                                </div>
                                <p class="text-charcoal-500 text-sm leading-relaxed mb-4">${issue.description}</p>
                                
                                ${issue.fixCode ? `
                                    <button onclick="app.showFixUI(${idx})" class="interactive-btn dark-ripple bg-ivory-200 text-charcoal-600 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-ivory-300 transition flex items-center gap-2 mb-4">
                                        <i data-lucide="wand-2" class="w-3 h-3"></i> Apply AI Fix
                                    </button>
                                    <div id="fix-ui-${idx}" class="hidden bg-charcoal-900 text-ivory-50 p-4 rounded-sm text-sm font-mono overflow-x-auto relative">
                                        <button onclick="app.applyFixCode('${issue.fixCode.replace(/'/g, "\\'")}', ${idx})" class="absolute top-2 right-2 text-ivory-300 hover:text-ivory-50"><i data-lucide="copy" class="w-4 h-4"></i></button>
                                        <pre>${issue.fixCode}</pre>
                                    </div>
                                ` : ''}
                            </div>
                        `;
                        list.insertAdjacentHTML('beforeend', html);
                    });
                }
                
                lucide.createIcons();
                this.saveAuditHistory(data);
                
                // Highlight first compiler error automatically
                const compErr = data.issues.find(i => i.source === 'COMPILER' && i.lineNumber);
                if (compErr) {
                    setTimeout(() => this.highlightLine(compErr.lineNumber), 200);
                }
            },"""
            
    # Remove old showEmpty/renderAuditResults since we are replacing it
    old_render = """            renderAuditResults(data) {
                document.getElementById('audit-loading').classList.add('hidden');
                const resultsEl = document.getElementById('audit-results');
                resultsEl.classList.remove('hidden');
                resultsEl.classList.add('flex');
                
                const cCompiler = document.getElementById('check-compiler');
                const cStatic = document.getElementById('check-static');
                const cAi = document.getElementById('check-ai');
                
                [cCompiler, cStatic, cAi].forEach(el => { el.className = "w-4 h-4"; el.setAttribute("data-lucide", "check-circle"); el.classList.add('text-success-500'); });
                
                const hasCompileErr = data.issues.some(i => i.source === 'COMPILER');
                const hasStaticErr = data.issues.some(i => i.source === 'STATIC_ANALYZER');
                const hasAiErr = data.issues.some(i => i.source === 'AI');
                
                if(hasCompileErr) { cCompiler.setAttribute("data-lucide", "alert-circle"); cCompiler.classList.replace('text-success-500', 'text-danger-500'); }
                if(hasStaticErr) { cStatic.setAttribute("data-lucide", "alert-circle"); cStatic.classList.replace('text-success-500', 'text-warning-500'); }
                if(hasAiErr) { cAi.setAttribute("data-lucide", "alert-circle"); cAi.classList.replace('text-success-500', 'text-brand-500'); }
                
                setTimeout(() => {
                    document.getElementById('res-score').textContent = data.score;
                    const bar = document.getElementById('res-score-bar');
                    bar.style.width = `${data.score}%`;
                    if(data.score < 60) bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-danger-500";
                    else if(data.score < 80) bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-warning-500";
                    else bar.className = "absolute left-0 top-0 h-full transition-all duration-1000 bg-success-500";
                    
                    resultsEl.classList.remove('opacity-0');
                    resultsEl.classList.add('opacity-100');
                }, 100);
                
                document.getElementById('res-summary-text').innerHTML = data.summary || "Analysis complete.";
                
                const list = document.getElementById('issue-list');
                list.innerHTML = "";
                
                if (!data.issues || data.issues.length === 0) {
                    list.innerHTML = `<div class="p-6 bg-ivory-100 border hairline-border text-center"><i data-lucide="check-circle" class="w-8 h-8 text-success-500 mx-auto mb-4"></i><h4 class="font-bold text-charcoal-600">No issues found</h4><p class="text-sm text-charcoal-400">Excellent code quality.</p></div>`;
                } else {
                    data.issues.forEach((issue, idx) => {
                        const badgeColor = issue.source === 'COMPILER' ? 'bg-danger-500' : (issue.source === 'STATIC_ANALYZER' ? 'bg-warning-500' : 'bg-brand-500');
                        let html = `
                            <div class="bg-ivory-100 border hairline-border p-6 hover-lift relative overflow-hidden group">
                                <div class="absolute top-0 left-0 w-1 h-full ${badgeColor}"></div>
                                <div class="flex justify-between items-start mb-4">
                                    <div class="flex items-center gap-3">
                                        <span class="text-[10px] font-bold uppercase tracking-widest text-ivory-50 ${badgeColor} px-2 py-1">${issue.source}</span>
                                        <h4 class="font-bold text-charcoal-600">${issue.title}</h4>
                                    </div>
                                    ${issue.lineNumber ? `<button onclick="app.highlightLine(${issue.lineNumber})" class="text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition">Line ${issue.lineNumber}</button>` : ''}
                                </div>
                                <p class="text-charcoal-500 text-sm leading-relaxed mb-4">${issue.description}</p>
                            </div>
                        `;
                        list.insertAdjacentHTML('beforeend', html);
                    });
                }
                
                lucide.createIcons();
                this.saveAuditHistory(data);
                
                const compErr = data.issues.find(i => i.source === 'COMPILER' && i.lineNumber);
                if (compErr) setTimeout(() => this.highlightLine(compErr.lineNumber), 200);
            },"""
            
    content = content.replace(old_render, js_render)
    
    js_show_empty = """            showEmpty() {
                // Remove legacy showEmpty since UI is statically displayed
            },"""
            
    old_show_empty = """            showEmpty() {
                document.getElementById('audit-empty').classList.remove('hidden');
                document.getElementById('audit-results').classList.add('hidden');
                document.getElementById('audit-results').classList.remove('flex');
                document.getElementById('audit-error').classList.add('hidden');
                document.getElementById('audit-loading').classList.add('hidden');
            },"""
            
    content = content.replace(old_show_empty, js_show_empty)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_html()
