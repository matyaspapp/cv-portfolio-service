class UserSerializer:
    @staticmethod
    def serialize_one(user: dict) -> dict:
        """
        Serialize user data from MongoDb
        Accept only: _id, username, hashed_password
        """
        valid_keys = {'_id', 'username', 'hashed_password'}

        if not isinstance(user, dict):
            raise TypeError

        if set(user.keys()) != valid_keys:
            raise ValueError

        return {
            'id': str(user['_id']),
            'hashed_password': user['hashed_password'],
            'username': user['username']
        }
