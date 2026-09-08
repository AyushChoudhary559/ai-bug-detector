$body = @{
    language = "python"
    sourceCode = "def test_function() `n    print('Missing colon!')"
    fileName = "test.py"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8080/api/v1/detector/analyze" -Method Post -Body $body -ContentType "application/json"
$response.Content
