import os, sys, urllib.request, json

token = os.environ.get("TELEGRAM_TOKEN", "")
print(f"Token: {token[:15]}..." if token else "ERROR: No token")

try:
    url = f"https://api.telegram.org/bot{token}/getMe"
    resp = urllib.request.urlopen(url, timeout=10)
    data = json.loads(resp.read())
    if data.get("ok"):
        print(f"✅ Token valid! Bot: @{data['result']['username']}")
    else:
        print(f"❌ Invalid token: {data.get('description')}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
