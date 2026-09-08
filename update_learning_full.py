import re

def update_learning_full():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace view-learning
    old_learning_start = '<section id="view-learning" class="view-section pt-20 pb-32">'
    old_learning_end = '</section>\n\n            <section id="view-history"'
    
    # We need to find the exact block using regex
    match = re.search(r'(<section id="view-learning".*?</section>)\s*<section id="view-history"', content, re.DOTALL)
    if not match:
        print("Could not find view-learning section")
        return
        
    old_view_learning = match.group(1)

    new_view_learning = """<section id="view-learning" class="view-section pt-20 pb-32">
                <div class="px-8 lg:px-16 max-w-[1800px] mx-auto">
                    <!-- LEARNING DASHBOARD -->
                    <div id="learning-dashboard" class="transition-opacity duration-500 opacity-100">
                        <div class="flex flex-col lg:flex-row justify-between items-end mb-12 gap-8">
                            <div>
                                <h2 class="text-editorial-h2 text-charcoal-600 mb-4">EVERY BUG IS<br>A LESSON.</h2>
                                <p class="text-2xl font-medium text-charcoal-400 max-w-2xl leading-relaxed">We automatically compile your most frequent mistakes to help you master clean, secure coding.</p>
                            </div>
                            
                            <!-- Progress Overview -->
                            <div class="bg-ivory-50 shadow-panel p-6 lg:w-96 border border-ivory-300">
                                <h4 class="text-xs font-bold uppercase tracking-widest text-charcoal-400 mb-4 flex items-center justify-between">Learning Progress <span class="text-brand-500" id="progress-overall">0%</span></h4>
                                
                                <div class="space-y-4">
                                    <div>
                                        <div class="flex justify-between text-xs font-bold text-charcoal-600 mb-1"><span>Security</span> <span id="progress-security-text">0%</span></div>
                                        <div class="w-full h-1 bg-ivory-300"><div id="progress-security-bar" class="h-full bg-danger-500 w-0 transition-all duration-1000"></div></div>
                                    </div>
                                    <div>
                                        <div class="flex justify-between text-xs font-bold text-charcoal-600 mb-1"><span>Performance</span> <span id="progress-performance-text">0%</span></div>
                                        <div class="w-full h-1 bg-ivory-300"><div id="progress-performance-bar" class="h-full bg-warning-500 w-0 transition-all duration-1000"></div></div>
                                    </div>
                                    <div>
                                        <div class="flex justify-between text-xs font-bold text-charcoal-600 mb-1"><span>Clean Code</span> <span id="progress-clean-text">0%</span></div>
                                        <div class="w-full h-1 bg-ivory-300"><div id="progress-clean-bar" class="h-full bg-brand-500 w-0 transition-all duration-1000"></div></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <div onclick="app.openLearningCategory('security')" class="cursor-pointer bg-ivory-50 shadow-panel p-10 text-left border-t-4 border-danger-500 hover-lift group">
                                <i data-lucide="shield-alert" class="w-10 h-10 text-danger-500 mb-6 group-hover:scale-110 transition-transform"></i>
                                <h3 class="text-xl font-bold text-charcoal-600 mb-4">Security First</h3>
                                <p class="text-charcoal-400 leading-relaxed mb-6">Master SQL Injection, XSS, input validation, and secure authentication flows.</p>
                                <button class="text-sm font-bold uppercase tracking-widest text-danger-500 group-hover:text-danger-600 transition flex items-center gap-2">Practice Security <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
                            </div>
                            <div onclick="app.openLearningCategory('performance')" class="cursor-pointer bg-ivory-50 shadow-panel p-10 text-left border-t-4 border-warning-500 hover-lift group">
                                <i data-lucide="zap" class="w-10 h-10 text-warning-500 mb-6 group-hover:scale-110 transition-transform"></i>
                                <h3 class="text-xl font-bold text-charcoal-600 mb-4">Performance</h3>
                                <p class="text-charcoal-400 leading-relaxed mb-6">Understand Time & Space Complexity (O(n)), DB queries, and memory optimization.</p>
                                <button class="text-sm font-bold uppercase tracking-widest text-warning-500 group-hover:text-warning-600 transition flex items-center gap-2">View Modules <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
                            </div>
                            <div onclick="app.openLearningCategory('clean_code')" class="cursor-pointer bg-ivory-50 shadow-panel p-10 text-left border-t-4 border-brand-500 hover-lift group">
                                <i data-lucide="code-2" class="w-10 h-10 text-brand-500 mb-6 group-hover:scale-110 transition-transform"></i>
                                <h3 class="text-xl font-bold text-charcoal-600 mb-4">Clean Code</h3>
                                <p class="text-charcoal-400 leading-relaxed mb-6">Master SOLID principles, DRY, naming conventions, and maintainable architecture.</p>
                                <button class="text-sm font-bold uppercase tracking-widest text-brand-500 group-hover:text-brand-600 transition flex items-center gap-2">Read Guide <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
                            </div>
                        </div>
                    </div>

                    <!-- ACTIVE MODULE VIEW -->
                    <div id="learning-module-view" class="hidden flex-col gap-12 transition-opacity duration-500 opacity-0">
                        <button onclick="app.closeLearningCategory()" class="text-xs font-bold uppercase tracking-widest text-charcoal-400 hover:text-charcoal-600 transition flex items-center gap-2 self-start"><i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Modules</button>
                        
                        <div class="flex items-center gap-4 border-b hairline-border pb-6">
                            <i id="lm-icon" data-lucide="shield-alert" class="w-12 h-12 text-brand-500"></i>
                            <h2 id="lm-title" class="text-4xl font-extrabold text-charcoal-600 tracking-tight">Security Practice</h2>
                        </div>
                        
                        <div class="flex flex-col lg:flex-row gap-12 items-start">
                            <!-- Module List (Sidebar) -->
                            <div class="lg:w-1/4 w-full flex flex-col space-y-2" id="lm-sidebar">
                                <!-- Modules dynamically injected here -->
                            </div>
                            
                            <!-- Active Content -->
                            <div class="lg:w-3/4 w-full bg-ivory-50 shadow-panel p-8 lg:p-12 border border-ivory-300">
                                <div id="lm-content">
                                    <h3 id="lmc-title" class="text-2xl font-bold text-charcoal-600 mb-4">Module Title</h3>
                                    <p id="lmc-explanation" class="text-lg text-charcoal-500 leading-relaxed mb-8">Explanation goes here...</p>
                                    
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                                        <div>
                                            <h4 class="text-xs font-bold uppercase tracking-widest text-danger-500 mb-2 flex items-center gap-2"><i data-lucide="x-circle" class="w-4 h-4"></i> Vulnerable/Bad</h4>
                                            <div class="bg-charcoal-900 text-danger-300 p-4 rounded-sm font-mono text-sm shadow-inner overflow-x-auto whitespace-pre"><code id="lmc-bad">bad code</code></div>
                                            <p id="lmc-whybad" class="text-sm text-danger-600 mt-2 p-3 bg-danger-50 rounded-sm"></p>
                                        </div>
                                        <div>
                                            <h4 class="text-xs font-bold uppercase tracking-widest text-success-500 mb-2 flex items-center gap-2"><i data-lucide="check-circle" class="w-4 h-4"></i> Secure/Optimized</h4>
                                            <div class="bg-charcoal-900 text-success-300 p-4 rounded-sm font-mono text-sm shadow-inner overflow-x-auto whitespace-pre"><code id="lmc-good">good code</code></div>
                                        </div>
                                    </div>
                                    
                                    <!-- Quiz Section -->
                                    <div class="border-t hairline-border pt-12 mt-8">
                                        <h4 class="text-sm font-bold uppercase tracking-widest text-charcoal-500 mb-6 flex items-center gap-2"><i data-lucide="help-circle" class="w-5 h-5"></i> Practice Question</h4>
                                        <p id="lmc-question" class="text-xl font-medium text-charcoal-600 mb-8 whitespace-pre-wrap">Question?</p>
                                        
                                        <div id="lmc-options" class="flex flex-col gap-3 mb-8">
                                            <!-- Options injected here -->
                                        </div>
                                        
                                        <div id="lmc-feedback" class="hidden p-6 rounded-sm mb-8 text-lg font-medium"></div>
                                        
                                        <button id="btn-next-module" onclick="app.nextLearningModule()" class="hidden interactive-btn bg-brand-500 text-ivory-50 px-8 py-3 text-sm font-bold uppercase tracking-widest hover:bg-brand-600 transition shadow-panel">Next Module <i data-lucide="arrow-right" class="w-4 h-4 inline ml-2"></i></button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>"""
            
    content = content.replace(old_view_learning, new_view_learning)

    # 2. Add Learning Data and logic to app.js
    # We'll insert it right after: `data() { return { ... } }` or just inject learning methods
    learning_data_js = """
    learningData: {
        security: {
            title: "Security Practice",
            icon: "shield-alert",
            colorClass: "text-danger-500",
            modules: [
                {
                    id: "sqli",
                    title: "SQL Injection",
                    explanation: "SQL Injection occurs when user input is insecurely embedded directly into a database query. Attackers can manipulate the input to bypass authentication, delete tables, or extract sensitive data.",
                    badCode: "String query = \\"SELECT * FROM users WHERE name='\\" + userInput + \\"';\\";\\nStatement stmt = conn.createStatement();\\nstmt.execute(query);",
                    whyBad: "If userInput is `admin' OR '1'='1`, the query becomes completely open and returns all users.",
                    goodCode: "String query = \\"SELECT * FROM users WHERE name=?\\";\\nPreparedStatement stmt = conn.prepareStatement(query);\\nstmt.setString(1, userInput);\\nstmt.execute();",
                    question: "Which vulnerability exists in this query construction?\\n\\nString q = \\"UPDATE products SET price=\\" + newPrice + \\" WHERE id=\\" + pId;",
                    options: ["Cross-Site Scripting", "SQL Injection", "Memory Leak", "Buffer Overflow"],
                    correctIndex: 1,
                    explanationCorrect: "Correct! Concatenating strings directly into a SQL command leaves the application vulnerable to SQL Injection. Always use Parameterized Queries."
                },
                {
                    id: "xss",
                    title: "Cross-Site Scripting (XSS)",
                    explanation: "XSS occurs when an application includes untrusted data in a web page without proper validation or escaping, allowing attackers to execute malicious scripts in victims' browsers.",
                    badCode: "<div>\\n  <h1>Welcome User</h1>\\n  <p>Status: <%= request.getParameter(\\"status\\") %></p>\\n</div>",
                    whyBad: "If status is `<script>alert(document.cookie)</script>`, the browser will execute it.",
                    goodCode: "<div>\\n  <h1>Welcome User</h1>\\n  <!-- Using standard encoding library -->\\n  <p>Status: <%= Encode.forHtml(request.getParameter(\\"status\\")) %></p>\\n</div>",
                    question: "What is the primary defense against Cross-Site Scripting (XSS)?",
                    options: ["Encrypting the database", "Context-aware Output Encoding", "Parameterized Queries", "Using HTTPS"],
                    correctIndex: 1,
                    explanationCorrect: "Correct! Context-aware output encoding ensures that the browser interprets the input as data, not as executable script."
                }
            ]
        },
        performance: {
            title: "Performance Optimization",
            icon: "zap",
            colorClass: "text-warning-500",
            modules: [
                {
                    id: "time-complexity",
                    title: "Time Complexity & Big O",
                    explanation: "Time complexity describes how the runtime of an algorithm scales as the input size grows. O(n) means linear time, O(n²) means quadratic time.",
                    badCode: "public List<Integer> findDuplicates(List<Integer> list) {\\n    List<Integer> dups = new ArrayList<>();\\n    for(int i=0; i<list.size(); i++) {\\n        for(int j=i+1; j<list.size(); j++) {\\n            if(list.get(i).equals(list.get(j))) {\\n                dups.add(list.get(i));\\n            }\\n        }\\n    }\\n    return dups;\\n}",
                    whyBad: "This O(n²) approach will freeze your application if the list has 100,000 items (10 billion iterations!).",
                    goodCode: "public Set<Integer> findDuplicates(List<Integer> list) {\\n    Set<Integer> seen = new HashSet<>();\\n    Set<Integer> dups = new HashSet<>();\\n    for(Integer item : list) {\\n        if(!seen.add(item)) dups.add(item);\\n    }\\n    return dups;\\n}",
                    question: "What is the time complexity of looking up a value in a standard Hash Map (HashSet/HashMap)?",
                    options: ["O(n²)", "O(n)", "O(log n)", "O(1)"],
                    correctIndex: 3,
                    explanationCorrect: "Correct! Hash Maps provide constant O(1) time complexity for lookups on average, making them vastly superior to searching through lists O(n)."
                }
            ]
        },
        clean_code: {
            title: "Clean Code & SOLID",
            icon: "code-2",
            colorClass: "text-brand-500",
            modules: [
                {
                    id: "dry",
                    title: "DRY Principle",
                    explanation: "DRY stands for 'Don't Repeat Yourself'. Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.",
                    badCode: "public void processOrder() {\\n    log.info(\\"Starting...\\");\\n    // 50 lines of complex DB logic\\n}\\n\\npublic void cancelOrder() {\\n    log.info(\\"Starting...\\");\\n    // The exact same 50 lines of complex DB logic\\n}",
                    whyBad: "If a bug is found in the DB logic, you have to fix it in multiple places. You will inevitably forget one.",
                    goodCode: "public void processOrder() {\\n    executeDbLogic();\\n}\\n\\npublic void cancelOrder() {\\n    executeDbLogic();\\n}\\n\\nprivate void executeDbLogic() {\\n    log.info(\\"Starting...\\");\\n    // 50 lines of complex DB logic\\n}",
                    question: "Which of the following is NOT a benefit of the DRY principle?",
                    options: ["Easier maintenance", "Reduced codebase size", "Faster application execution time", "Fewer bugs during refactoring"],
                    correctIndex: 2,
                    explanationCorrect: "Correct! DRY does not inherently make code execute faster (in fact, function calls add microscopic overhead), but it vastly improves maintainability and reduces bugs."
                }
            ]
        }
    },
    learningProgress: {
        security: [],
        performance: [],
        clean_code: []
    },
    currentCategory: null,
    currentModuleIndex: 0,"""

    # Find where app object starts and inject learningData properties
    app_start = "const app = {"
    app_new = app_start + "\n" + learning_data_js
    content = content.replace(app_start, app_new)

    # Now add the methods inside app.
    methods_code = """
            loadLearningProgress() {
                const prog = localStorage.getItem('devsentry_learning_progress');
                if (prog) {
                    try {
                        this.learningProgress = JSON.parse(prog);
                    } catch(e) {}
                }
                this.updateLearningDashboard();
            },
            
            saveLearningProgress() {
                localStorage.setItem('devsentry_learning_progress', JSON.stringify(this.learningProgress));
                this.updateLearningDashboard();
            },
            
            updateLearningDashboard() {
                const calcProg = (cat) => {
                    const total = this.learningData[cat].modules.length;
                    if (total === 0) return 0;
                    const comp = this.learningProgress[cat] ? this.learningProgress[cat].length : 0;
                    return Math.round((comp / total) * 100);
                };
                
                const sec = calcProg('security');
                const perf = calcProg('performance');
                const clean = calcProg('clean_code');
                const overall = Math.round((sec + perf + clean) / 3);
                
                const el = (id, w) => { const node = document.getElementById(id); if(node) node.style.width = w + '%'; };
                const text = (id, t) => { const node = document.getElementById(id); if(node) node.innerText = t + '%'; };
                
                el('progress-security-bar', sec); text('progress-security-text', sec);
                el('progress-performance-bar', perf); text('progress-performance-text', perf);
                el('progress-clean-bar', clean); text('progress-clean-text', clean);
                text('progress-overall', overall);
            },
            
            openLearningCategory(categoryId, targetModuleId = null) {
                const cat = this.learningData[categoryId];
                if (!cat) return;
                
                this.currentCategory = categoryId;
                
                let startIdx = 0;
                if (targetModuleId) {
                    const idx = cat.modules.findIndex(m => m.id === targetModuleId);
                    if (idx !== -1) startIdx = idx;
                }
                this.currentModuleIndex = startIdx;
                
                document.getElementById('learning-dashboard').classList.add('hidden');
                document.getElementById('learning-dashboard').classList.remove('opacity-100');
                
                const view = document.getElementById('learning-module-view');
                view.classList.remove('hidden');
                setTimeout(() => view.classList.add('opacity-100'), 50);
                
                document.getElementById('lm-title').innerText = cat.title;
                const icon = document.getElementById('lm-icon');
                icon.setAttribute('data-lucide', cat.icon);
                icon.className = `w-12 h-12 ${cat.colorClass}`;
                if(window.lucide) window.lucide.createIcons();
                
                this.renderLearningSidebar();
                this.loadLearningModule(this.currentModuleIndex);
            },
            
            closeLearningCategory() {
                this.currentCategory = null;
                
                const view = document.getElementById('learning-module-view');
                view.classList.remove('opacity-100');
                setTimeout(() => {
                    view.classList.add('hidden');
                    const dash = document.getElementById('learning-dashboard');
                    dash.classList.remove('hidden');
                    setTimeout(() => dash.classList.add('opacity-100'), 50);
                }, 300);
                this.updateLearningDashboard();
            },
            
            renderLearningSidebar() {
                const catId = this.currentCategory;
                const modules = this.learningData[catId].modules;
                const completed = this.learningProgress[catId] || [];
                
                let html = '';
                modules.forEach((mod, idx) => {
                    const isCompleted = completed.includes(mod.id);
                    const isActive = idx === this.currentModuleIndex;
                    
                    let cls = "p-4 rounded-sm flex items-center justify-between cursor-pointer transition text-left ";
                    if (isActive) cls += "bg-brand-500 text-ivory-50 font-bold shadow-panel";
                    else cls += "bg-transparent text-charcoal-500 hover:bg-ivory-100 hover:text-charcoal-600 font-medium";
                    
                    html += `<button onclick="app.loadLearningModule(${idx})" class="${cls}">
                        <span>${idx+1}. ${mod.title}</span>
                        ${isCompleted ? '<i data-lucide="check-circle" class="w-4 h-4 ' + (isActive ? 'text-ivory-50' : 'text-success-500') + '"></i>' : ''}
                    </button>`;
                });
                document.getElementById('lm-sidebar').innerHTML = html;
                if(window.lucide) window.lucide.createIcons();
            },
            
            loadLearningModule(index) {
                this.currentModuleIndex = index;
                this.renderLearningSidebar();
                
                const mod = this.learningData[this.currentCategory].modules[index];
                
                document.getElementById('lmc-title').innerText = mod.title;
                document.getElementById('lmc-explanation').innerText = mod.explanation;
                document.getElementById('lmc-bad').innerText = mod.badCode;
                document.getElementById('lmc-whybad').innerText = mod.whyBad;
                document.getElementById('lmc-good').innerText = mod.goodCode;
                document.getElementById('lmc-question').innerText = mod.question;
                
                let optHtml = '';
                mod.options.forEach((opt, idx) => {
                    optHtml += `<button onclick="app.submitQuizAnswer(${idx})" id="quiz-opt-${idx}" class="p-4 rounded-sm border border-charcoal-200 text-left font-medium text-charcoal-600 hover:border-brand-500 hover:bg-brand-50 transition w-full shadow-sm">${String.fromCharCode(65+idx)}. ${opt}</button>`;
                });
                document.getElementById('lmc-options').innerHTML = optHtml;
                
                const fb = document.getElementById('lmc-feedback');
                fb.classList.add('hidden');
                fb.className = "hidden p-6 rounded-sm mb-8 text-lg font-medium"; // reset
                
                document.getElementById('btn-next-module').classList.add('hidden');
            },
            
            submitQuizAnswer(selectedIndex) {
                const mod = this.learningData[this.currentCategory].modules[this.currentModuleIndex];
                const fb = document.getElementById('lmc-feedback');
                fb.classList.remove('hidden');
                
                // Disable all buttons
                mod.options.forEach((_, idx) => {
                    const btn = document.getElementById(`quiz-opt-${idx}`);
                    btn.disabled = true;
                    btn.classList.remove('hover:border-brand-500', 'hover:bg-brand-50');
                    if (idx === mod.correctIndex) {
                        btn.classList.add('border-success-500', 'bg-success-50', 'text-success-700');
                    } else if (idx === selectedIndex) {
                        btn.classList.add('border-danger-500', 'bg-danger-50', 'text-danger-700');
                    }
                });
                
                if (selectedIndex === mod.correctIndex) {
                    fb.innerHTML = `<div class="flex items-start gap-3"><i data-lucide="check-circle" class="w-6 h-6 shrink-0 mt-0.5"></i> <div>${mod.explanationCorrect}</div></div>`;
                    fb.classList.add('bg-success-500', 'text-ivory-50');
                    
                    // Mark completed
                    if (!this.learningProgress[this.currentCategory]) this.learningProgress[this.currentCategory] = [];
                    if (!this.learningProgress[this.currentCategory].includes(mod.id)) {
                        this.learningProgress[this.currentCategory].push(mod.id);
                        this.saveLearningProgress();
                    }
                    
                    // Show next button
                    if (this.currentModuleIndex < this.learningData[this.currentCategory].modules.length - 1) {
                        document.getElementById('btn-next-module').classList.remove('hidden');
                    } else {
                        document.getElementById('btn-next-module').classList.remove('hidden');
                        document.getElementById('btn-next-module').innerHTML = 'Back to Modules <i data-lucide="check" class="w-4 h-4 inline ml-2"></i>';
                        document.getElementById('btn-next-module').onclick = () => this.closeLearningCategory();
                    }
                    if(window.lucide) window.lucide.createIcons();
                } else {
                    fb.innerHTML = `<div class="flex items-center gap-3"><i data-lucide="x-circle" class="w-6 h-6 shrink-0"></i> Incorrect. Try reviewing the explanation above.</div>`;
                    fb.classList.add('bg-danger-500', 'text-ivory-50');
                    
                    // Re-enable for retry after 2s
                    setTimeout(() => {
                        fb.classList.add('hidden');
                        fb.classList.remove('bg-danger-500', 'text-ivory-50');
                        mod.options.forEach((_, idx) => {
                            const btn = document.getElementById(`quiz-opt-${idx}`);
                            btn.disabled = false;
                            btn.className = `p-4 rounded-sm border border-charcoal-200 text-left font-medium text-charcoal-600 hover:border-brand-500 hover:bg-brand-50 transition w-full shadow-sm`;
                        });
                    }, 2500);
                }
            },
            
            nextLearningModule() {
                if (this.currentModuleIndex < this.learningData[this.currentCategory].modules.length - 1) {
                    this.loadLearningModule(this.currentModuleIndex + 1);
                }
            },
            
            jumpToLearning(category, moduleId) {
                this.navigate('learning');
                setTimeout(() => {
                    this.openLearningCategory(category, moduleId);
                }, 100);
            },"""
    
    # Inject methods inside init or before it
    # We will look for `init() {` and place methods before it
    init_match = "init() {"
    content = content.replace(init_match, methods_code + "\n\n            " + init_match)

    # Make init call loadLearningProgress
    init_inside = """this.setupTabs();
                    this.setupEditor();
                    this.loadAuth();
                    this.loadHistory();"""
    init_inside_new = init_inside + "\n                    this.loadLearningProgress();"
    content = content.replace(init_inside, init_inside_new)

    # Finally, link from Code Audit to Learning!
    # In renderAuditResults, where issues are rendered:
    old_issue_render = """html += `<div class="bg-ivory-50 border border-ivory-300 shadow-sm p-5 rounded-sm">
                        <div class="flex items-start gap-4 mb-3">
                            <i data-lucide="${icon}" class="w-5 h-5 ${color} shrink-0 mt-0.5"></i>
                            <div>
                                <h4 class="text-charcoal-600 font-bold text-lg">${iss.title}</h4>
                                <p class="text-sm text-charcoal-400 font-mono mt-1">${iss.source} - Line ${iss.lineNumber || 'Unknown'}</p>
                            </div>
                        </div>
                        <p class="text-charcoal-500 leading-relaxed">${iss.description}</p>`"""
                        
    new_issue_render = """
                    let learnBtn = '';
                    let lowerTitle = iss.title.toLowerCase();
                    let lowerDesc = iss.description ? iss.description.toLowerCase() : '';
                    if (lowerTitle.includes('sql') || lowerDesc.includes('sql')) {
                        learnBtn = `<button onclick="app.jumpToLearning('security', 'sqli')" class="mt-4 text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-1">Learn about this issue <i data-lucide="arrow-right" class="w-3 h-3"></i></button>`;
                    } else if (lowerTitle.includes('xss') || lowerTitle.includes('cross-site') || lowerDesc.includes('cross-site')) {
                        learnBtn = `<button onclick="app.jumpToLearning('security', 'xss')" class="mt-4 text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-1">Learn about this issue <i data-lucide="arrow-right" class="w-3 h-3"></i></button>`;
                    } else if (lowerTitle.includes('complexity') || lowerDesc.includes('complexity') || lowerTitle.includes('loop')) {
                        learnBtn = `<button onclick="app.jumpToLearning('performance', 'time-complexity')" class="mt-4 text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-1">Learn about complexity <i data-lucide="arrow-right" class="w-3 h-3"></i></button>`;
                    } else if (lowerTitle.includes('duplicate') || lowerTitle.includes('solid')) {
                        learnBtn = `<button onclick="app.jumpToLearning('clean_code', 'dry')" class="mt-4 text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-1">Learn clean code <i data-lucide="arrow-right" class="w-3 h-3"></i></button>`;
                    } else {
                        learnBtn = `<button onclick="app.jumpToLearning('clean_code', 'dry')" class="mt-4 text-xs font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition flex items-center gap-1">Learn clean code <i data-lucide="arrow-right" class="w-3 h-3"></i></button>`;
                    }

                    html += `<div class="bg-ivory-50 border border-ivory-300 shadow-sm p-5 rounded-sm">
                        <div class="flex items-start gap-4 mb-3">
                            <i data-lucide="${icon}" class="w-5 h-5 ${color} shrink-0 mt-0.5"></i>
                            <div>
                                <h4 class="text-charcoal-600 font-bold text-lg">${iss.title}</h4>
                                <p class="text-sm text-charcoal-400 font-mono mt-1">${iss.source} - Line ${iss.lineNumber || 'Unknown'}</p>
                            </div>
                        </div>
                        <p class="text-charcoal-500 leading-relaxed">${iss.description}</p>
                        ${learnBtn}`"""
                        
    content = content.replace(old_issue_render, new_issue_render)

    # Fix existing performance scan overrides. I replaced them in update_learning, but since view-learning was completely swapped, I don't need to remove old ones. I just overwrote view-learning entirely.
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Full Learning system integrated")

if __name__ == "__main__":
    update_learning_full()
