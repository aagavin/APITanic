from apitanic.model.firebase import Firebase
from apitanic.model.friends import Friends
from apitanic.model.user import User


class Favourites(Firebase):
    def __init__(self):
        Firebase.__init__(self)

    async def get_favoutie_by_id(self, user_id: str, imdb_id: str):
        return self.favourites_ref.where('user_id', '==', user_id).where('imdb_id', '==', imdb_id).get()

    async def __get_favourites(self, user_id: str) -> list:
        favourite_document_ref = self.favourites_ref.where('user_id', '==', user_id).get()
        return [fav.to_dict() for fav in favourite_document_ref]

    async def get_all_favourites(self, token: str) -> list:
        user_id = await User.get_user_id_by_token(token)
        return await self.__get_favourites(user_id)

    async def add_favourite(self, token: str, imdb_id: str) -> bool:
        user_id = await User.get_user_id_by_token(token)
        favs = await self.get_favoutie_by_id(user_id, imdb_id)
        count = sum(1 for x in favs)
        if count != 0:
            return False
        favourite = {'imdb_id': imdb_id, 'user_id': user_id}
        ref = self.favourites_ref.document()
        ref.set(favourite)
        return True

    async def delete_favourite(self, token: str, imdb_id: str) -> None:
        user_id = await User.get_user_id_by_token(token)
        doc_refs = await self.get_favoutie_by_id(user_id, imdb_id)
        for fav in doc_refs:
            fav.reference.delete()

    async def get_recommendations(self, token: str):
        friends = Friends()
        users_friends = await friends.get_all_friends(token)
        user_fav = [a['imdb_id'] for a in await self.get_all_favourites(token)]
        friend_ids = [fid['user_id'] for fid in users_friends]
        friends_fav = [self.__get_favourites(ffav) for ffav in friend_ids]
        friends_imdb_ids = []
        for ffav in friends_fav:
            for f in await ffav:
                friends_imdb_ids.append(f['imdb_id'])
        return set(user_fav) - set(friends_imdb_ids)
