import os
import firebase_admin
from firebase_admin import credentials, firestore, auth

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
        pass

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

    @staticmethod
    def get_user_id_by_token(self, token:str):
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
