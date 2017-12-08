import ujson as json
import falcon
from falcon import Request,Response


class HelloWorld:

    def on_get(self, req :Request, resp: Response):
        """
        Hello world example
        :param req:
        :param resp:
        :return:
        """
        
        resp.body = json.dumps(
            {
                'success': True,
                'name': 'API Tanic',
                'tagline': 'The API that never goes down',
                'tagline2': 'always asyncs',
                'AKA': [
                    'Planet of the API\'s',
                    'Life of API',
                    'Snakes on an API',
                    'Lord of APIs',
                    'Cloudy with a change of APIs'
                ]
            }
        )


api = falcon.API()
api.add_route('/', HelloWorld())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    print('--> server ready')
    httpd.serve_forever()
