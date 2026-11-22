import os
import json
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
ADMIN_PASSWORD = "Mahakal@989#"  # <--- Set your secret password here
DIR = os.path.dirname(os.path.abspath(__file__))

class BSDKAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        # API to fetch current config
        if self.path == '/api/config':
            config_file = os.path.join(DIR, "config.json")
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    data = f.read()
            else:
                data = json.dumps({"url": "./bsdk-clube.apk", "version": "v1.0.0", "size": "15.0 MB"})
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(data.encode('utf-8'))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/upload':
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self._send_json(400, {"success": False, "message": "Expected multipart/form-data"})
                return

            # Extract boundary
            match = re.search(r'boundary=([^\s;]+)', content_type)
            if not match:
                self._send_json(400, {"success": False, "message": "No boundary found"})
                return

            boundary = match.group(1).encode('utf-8')
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            parts = body.split(b'--' + boundary)
            password = None
            version = "v1.0.0"
            custom_size = None
            file_data = None
            file_name = "bsdk-clube.apk"

            for part in parts:
                if not part or part == b'--\r\n' or part == b'--':
                    continue
                
                header_end = part.find(b'\r\n\r\n')
                if header_end == -1:
                    continue
                
                header = part[:header_end].decode('utf-8', errors='ignore')
                content = part[header_end + 4:]
                if content.endswith(b'\r\n'):
                    content = content[:-2]

                if 'name="password"' in header:
                    password = content.decode('utf-8', errors='ignore').strip()
                elif 'name="version"' in header:
                    version = content.decode('utf-8', errors='ignore').strip()
                elif 'name="size"' in header:
                    custom_size = content.decode('utf-8', errors='ignore').strip()
                elif 'name="apk_file"' in header:
                    file_data = content
                    fn_match = re.search(r'filename="([^"]+)"', header)
                    if fn_match:
                        file_name = fn_match.group(1)

            if password != ADMIN_PASSWORD:
                self._send_json(401, {"success": False, "message": "Invalid password! Only owner can upload."})
                return

            if not file_data or len(file_data) == 0:
                self._send_json(400, {"success": False, "message": "No APK file selected."})
                return

            # Save APK
            apk_path = os.path.join(DIR, "bsdk-clube.apk")
            with open(apk_path, "wb") as f:
                f.write(file_data)

            size_mb = custom_size if custom_size else f"{len(file_data) / (1024 * 1024):.1f} MB"
            config_data = {
                "url": "./bsdk-clube.apk",
                "version": version or "v1.0.0",
                "size": size_mb
            }
            with open(os.path.join(DIR, "config.json"), "w") as f:
                json.dump(config_data, f, indent=2)

            self._send_json(200, {
                "success": True, 
                "message": f"New APK successfully uploaded and updated! (Size: {size_mb})"
            })
            return

        self.send_error(404)

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


if __name__ == '__main__':
    os.chdir(DIR)
    cfg_path = os.path.join(DIR, "config.json")
    if not os.path.exists(cfg_path):
        with open(cfg_path, "w") as f:
            json.dump({"url": "./bsdk-clube.apk", "version": "v1.0.0", "size": "15.0 MB"}, f, indent=2)

    server = HTTPServer(('0.0.0.0', PORT), BSDKAppHandler)
    print("=" * 60)
    print(f"🚀 BSDK Clube Server Started!")
    print(f"👉 Local Access: http://localhost:{PORT}")
    print(f"🔑 Secret Password: {ADMIN_PASSWORD}")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
