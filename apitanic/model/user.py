from . import auth
from . import firebase_app
from apitanic.model.firebase import Firebase


class User(Firebase):

    def __init__(self):
        Firebase.__init__(self)

    @staticmethod
    async def get_user_by_id(userid: str):
        return auth.get_user(userid)

    @staticmethod
    async def get_user_id_by_token(token: str):
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']

    async def search_user(self, search_query) -> list:
        page = auth.list_users()
        user_list = []
        while page:
            for user in page.users:
                if search_query in user.email.lower() or search_query in user.display_name.lower():
                    user_list.append({
                        'uid': user.uid,
                        'display_name': user.display_name,
                        'email': user.email
                    })
            page = page.get_next_page()
        return user_list

    async def create_account(self, email: str, password: str, display_name: str) -> str:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=display_name,
            disabled=False,
            app=firebase_app
        )
        return auth.create_custom_token(user.uid)

    async def update_account(self, token: str, email: str, display_name: str, new_password: str) -> bool:
        uid = await User.get_user_id_by_token(token)
        auth.update_user(
            uid,
            email=email,
            display_name=display_name,
            password=new_password
        )
        return True
