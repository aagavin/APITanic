from imdbpie import Imdb
import ujson as json
from falcon import Request, Response


class ImdbController:
    imdb = Imdb()

    def __init__(self):
        pass

    def on_get(self, req: Request, resp: Response, imdbtype):
        if imdbtype == 'getTitleById':
            id = req.get_param('id')
            title = self.imdb.get_title_by_id(id)
            resp.body = json.dumps({
                'data': title
            })
        elif imdbtype == 'search':
            search = req.get_param('q')
            movie = self.imdb.search_for_title(search)
            resp.body = json.dumps({
                'data': movie
            })
        else:
            resp.body = json.dumps({
                'error': 'imdb request error'
            })
