from flask import Flask, request, Response
import requests

app = Flask(__name__)

TARGET_URL = "http://fi10.bot-hosting.net:20160"  # الموقع الأصلي

@app.route('/', defaults={'path': ''}, methods=["GET", "POST"])
@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    # بناء الرابط الأصلي
    url = f"{TARGET_URL}/{path}"
    
    # اختيار الطريقة GET أو POST
    if request.method == "POST":
        resp = requests.post(url, data=request.form, headers=request.headers, allow_redirects=False)
    else:
        resp = requests.get(url, params=request.args, headers=request.headers, allow_redirects=False)
    
    # تعديل المحتوى إذا لزم الأمر (روابط داخلية)
    content = resp.content
    content_type = resp.headers.get('Content-Type', 'text/html')
    
    return Response(content, status=resp.status_code, content_type=content_type)

if __name__ == "__main__":
    app.run(debug=True)
