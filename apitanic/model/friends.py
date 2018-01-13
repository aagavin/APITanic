from . import auth
from . import firebase_app
from apitanic.model.firebase import Firebase
from apitanic.model.user import User


class Friends(Firebase):
    def __init__(self):
        Firebase.__init__(self)

    async def get_friends_by_id(self, user_id: str, friend_id: str):
        return self.friends_ref.where('friend_id', '==', friend_id).where('user_id', '==', user_id).get()

    async def get_all_friends(self, token: str):
        user_id = await User.get_user_id_by_token(token)
        friends_document_ref = self.friends_ref.where('user_id', '==', user_id).get()
        fri_list = []
        # get_user_by_id
        for fav in friends_document_ref:
            friend = await User.get_user_by_id(fav.get('friend_id'))
            fri_list.append({
                'user_id': friend.uid,
                'friend': {
                    'display_name': friend.display_name,
                    'email': friend.email
                }
            })
        return fri_list

    async def add_friend(self, token: str, friend_id: str):
        user_id = await User.get_user_id_by_token(token)
        friends = await self.get_friends_by_id(user_id, friend_id)
        count = sum(1 for x in friends)
        if count != 0:
            return False
        friend = {'user_id': user_id, 'friend_id': friend_id}
        ref = self.friends_ref.document()
        ref.set(friend)
        return True

    async def delete_friend(self, token, friend_id):
        user_id = await User.get_user_id_by_token(token)
        doc_refs = await self.get_friends_by_id(user_id, friend_id)
        for fri in doc_refs:
            fri.reference.delete()
