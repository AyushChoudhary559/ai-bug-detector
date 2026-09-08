import re

def fix_issue_render():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to add the "Learn about this issue" button to the issue render inside renderIssueList.
    
    old_issue_btn = """                        ${issue.lineNumber ? `
                        <div class="pt-2">
                            <button onclick="app.highlightLine(${issue.lineNumber})" class="interactive-btn dark-ripple bg-charcoal-600 text-ivory-50 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-charcoal-900 transition flex items-center gap-2">
                                <i data-lucide="target" class="w-3 h-3"></i> Show Line ${issue.lineNumber}
                            </button>
                        </div>` : ''}
                    </div>"""
                    
    new_issue_btn = """                        <div class="pt-4 flex gap-4">
                            ${issue.lineNumber ? `
                            <button onclick="app.highlightLine(${issue.lineNumber})" class="interactive-btn dark-ripple bg-charcoal-600 text-ivory-50 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-charcoal-900 transition flex items-center gap-2">
                                <i data-lucide="target" class="w-3 h-3"></i> Show Line ${issue.lineNumber}
                            </button>` : ''}
                            
                            ${(() => {
                                let t = (issue.title || '').toLowerCase();
                                let d = (issue.description || '').toLowerCase();
                                let it = (issue.issueType || '').toLowerCase();
                                
                                if (t.includes('sql') || d.includes('sql')) {
                                    return `<button onclick="app.jumpToLearning('security', 'sqli')" class="border border-brand-500 text-brand-500 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-brand-50 transition flex items-center gap-2"><i data-lucide="book-open" class="w-3 h-3"></i> Learn about this issue <i data-lucide="arrow-right" class="w-3 h-3 ml-auto"></i></button>`;
                                } else if (t.includes('xss') || t.includes('cross-site') || d.includes('cross-site')) {
                                    return `<button onclick="app.jumpToLearning('security', 'xss')" class="border border-brand-500 text-brand-500 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-brand-50 transition flex items-center gap-2"><i data-lucide="book-open" class="w-3 h-3"></i> Learn about this issue <i data-lucide="arrow-right" class="w-3 h-3 ml-auto"></i></button>`;
                                } else if (it === 'performance' || t.includes('complexity') || d.includes('complexity') || t.includes('loop')) {
                                    return `<button onclick="app.jumpToLearning('performance', 'time-complexity')" class="border border-brand-500 text-brand-500 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-brand-50 transition flex items-center gap-2"><i data-lucide="book-open" class="w-3 h-3"></i> Learn about complexity <i data-lucide="arrow-right" class="w-3 h-3 ml-auto"></i></button>`;
                                } else {
                                    return `<button onclick="app.jumpToLearning('clean_code', 'dry')" class="border border-brand-500 text-brand-500 px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-brand-50 transition flex items-center gap-2"><i data-lucide="book-open" class="w-3 h-3"></i> Learn clean code <i data-lucide="arrow-right" class="w-3 h-3 ml-auto"></i></button>`;
                                }
                            })()}
                        </div>
                    </div>"""
                    
    content = content.replace(old_issue_btn, new_issue_btn)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Learning buttons linked to issues")

if __name__ == "__main__":
    fix_issue_render()
