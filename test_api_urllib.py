import urllib.request
import json

data = {
    "language": "java",
    "sourceCode": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello DevSentry AI\");\n    }\n}",
    "fileName": "Main.java"
}

req = urllib.request.Request("http://localhost:8080/api/v1/detector/analyze", 
                             data=json.dumps(data).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(json.dumps(json.loads(response.read()), indent=2))
except Exception as e:
    print(e)
