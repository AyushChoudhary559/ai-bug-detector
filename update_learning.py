import re

def update_learning_modules():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update buttons in Learning section
    old_buttons = """<button class="text-sm font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-2">View Modules <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
                        </div>
                        <div class="bg-ivory-50 shadow-panel p-10 text-left border-t-4 border-brand-500 hover-lift">
                            <i data-lucide="code-2" class="w-10 h-10 text-brand-500 mb-6"></i>
                            <h3 class="text-xl font-bold text-charcoal-600 mb-4">Clean Code</h3>
                            <p class="text-charcoal-400 leading-relaxed mb-6">Master SOLID principles, design patterns, and maintainable architecture through AI-guided refactoring.</p>
                            <button class="text-sm font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-2">Read Guide <i data-lucide="arrow-right" class="w-4 h-4"></i></button>"""
                            
    new_buttons = """<button onclick="app.startPerformanceScan()" class="text-sm font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-2">View Modules <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
                        </div>
                        <div class="bg-ivory-50 shadow-panel p-10 text-left border-t-4 border-brand-500 hover-lift">
                            <i data-lucide="code-2" class="w-10 h-10 text-brand-500 mb-6"></i>
                            <h3 class="text-xl font-bold text-charcoal-600 mb-4">Clean Code</h3>
                            <p class="text-charcoal-400 leading-relaxed mb-6">Master SOLID principles, design patterns, and maintainable architecture through AI-guided refactoring.</p>
                            <button onclick="app.startCleanCodeScan()" class="text-sm font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-2">Read Guide <i data-lucide="arrow-right" class="w-4 h-4"></i></button>"""

    if "app.startPerformanceScan()" not in content:
        content = content.replace(old_buttons, new_buttons)

    # Update app.js
    old_security = """            startSecurityScan() {
                this.navigate('audit');
                this.loadTemplate('java');
                setTimeout(() => this.runAudit(true), 500);
            },"""
            
    new_scans = """            startSecurityScan() {
                this.navigate('audit');
                this.changeLanguage('java', false);
                if (this.editor) {
                    this.editor.setValue(`public class UserAuth {\\n    public boolean login(String user, String pass) {\\n        // Vulnerable to SQL Injection\\n        String query = "SELECT * FROM users WHERE uname='" + user + "' AND pword='" + pass + "'";\\n        \\n        // Resource Leak\\n        Connection conn = dataSource.getConnection();\\n        Statement stmt = conn.createStatement();\\n        ResultSet rs = stmt.executeQuery(query);\\n        \\n        return rs.next();\\n    }\\n}`);
                }
                setTimeout(() => this.runAudit(true), 500);
            },
            
            startPerformanceScan() {
                this.navigate('audit');
                this.changeLanguage('python', false);
                if (this.editor) {
                    this.editor.setValue(`def bad_performance(data):\\n    result = []\\n    for item in data:\\n        # O(N^2) complexity hidden in 'in' operator on a list\\n        if item not in result:\\n            result.append(item)\\n    return result`);
                }
                setTimeout(() => this.runAudit(true), 500);
            },
            
            startCleanCodeScan() {
                this.navigate('audit');
                this.changeLanguage('cpp', false);
                if (this.editor) {
                    this.editor.setValue(`#include <iostream>\\n\\n// Anti-pattern: global state, magic numbers, missing memory management\\nint MAGIC = 42;\\n\\nvoid process() {\\n    int* leak = new int[100];\\n    if (MAGIC == 42) {\\n        return; // Memory leak here!\\n    }\\n    delete[] leak;\\n}\\n\\nint main() {\\n    process();\\n    return 0;\\n}`);
                }
                setTimeout(() => this.runAudit(true), 500);
            },"""

    if "startPerformanceScan()" not in content:
        content = content.replace(old_security, new_scans)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Updated learning modules")

if __name__ == "__main__":
    update_learning_modules()
