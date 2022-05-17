from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.user import get_current_user

from app.repositories.wallet import \
    WalletRepository, \
    get_wallet_repository
from app.schemas.wallet import Wallet


wallet_router = APIRouter(prefix='/api/v1/wallets')


@wallet_router.get('', status_code=status.HTTP_200_OK, tags=['Wallets'])
def get_all_wallet(
    user: dict = Depends(get_current_user),
    repository: WalletRepository = Depends(get_wallet_repository)
):
    return {'data': repository.get_all()}


@wallet_router.post('', status_code=status.HTTP_201_CREATED, tags=['Wallets'])
def create_new_wallet(
    new_wallet: Wallet,
    user: dict = Depends(get_current_user),
    repository: WalletRepository = Depends(get_wallet_repository)
):
    try:
        stored_wallet = repository.create(new_wallet)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid wallet data..'
        )

    return stored_wallet


@wallet_router.get('/{id}', status_code=status.HTTP_200_OK, tags=['Wallets'])
def get_wallet_by_id(
    id: str,
    user: dict = Depends(get_current_user),
    repository: WalletRepository = Depends(get_wallet_repository)
):
    try:
        lookup_wallet = repository.get_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wallet is not found..'
        )

    if not lookup_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wallet is not found..'
        )

    return lookup_wallet


@wallet_router.put('/{id}', status_code=status.HTTP_200_OK, tags=['Wallets'])
def update_wallet_by_id(
    id: str,
    update_data: dict,
    user: dict = Depends(get_current_user),
    repository: WalletRepository = Depends(get_wallet_repository)
):
    try:
        updated_wallet = repository.update_by_id(id, update_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wallet could not be updated..'
        )

    return updated_wallet


@wallet_router.delete('/{id}', status_code=status.HTTP_200_OK, tags=['Wallets'])
def delete_wallet_by_id(
    id: str,
    user: dict = Depends(get_current_user),
    repository: WalletRepository = Depends(get_wallet_repository)
):
    try:
        deleted_wallet = repository.delete_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wallet is not found..'
        )

    if not deleted_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wallet is not found..'
        )

    return {'data': deleted_wallet}
