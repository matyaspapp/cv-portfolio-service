class TransactionSerializer:
    @staticmethod
    def serialize_one(transaction: dict) -> dict:
        """
        Serialize transaction data from MongoDB
        Accept only: _id, owner_id, asset, amount, price, currency, tags, date, type
        """
        valid_keys = {
            '_id',
            'owner_id',
            'asset', 
            'amount',
            'price',
            'currency',
            'tags',
            'date',
            'type'
        }
        if not isinstance(transaction, dict):
            raise TypeError

        if len(transaction) != 9:
            raise ValueError

        if set(transaction.keys()) != valid_keys:
            raise ValueError

        return {
            'id': str(transaction['_id']),
            'owner_id': str(transaction['owner_id']),
            'asset': transaction['asset'],
            'amount': transaction['amount'],
            'price': transaction['price'],
            'currency': transaction['currency'],
            'tags': transaction['tags'],
            'date': transaction['date'],
            'type': transaction['type']
        }

    @staticmethod
    def serialize_many(transactions: list[dict]) -> list[dict]:
        return [
            TransactionSerializer.serialize_one(transaction)
            for transaction in transactions
        ]
