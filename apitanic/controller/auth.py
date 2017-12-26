import ujson as json
from apitanic.model.firebase import Firebase
from falcon import Request, Response


class FirebaseController:

    def __init__(self):
        self.firebase = Firebase()

    def on_post(self, req: Request, resp: Response):
        email = req.media.get('email')
        password = req.media.get('password')
        display_name = req.media.get('display_name')

        token = self.firebase.create_account(email, password, display_name)
        resp.body = json.dumps(***REMOVED***'data': ***REMOVED***
            'token': token
        ***REMOVED******REMOVED***)
