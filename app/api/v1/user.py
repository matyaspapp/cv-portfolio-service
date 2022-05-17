from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.repositories.user import UserRepository, get_user_repository
from app.schemas.user import User, UserResponse


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/users/auth')


user_router = APIRouter(prefix='/api/v1/users')


@user_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    tags=['Users']
)
def create_new_user(
    new_user: User,
    repository: UserRepository = Depends(get_user_repository)
):
    db_user = repository.get_by_username(new_user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This username is already taken..'
        )

    try:
        stored_user = repository.create(new_user)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user data..'
        )

    return repository.generate_jwt_token(stored_user)


@user_router.post(
    '/auth',
    status_code=status.HTTP_200_OK,
    tags=['Users']
)
def auth_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repository: UserRepository = Depends(get_user_repository)
):
    authenticate_data = repository.get_authenticated_user(
        form_data.username,
        form_data.password
    )

    if not authenticate_data['authenticated']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials..'
        )

    return repository.generate_jwt_token(authenticate_data['user'])


@user_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    tags=['Users']
)
def get_current_user(
    token: str = Depends(oauth2_schema),
    repository: UserRepository = Depends(get_user_repository)
):
    payload = repository.verify_jwt_token(token)
    if not payload['authorized']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials..'
        )

    return {'username': payload['username'], 'id': payload['id']}
