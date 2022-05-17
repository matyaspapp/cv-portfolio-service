import csv

from fastapi import UploadFile

class TransactionFileProcessor:
    @staticmethod
    async def import_csv(file: UploadFile) -> list[dict]:
        transactions = []
        content = await file.read()
        content = [row for row in content.decode().split('\n') if bool(row)]
        for row in content:
            row_data = row.split(',')
            transaction = {
                'asset': row_data[0],
                'amount': row_data[1],
                'historical_price': row_data[2],
                'date': row_data[3],
                'type': row_data[4],
                #constants
                'currency': 'USD',
                'tags': []
            }

            transactions.append(transaction)

        return transactions
