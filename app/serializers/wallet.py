class WalletSerializer:
    @staticmethod
    def serialize_one(wallet: dict) -> dict:
        """
        Serialize transaction data from MongoDB
        Accept only: _id, owner_id, address, chain
        """
        valid_keys = {'_id', 'owner_id', 'address', 'chain'}
        if not isinstance(wallet, dict):
            raise TypeError

        if set(wallet.keys()) != valid_keys:
            raise ValueError

        return {
            'id': str(wallet['_id']),
            'owner_id': str(wallet['owner_id']),
            'address': wallet['address'],
            'chain': wallet['chain']
        }

    @staticmethod
    def serialize_many(wallets: list[dict]) -> list[dict]:
        if not isinstance(wallets, list):
            raise TypeError

        return [
            WalletSerializer.serialize_one(wallet)
            for wallet in wallets
        ]
