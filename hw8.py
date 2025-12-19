from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json


def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not os.path.exists("pdfs"):
            os.makedirs("pdfs")
        def get_yandex_disk_files():
            try:
                resp = get("https://cloud-api.yandex.net/v1/disk/resources?path=python",
                           headers={"Authorization": f"OAuth {token}"})
                if resp.status_code == 200:
                    return resp.json()["_embedded"]["items"]
                return []
            except Exception:
                return []

        files = get_yandex_disk_files()

        def fname2html(fname):
            print("Файл", fname)
            all_names = [file["name"] for file in files]
            is_uploaded = fname in all_names
            bg_color = "background-color: rgba(0, 200, 0, 0.25)" if is_uploaded else ""
            return f"""
                <li style="display: flex; align-items: center; list-style: none; {bg_color}; padding: 8px" onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                    <p style="flex-basis: 50%; margin: 0">{fname}</p>
                    <button style="background: lightgray; border: 0; border-radius: 10px; height: 40px; padding: 0 20px; cursor: pointer;">{"Загружено" if is_uploaded else "Загрузить"}</button>
                </li>
            """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("""
            <html>
                <head>
                </head>
                <body>
                    <div style="max-width: 1100px; margin: 0 auto">
                        <h1>Загрузка файлов на Яндекс диск</h1>
                        <ul style="display: flex; flex-direction: column; gap: 10px; padding: 0">
                          <li style="display: flex; list-style: none; border-bottom: 2px solid gray; padding: 8px">
                            <p style="flex-basis: 50%; margin: 0">Файл</p>
                            <p style="flex-basis: 50%; margin: 0">Действие</p>
                          </li>
                          {files}
                        </ul>
                    </div>
                </body>
            </html>
        """.format(files="\n".join(map(fname2html, os.listdir("pdfs")))).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"python/{urllib.parse.quote(fname)}"
        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                   headers={"Authorization": token})
        print(resp.text)
        upload_url = json.loads(resp.text)["href"]
        print(upload_url)
        resp = put(upload_url, files={'file': (fname, open(local_path, 'rb'))})
        print(resp.status_code)
        self.send_response(200)
        self.end_headers()


token = input("Введите OAuth токен Яндекс.Диска: ").strip()
run(handler_class=HttpGetHandler)