from http.server import *
import urllib
import json


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('127.0.0.1', 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def get_image_base64():
    with open('./ofiroshima_b64', 'r') as f:
        return f.read()


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        jdata = urllib.parse.parse_qs(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        is_valid = jdata['token'][0] == 'aaa' and jdata['password'][0] == 'bbb' # replaces actual logic
        lock_response = ''
        if is_valid:
            lock_response = get_image_base64()
        response_dict = {'isValid': is_valid, 'lockResponse': lock_response, 'calcTime': 1337}
        self.wfile.write(json.dumps(response_dict).encode('utf-8'))


if __name__ == '__main__':
    run(handler_class=MyHTTPRequestHandler)