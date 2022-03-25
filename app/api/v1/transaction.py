from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.transaction import TransactionRepository, get_transaction_repository
from app.schemas.transaction import Transaction


transaction_router = APIRouter(prefix='/api/v1/transactions')


@transaction_router.post('', status_code=status.HTTP_201_CREATED)
def create_new_transaction(
    new_transaction: Transaction,
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


@transaction_router.get('/{id}', status_code=status.HTTP_200_OK)
def get_transaction_by_id(
    id: str,
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


@transaction_router.get('', status_code=status.HTTP_200_OK)
def get_all_transaction(
    tag: Optional[str] = None,
    asset: Optional[str] = None,
    repository: TransactionRepository = Depends(get_transaction_repository)
):
    if asset:
        return {'data': repository.get_all_by_asset(asset)}

    return {'data': repository.get_all()}


@transaction_router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_transaction_by_id(
    id: str,
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
