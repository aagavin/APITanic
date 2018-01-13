from . import firebase_db
from . import CollectionReference


class Firebase(object):

    def __init__(self):
        self.favourites_ref = firebase_db.collection('favourites')
        self.friends_ref = firebase_db.collection('friends')

    async def collection_ref(self, collection_name: str):
        return firebase_db.collection(collection_name)

    async def search_one_where(
            self,
            document_ref: CollectionReference,
            field_name: str,
            field_value,
            operation: str = '=='
    ):
        return document_ref.where(field_name, operation, field_value).get()

    async def search_two_where(
            self,
            document_ref: CollectionReference,
            field_name1: str,
            field_value1: str,
            field_name2: str,
            field_value2,
            operation1: str = '==',
            operation2: str = '==',
    ):
        return document_ref\
            .where(field_name1, operation1, field_value1)\
            .where(field_name2, operation2, field_value2).get()

