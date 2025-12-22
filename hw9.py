from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from typing import List
from urllib.parse import urlparse

class TodoServer(BaseHTTPRequestHandler):
    tasks_list = []
    FILE_NAME = "tasks.txt"
    
    @classmethod
    def load_tasks(cls):
        if os.path.exists(cls.FILE_NAME):
            try:
                with open(cls.FILE_NAME, 'r', encoding='utf-8') as f:
                    cls.tasks_list = json.load(f)
            except (json.JSONDecodeError, IOError):
                cls.tasks_list = []
    
    @classmethod
    def save_tasks(cls):
        try:
            with open(cls.FILE_NAME, 'w', encoding='utf-8') as f:
                json.dump(cls.tasks_list, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def do_GET(self):
        match self.path:
            case "/tasks":
                self.get_tasks()
            case _:
                self.not_found()

    def do_POST(self):
        path = urlparse(self.path).path
        paths = [p for p in path.split("/") if p]

        if not paths:
            return self.not_found()

        match (paths[0]):
            case "tasks":
               if len(paths) == 1:
                    return self.create_task()
               elif len(paths) == 3 and paths[2] == "complete":
                   return self.task_complete(paths)
               else:
                   return self.not_found()
            case _:
                return self.not_found()

    def create_task(self):
        data = self.read_json()
        if data is None:
            return

        title = data.get("title")
        priority = data.get("priority")

        if self.is_nonempty_str(title) and self.is_nonempty_str(priority):
            new_task = {"id": len(self.tasks_list) + 1,**data, "isDone": False}
            self.tasks_list.append(new_task)
            self.save_tasks()  # Просто self.save_tasks()
            return self.send_http_response(data=new_task)
        return self.send_http_response(400, {"error":"Validation error","fields":{"title":"required","priority":"required"}})

    def task_complete(self, paths: List[str]):
        _, id, action = paths
        try:
            task_id = int(id)
        except ValueError:
            return self.send_http_response(400, {"error": "Incorrect id"})

        task_index = next((i for i, task in enumerate(self.tasks_list)
                      if task["id"] == task_id), -1)
        if task_index != -1:
            self.tasks_list[task_index].update({"isDone": True})
            self.save_tasks()
            return self.send_http_response()

        return self.send_http_response(404)

    def get_tasks(self):
        self.send_http_response(data=self.tasks_list)

    def not_found(self):
        self.send_http_response(404)

    def send_http_response(self, status_code=200, data=None):
        self.send_response(status_code)
        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", f"{len(body)}")

        else:
            self.send_header("Content-Length", "0")
        self.end_headers()

        if body:
            self.wfile.write(body)

    def read_json(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode("utf-8"))
            return data
        except json.JSONDecodeError:
            return self.send_http_response(400,{"error": "Invalid JSON"})

    def is_nonempty_str(self, s: str) -> bool:
        return isinstance(s, str) and bool(s.strip())

def run_server(server_class=HTTPServer, handler_class=TodoServer):
    PORT = 8000
    server_address = ("", PORT)
    
    handler_class.load_tasks()
    
    server = server_class(server_address, handler_class)

    try:
        print(f"Сервер запустился на http://localhost:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

run_server()
