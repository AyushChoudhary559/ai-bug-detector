import re

def update_frontend():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add all languages to dropdown
    old_select = '<select id="language-select" class="bg-transparent border-b-2 border-charcoal-600 py-2 pr-8 text-lg font-bold text-charcoal-600 outline-none"><option value="java">Java</option><option value="cpp">C++</option></select>'
    new_select = """<select id="language-select" class="bg-transparent border-b-2 border-charcoal-600 py-2 pr-8 text-lg font-bold text-charcoal-600 outline-none">
        <option value="java">Java</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="html">HTML</option>
        <option value="sql">SQL</option>
    </select>"""
    html = html.replace(old_select, new_select)

    # Add analysis breakdown UI
    old_audit_results = '<div id="audit-results" class="hidden h-full flex flex-col opacity-0 transition-opacity duration-700">'
    new_audit_results = """<div id="audit-results" class="hidden h-full flex flex-col opacity-0 transition-opacity duration-700">
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
        </div>"""
    html = html.replace(old_audit_results, new_audit_results)

    # Modify `renderResults` to update the checks based on compileStatus
    old_renderResults = """        const titleEl = document.getElementById('res-summary-title');
        if(titleEl) titleEl.textContent = score >= 80 ? "Excellent Quality" : (score >= 60 ? "Needs Improvement" : "Critical Attention Required");"""
    
    new_renderResults = """        const titleEl = document.getElementById('res-summary-title');
        if(titleEl) titleEl.textContent = score >= 80 ? "Excellent Quality" : (score >= 60 ? "Needs Improvement" : "Critical Attention Required");
        
        // Update Breakdown Checks
        const cc = document.getElementById('check-compiler');
        if (cc) {
            cc.className = res.compileStatus === 'PASSED' ? 'w-4 h-4 text-success-500' : (res.compileStatus === 'FAILED' ? 'w-4 h-4 text-danger-500' : 'w-4 h-4 text-warning-500');
            if (res.compileStatus && res.compileStatus.includes('UNAVAILABLE')) cc.className = 'w-4 h-4 text-charcoal-300';
        }
        """
    html = html.replace(old_renderResults, new_renderResults)

    # Add Source badge to issues
    # Find: <p class="text-[10px] font-bold uppercase tracking-widest text-charcoal-400">${issue.severity}</p>
    old_issue_header = '<p class="text-[10px] font-bold uppercase tracking-widest text-charcoal-400">${issue.severity}</p>'
    new_issue_header = '<p class="text-[10px] font-bold uppercase tracking-widest text-charcoal-400 flex items-center gap-2"><span class="bg-charcoal-200 px-1 py-0.5 rounded">${issue.source || \'AI\'}</span> ${issue.severity}</p>'
    html = html.replace(old_issue_header, new_issue_header)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated Frontend")

if __name__ == "__main__":
    update_frontend()
