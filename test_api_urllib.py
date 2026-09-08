import urllib.request
import json

data = {
    "language": "python",
    "sourceCode": "def test_function()\n    print('Missing colon!')",
    "fileName": "test.py"
}

req = urllib.request.Request("http://localhost:8080/api/v1/detector/analyze", 
                             data=json.dumps(data).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(json.dumps(json.loads(response.read()), indent=2))
except Exception as e:
    print(e)
