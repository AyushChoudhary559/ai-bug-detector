import re

def remove_login_entry():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Turn auth-view into auth-modal
    html = re.sub(
        r'<div id="auth-view" class="min-h-screen flex items-center justify-center p-6 bg-ivory-200 relative overflow-hidden">',
        r'<div id="auth-modal" class="hidden fixed inset-0 z-[100] flex items-center justify-center p-6 bg-charcoal-900/40 backdrop-blur-sm transition-opacity duration-300">',
        html
    )

    # 2. Add an absolute close button to auth-modal
    auth_form_start = r'<div class="max-w-md w-full bg-ivory-50 p-10 shadow-float relative z-10">'
    auth_form_start_replacement = r"""<div class="max-w-md w-full bg-ivory-50 p-10 shadow-float relative z-10">
        <button onclick="app.closeAuthModal()" class="absolute top-4 right-4 text-charcoal-400 hover:text-charcoal-600"><i data-lucide="x" class="w-6 h-6"></i></button>"""
    html = html.replace(auth_form_start, auth_form_start_replacement)

    # 3. Make main-app visible by default
    html = re.sub(
        r'<div id="main-app" class="hidden min-h-screen flex-col relative">',
        r'<div id="main-app" class="flex min-h-screen flex-col relative">',
        html
    )

    # 4. Update the Header to have toggleable auth states
    old_header_auth = r"""<div class="flex items-center gap-6">
                  <div class="w-8 h-8 rounded-full bg-charcoal-600 text-ivory-50 flex items-center justify-center text-xs font-bold"><span id="nav-profile-name">Me</span></div>
                  <button onclick="app.logout\(\)" class="text-sm font-bold uppercase tracking-widest text-charcoal-400 hover:text-charcoal-600 transition">Logout</button>
              </div>"""
    
    new_header_auth = r"""<div class="flex items-center gap-6">
                  <div class="w-8 h-8 rounded-full bg-charcoal-600 text-ivory-50 flex items-center justify-center text-xs font-bold"><span id="nav-profile-name">GU</span></div>
                  <div id="auth-actions-logged-out" class="block">
                      <button onclick="app.openAuthModal()" class="text-sm font-bold uppercase tracking-widest text-brand-500 hover:text-brand-600 transition">Sign In</button>
                  </div>
                  <div id="auth-actions-logged-in" class="hidden">
                      <button onclick="app.logout()" class="text-sm font-bold uppercase tracking-widest text-charcoal-400 hover:text-charcoal-600 transition">Logout</button>
                  </div>
              </div>"""
    
    html = re.sub(old_header_auth, new_header_auth, html)

    # 5. Update JS loadAuth() and updateAuthUI() and mockSignOut() and logout()
    js_load_auth = r"""loadAuth() {
                const user = localStorage.getItem('devsentry_user');
                if(user) {
                    const data = JSON.parse(user);
                    document.getElementById('auth-actions-logged-out').classList.add('hidden');
                    document.getElementById('auth-actions-logged-in').classList.remove('hidden');
                    document.getElementById('nav-profile-name').textContent = data.name.substring(0,2).toUpperCase();
                    document.getElementById('hero-name').textContent = data.name;
                    this.user = data;
                } else {
                    document.getElementById('auth-actions-logged-out').classList.remove('hidden');
                    document.getElementById('auth-actions-logged-in').classList.add('hidden');
                    document.getElementById('nav-profile-name').textContent = "GU";
                    document.getElementById('hero-name').textContent = "Developer";
                    this.user = null;
                }
            },"""
    html = re.sub(r'loadAuth\(\)\s*\{.*?(?=openAuthModal\(\)\s*\{)', js_load_auth + '\n            ', html, flags=re.DOTALL)

    js_update_auth_ui = r"""updateAuthUI() {
                const user = localStorage.getItem('devsentry_user');
                if(user) {
                    const data = JSON.parse(user);
                    document.getElementById('auth-actions-logged-out').classList.add('hidden');
                    document.getElementById('auth-actions-logged-in').classList.remove('hidden');
                    document.getElementById('nav-profile-name').textContent = data.name.substring(0,2).toUpperCase();
                    document.getElementById('hero-name').textContent = data.name;
                }
            },"""
    html = re.sub(r'updateAuthUI\(\)\s*\{.*?(?=mockSignOut\(\)\s*\{)', js_update_auth_ui + '\n            ', html, flags=re.DOTALL)

    js_mock_signout = r"""mockSignOut() {
                localStorage.removeItem('devsentry_user');
                this.user = null;
                document.getElementById('auth-actions-logged-in').classList.add('hidden');
                document.getElementById('auth-actions-logged-out').classList.remove('hidden');
                document.getElementById('nav-profile-name').textContent = "GU";
                document.getElementById('hero-name').textContent = "Developer";
                this.navigate('dashboard');
                this.showAlert("Signed Out", "You have been successfully signed out.");
            },"""
    html = re.sub(r'mockSignOut\(\)\s*\{.*?(?=toggleUserDropdown)', js_mock_signout + '\n            ', html, flags=re.DOTALL)

    # Remove the toggleUserDropdown entirely since it's not used anymore in the new layout
    html = re.sub(r'toggleUserDropdown\(e\)\s*\{.*?\},\n\s*logout\(\)\s*\{', r'logout() {', html, flags=re.DOTALL)


    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Login removed from entry flow successfully.")

if __name__ == "__main__":
    remove_login_entry()
