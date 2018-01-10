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
                if search_query in user.email or search_query in user.display_name:
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

    def get_user_id_by_token(self, token: str):
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']

    def get_favouties_by_id(self, user_id: str, imdb_id: str):
        return self.favourites_ref.where('user_id', '==', user_id).where('imdb_id', '==', imdb_id).get()

    def get_all_favourites(self, token: str):
        user_id = self.get_user_id_by_token(token)
        favourite_document_ref = self.favourites_ref.where('user_id', '==', user_id).get()
        fav_list = []
        for fav in favourite_document_ref:
            fav_list.append(fav.to_dict())
        return fav_list

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

    def get_all_friends(self, token: str):
        user_id = self.get_user_id_by_token(token)
        favourite_document_ref = self.favourites_ref.where('user_id', '==', user_id).get()
        fri_list = []
        for fav in favourite_document_ref:
            fri_list.append(fav.to_dict())
        return fri_list

    def add_friend(self, token: str, friend_id: str):
        user_id = self.get_user_id_by_token(token)
        friends = self.get_favouties_by_id(user_id, friend_id)
        count = sum(1 for x in friends)
        if count != 0:
            return False
        friend = {'user_id': user_id, 'friend_id': friend_id}
        ref = self.favourites_ref.document()
        ref.set(friend)
        return True

    def delete_friend(self, token, friend_id):
        user_id = self.get_user_id_by_token(token)
        doc_refs = self.get_friends_by_id(user_id, friend_id)
        for fri in doc_refs:
            fri.reference.delete()
