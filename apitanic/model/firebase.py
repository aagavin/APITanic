import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from google.cloud.firestore_v1beta1 import CollectionReference

cred = credentials.Certificate({
    "type": os.getenv("type"),
    "project_id": os.getenv("project_id"),
    "private_key_id": os.getenv("private_key_id"),
    "private_key": os.getenv("private_key").replace('\\n', '\n'),
    "client_email": os.getenv("client_email"),
    "client_id": os.getenv("client_id"),
    "auth_uri": os.getenv("auth_uri"),
    "token_uri": os.getenv("token_uri"),
    "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("client_x509_cert_url")
})

firebase_app = firebase_admin.initialize_app(cred)
firebase_db = firestore.client()


class Firebase:

    def __init__(self):
        self.favourites_ref = firebase_db.collection('favourites')
        self.friends_ref = firebase_db.collection('friends')

    def search_user(self, search_query) -> list:
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

    def create_account(self, email: str, password: str, display_name: str) -> str:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=display_name,
            disabled=False,
            app=firebase_app
        )
        return auth.create_custom_token(user.uid)

    def get_user_by_id(self, userid: str):
        return auth.get_user(userid)

    def get_user_id_by_token(self, token: str):
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']

    def get_favouties_by_id(self, user_id: str, imdb_id: str):
        return self.favourites_ref.where('user_id', '==', user_id).where('imdb_id', '==', imdb_id).get()

    def __get_favourites(self, user_id: str):
        favourite_document_ref = self.favourites_ref.where('user_id', '==', user_id).get()
        fav_list = [fav.to_dict() for fav in favourite_document_ref]
        return fav_list

    def get_all_favourites(self, token: str):
        user_id = self.get_user_id_by_token(token)
        return self.__get_favourites(user_id)

    def add_favourite(self, token: str, imdb_id: str) -> bool:
        user_id = self.get_user_id_by_token(token)
        favs = self.get_favouties_by_id(user_id, imdb_id)
        count = sum(1 for x in favs)
        if count != 0:
            return False
        favourite = {'imdb_id': imdb_id, 'user_id': user_id}
        ref = self.favourites_ref.document()
        ref.set(favourite)
        return True

    def delete_favourite(self, token: str, imdb_id: str):
        user_id = self.get_user_id_by_token(token)
        doc_refs = self.get_favouties_by_id(user_id, imdb_id)
        for fav in doc_refs:
            fav.reference.delete()

    def get_friends_by_id(self, user_id: str, friend_id: str):
        return self.friends_ref.where('friend_id', '==', friend_id).where('user_id', '==', user_id).get()

    async def get_all_friends(self, token: str):
        user_id = self.get_user_id_by_token(token)
        friends_document_ref = self.friends_ref.where('user_id', '==', user_id).get()
        fri_list = []
        # get_user_by_id
        for fav in friends_document_ref:
            friend = self.get_user_by_id(fav.get('friend_id'))
            fri_list.append({
                'user_id': friend.uid,
                'friend': {
                    'display_name': friend.display_name,
                    'email': friend.email
                }
            })
        return fri_list

    def add_friend(self, token: str, friend_id: str):
        user_id = self.get_user_id_by_token(token)
        friends = self.get_friends_by_id(user_id, friend_id)
        count = sum(1 for x in friends)
        if count != 0:
            return False
        friend = {'user_id': user_id, 'friend_id': friend_id}
        ref = self.friends_ref.document()
        ref.set(friend)
        return True

    def delete_friend(self, token, friend_id):
        user_id = self.get_user_id_by_token(token)
        doc_refs = self.get_friends_by_id(user_id, friend_id)
        for fri in doc_refs:
            fri.reference.delete()

    async def get_recommendations(self, token: str):
        users_friends = await self.get_all_friends(token)
        user_fav = [a['imdb_id'] for a in self.get_all_favourites(token)]
        friend_ids = [fid['user_id'] for fid in users_friends]
        friends_fav = [self.__get_favourites(ffav) for ffav in friend_ids]
        friends_imdb_ids = []
        for ffav in friends_fav:
            for f in ffav:
                friends_imdb_ids.append(f['imdb_id'])
        return set(user_fav) - set(friends_imdb_ids)
