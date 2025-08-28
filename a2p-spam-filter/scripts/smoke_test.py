import requests, json
url = 'http://localhost:8080/check_sms'
payloads = [
    {'message':'Your OTP is 123456 for ICICI Bank.'},
    {'message':'Earn money fast at https://get-rich-fast.example.com'},
    {'message':'Your package with tracking ID 162556 has been shipped.'}
]
for p in payloads:
    r = requests.post(url, json=p)
    try:
        print(r.status_code, r.json())
    except Exception:
        print('error', r.text)
