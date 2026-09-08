import re

def update_security():
    with open('src/main/java/com/cs/bugdetector/security/SecurityConfig.java', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('"/api/reports/**"', '"/api/reports/**", "/api/health/**"')

    with open('src/main/java/com/cs/bugdetector/security/SecurityConfig.java', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated SecurityConfig")

if __name__ == "__main__":
    update_security()
