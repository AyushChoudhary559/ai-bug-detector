import re

def add_dependencies():
    with open('pom.xml', 'r', encoding='utf-8') as f:
        pom = f.read()

    deps = """
        <!-- JSqlParser for SQL validation -->
        <dependency>
            <groupId>com.github.jsqlparser</groupId>
            <artifactId>jsqlparser</artifactId>
            <version>4.6</version>
        </dependency>
        
        <!-- JSoup for HTML validation -->
        <dependency>
            <groupId>org.jsoup</groupId>
            <artifactId>jsoup</artifactId>
            <version>1.17.2</version>
        </dependency>
"""
    if "jsqlparser" not in pom:
        pom = pom.replace("</dependencies>", deps + "\n    </dependencies>")
        with open('pom.xml', 'w', encoding='utf-8') as f:
            f.write(pom)
        print("Dependencies added.")
    else:
        print("Dependencies already exist.")

if __name__ == "__main__":
    add_dependencies()
