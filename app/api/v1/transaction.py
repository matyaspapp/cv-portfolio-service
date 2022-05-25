import datetime

from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status

from app.api.v1.user import get_current_user

from app.nomicsapi.service import api_handler
from app.repositories.transaction import \
    TransactionRepository, \
    get_transaction_repository
from app.schemas.transaction import Transaction


transaction_router = APIRouter(prefix='/api/v1/transactions')


@transaction_router.get(
    '',
    status_code=status.HTTP_200_OK,
    tags=['Transactions']
)
def get_all_transaction(
    asset: Optional[str] = None,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    if asset:
        return {'data': repository.get_all_by_asset(asset)}

    transactions = repository.get_all(owner_id=user['id'])
    transactions = sorted(
        transactions,
        key=lambda t: datetime.datetime(
            int(t['date'].split('-')[0]),
            int(t['date'].split('-')[1]),
            int(t['date'].split('-')[2])
        ),
        reverse=True
    )
    return {'data': transactions}


@transaction_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    tags=['Transactions']
)
def create_new_transaction(
    new_transaction: Transaction,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    try:
        stored_transaction = repository.create(new_transaction)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid transaction data..'
        )

    return stored_transaction


@transaction_router.get(
    '/portfolio',
    status_code=status.HTTP_200_OK,
    tags=['Transactions']
)
async def calculate_portfolio(
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    portfolio = repository.calculate_portfolio(owner_id=user['id'])
    if not portfolio:
        return {'data': {'portfolio': {}}}

    api_data = await api_handler.get_asset_data(*portfolio['assets'].keys())

    return {'data': {'portfolio': portfolio, 'api_data': api_data}}


@transaction_router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions']
)
def get_transaction_by_id(
    id: str,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    try:
        lookup_transaction = repository.get_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction is not found..'
        )

    if not lookup_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction is not found..'
        )

    return lookup_transaction


@transaction_router.put(
    '/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions']
)
def update_transactionby_id(
    id: str,
    update_data: dict,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    try:
        updated_transaction = repository.update_by_id(id, update_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction could not be updated..'
        )

    if not updated_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction could not be updated..'
        )

    return updated_transaction

@transaction_router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions']
)
def delete_transaction_by_id(
    id: str,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    try:
        deleted_transaction = repository.delete_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction is not found..'
        )

    if not deleted_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction is not found..'
        )

    return {'data': deleted_transaction}


@transaction_router.post(
    '/file',
    status_code=status.HTTP_201_CREATED,
    tags=['Transactions']
)
async def import_transaction_csv(
    file: UploadFile,
    user: dict = Depends(get_current_user),
    repository: TransactionRepository = Depends(get_transaction_repository)
):  # pragma: no cover
    if file.filename.split('.')[-1] not in {'csv'}:
        return{'error': 'Wrong file type..'}

    try:
        transactions = await repository.import_csv(file)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid transaction data..'
        )

    try:
        for transaction in transactions:
            transaction['owner_id'] = user['id']
            repository.create(transaction)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid transaction data..'
        )

    return {'data': {'processed_file': file.filename, 'data': transactions}}
