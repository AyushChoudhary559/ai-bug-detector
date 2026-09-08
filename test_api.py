import requests
import json

data = {
    "language": "python",
    "sourceCode": "def test_function()\n    print('Missing colon!')",
    "fileName": "test.py"
}

try:
    response = requests.post("http://localhost:8080/api/v1/detector/analyze", json=data)
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(e)
