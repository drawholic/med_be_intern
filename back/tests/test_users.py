import pytest
from .test_init import get_db, client
from ..users.pd_models import UserSignUp
from ..users.crud import UserCrud
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_user(get_db: AsyncSession):
    user_data = {'email': 'test@email.com',
                         'password1': 'testpass',
                         'password2': 'testpass'}
    user_data = UserSignUp(**user_data)
    user = await UserCrud(get_db).create_user(user=user_data)
    assert user.email == user_data.get('email')

# class TestUser:
#
#     @pytest.mark.asyncio
#     async def test_create_user(self, db: AsyncSession = Depends(get_db)):
#         user_data = {'email': 'test@email.com',
#                      'password1': 'testpass',
#                      'password2': 'testpass'}
#         user_data = UserSignUp(**user_data)
#         # db = await get_db()
#         user = await UserCrud(db).create_user(user=user_data)
#         assert user.email == user_data.get('email')