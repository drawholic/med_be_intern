import pytest
from .test_init import get_db, client
from back.users.pd_models import UserSignUp
from back.users.crud import UserCrud


class UserTest:

    @pytest.fixture(autouse=True)
    def __init__(self):
        self.db = get_db

    @pytest.mark.asyncio
    async def test_create_user(self):
        user_data = {'email': 'test@email.com',
                     'password1': 'testpass',
                     'password2': 'testpass'}
        UserCrud(self.db).create_user(user=user_data)