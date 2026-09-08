import re

def fix_layout():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add xl:items-start to parent flex row
    parent_old = '<div class="px-8 lg:px-16 max-w-[1800px] mx-auto flex flex-col xl:flex-row gap-16">'
    parent_new = '<div class="px-8 lg:px-16 max-w-[1800px] mx-auto flex flex-col xl:flex-row xl:items-start gap-16">'
    content = content.replace(parent_old, parent_new)

    # 2. Make editor sticky so it stays visible while scrolling long results
    editor_old = '<div class="xl:w-7/12 flex flex-col h-[80vh]">'
    editor_new = '<div class="xl:w-7/12 flex flex-col h-[80vh] xl:sticky xl:top-24">'
    content = content.replace(editor_old, editor_new)

    # 3. Remove fixed height from right column
    right_old = '<div class="xl:w-5/12 h-[80vh] flex flex-col pt-24">'
    right_new = '<div class="xl:w-5/12 flex flex-col pt-24 pb-24">'
    content = content.replace(right_old, right_new)

    # 4. Remove h-full from audit-results
    results_old = '<div id="audit-results" class="hidden h-full flex flex-col opacity-0 transition-opacity duration-700">'
    results_new = '<div id="audit-results" class="hidden flex flex-col opacity-0 transition-opacity duration-700">'
    content = content.replace(results_old, results_new)

    # 5. Remove overflow-y-auto from issue-list
    list_old = '<div class="flex-1 overflow-y-auto pr-4 space-y-6" id="issue-list"></div>'
    list_new = '<div class="space-y-6" id="issue-list"></div>'
    content = content.replace(list_old, list_new)
    
    # Also fix empty state
    empty_old = '<div id="audit-empty" class="h-full flex flex-col items-center justify-center text-center opacity-100 transition-opacity duration-500">'
    empty_new = '<div id="audit-empty" class="h-64 flex flex-col items-center justify-center text-center opacity-100 transition-opacity duration-500">'
    content = content.replace(empty_old, empty_new)
    
    loading_old = '<div id="audit-loading" class="hidden h-full flex flex-col items-center justify-center text-center">'
    loading_new = '<div id="audit-loading" class="hidden h-64 flex flex-col items-center justify-center text-center">'
    content = content.replace(loading_old, loading_new)
    
    error_old = '<div id="audit-error" class="hidden h-full flex flex-col items-center justify-center text-center">'
    error_new = '<div id="audit-error" class="hidden h-64 flex flex-col items-center justify-center text-center">'
    content = content.replace(error_old, error_new)

    # Now let's fix the Complexity section generation in JS to be exactly what the user wants.
    complexity_old = """        if (res.complexity) {
            container.innerHTML += `
                <div class="bg-ivory-50 shadow-panel hover-lift border-l-4 border-brand-500 p-6 mt-6 animate-fade-up">
                    <h4 class="text-lg font-bold text-charcoal-600 mb-4 flex items-center gap-2"><i data-lucide="cpu" class="w-5 h-5 text-brand-500"></i> Complexity Analysis</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-ivory-200 p-4 rounded-sm">
                            <p class="text-xs font-bold uppercase tracking-widest text-charcoal-400 mb-1">Time Complexity</p>
                            <p class="text-xl font-black text-brand-500 mb-2">${res.complexity.timeComplexity || res.complexity.time || 'O(1)'}</p>
                            <p class="text-sm text-charcoal-500">${res.complexity.timeExplanation || ''}</p>
                        </div>
                        <div class="bg-ivory-200 p-4 rounded-sm">
                            <p class="text-xs font-bold uppercase tracking-widest text-charcoal-400 mb-1">Space Complexity</p>
                            <p class="text-xl font-black text-brand-500 mb-2">${res.complexity.spaceComplexity || res.complexity.space || 'O(1)'}</p>
                            <p class="text-sm text-charcoal-500">${res.complexity.spaceExplanation || ''}</p>
                        </div>
                    </div>
                </div>
            `;
        }"""
        
    complexity_new = """        if (res.complexity) {
            container.innerHTML += `
                <div class="bg-ivory-50 shadow-panel p-8 mt-12 animate-fade-up">
                    <h4 class="text-xl font-bold text-charcoal-600 mb-2 flex items-center gap-3 uppercase tracking-widest">
                        <i data-lucide="cpu" class="w-6 h-6 text-brand-500"></i> Complexity Analysis
                    </h4>
                    <p class="text-charcoal-400 mb-8 text-lg">Understand the performance characteristics of your code.</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-ivory-100 border border-ivory-300 p-6 rounded-sm flex flex-col">
                            <p class="text-sm font-bold uppercase tracking-widest text-charcoal-500 mb-4">Time Complexity</p>
                            <p class="text-3xl font-black text-brand-500 mb-2 font-mono">${res.complexity.timeComplexity || res.complexity.time || 'O(1)'}</p>
                            <p class="text-base text-charcoal-500 mt-auto leading-relaxed">${res.complexity.timeExplanation || 'Constant time execution.'}</p>
                        </div>
                        <div class="bg-ivory-100 border border-ivory-300 p-6 rounded-sm flex flex-col">
                            <p class="text-sm font-bold uppercase tracking-widest text-charcoal-500 mb-4">Space Complexity</p>
                            <p class="text-3xl font-black text-brand-500 mb-2 font-mono">${res.complexity.spaceComplexity || res.complexity.space || 'O(1)'}</p>
                            <p class="text-base text-charcoal-500 mt-auto leading-relaxed">${res.complexity.spaceExplanation || 'Constant memory usage.'}</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            container.innerHTML += `
                <div class="bg-ivory-50 shadow-panel p-8 mt-12 animate-fade-up">
                    <h4 class="text-xl font-bold text-charcoal-600 mb-2 flex items-center gap-3 uppercase tracking-widest">
                        <i data-lucide="cpu" class="w-6 h-6 text-brand-500"></i> Complexity Analysis
                    </h4>
                    <p class="text-charcoal-400 text-lg">Complexity analysis unavailable for this snippet.</p>
                </div>
            `;
        }"""
        
    content = content.replace(complexity_old, complexity_new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Layout fixes applied successfully")

if __name__ == "__main__":
    fix_layout()
