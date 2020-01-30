from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import api
import urllib.parse

HOST = '127.0.0.1'
PORT = 8000

class CustomHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Object with parsed request path
        request_data = urllib.parse.urlparse(self.path)
        
        if re.fullmatch(r'^/object/\d+$', request_data.path):
            city_info = api.get_object_info(int(request_data.path[8:]))
            if city_info:
                self.response(200, {'content-type': 'application/json'}, city_info)
            else:
                self.send_error(404, explain='Информация о населенном пункте не найдена')

        elif re.fullmatch(r'^/page/\d+$', request_data.path):
            objects_count = None
            
            query_params = urllib.parse.parse_qs(request_data.query)
            if 'count' in query_params and len(query_params['count']) == 1 and query_params['count'][0].isdigit():
                objects_count = int(query_params['count'][0])

            if objects_count == None:
                self.send_error(400, explain='Неправильный формат GET параметра count=number - число объектов на странице')
            else:
                page = api.get_page(int(request_data.path[6:]), objects_count)
                if page:
                    self.response(200, {'content-type': 'application/json'}, page)
                else:
                    self.send_error(404, explain='Страница с указанным номером не найдена')

        elif re.fullmatch(r'^/comparison$', request_data.path):
            query_params = urllib.parse.parse_qs(request_data.query)
            if 'object1' not in query_params or 'object2' not in query_params or len(query_params['object1']) != 1 or len(query_params['object2']) != 1:
                self.send_error(400, explain='Неправильный формат GET параметров object1 и object2')
            else:
                comparison = api.get_objects_comparison(query_params['object1'][0], query_params['object2'][0])
                if comparison:
                    self.response(200, {'content-type': 'application/json'}, comparison)
                else:
                    self.send_error(404, explain='Один или оба населенных пункта для сравнения не найдены')

        elif re.fullmatch(r'^/?$', request_data.path):
            with open('readme.md', 'r', encoding='utf-8') as file:
                description = file.read()
            self.response(200, {'content-type': 'text/markdown'}, description)
            
        else:
            self.send_error(404)

    def response(self, code: int, headers: dict, content: str):
        '''
        Send response to the client.
        Arguments:
        - code: HTTP status code.
        - headers: HTTP headers.
        - content: any content to be sent.
        Return: None.
        '''

        self.send_response(code)
        for name in headers.keys():
            self.send_header(name, headers[name])
        self.end_headers()
        self.wfile.write(bytes(content, encoding='utf-16'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (HOST, PORT)
    http_serv = server_class(server_address, handler_class)
    http_serv.serve_forever()


if __name__ == '__main__':
    print('Server started')
    run(handler_class=CustomHTTPHandler)

