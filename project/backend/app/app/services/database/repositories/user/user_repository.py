from app.services.database.models.user.user import User
from app.services.database.repositories.base import Base, Model
from app.services.database.schemas.user.user import UserCreate


class UserRepository(Base):
    model = User

    def __init__(self, session, password_hasher):
        super().__init__(session)
        self._password_hasher = password_hasher

    async def get_user(self, name: str) -> Model:
        return await self._select_one(self.model.name == name)

    async def get_user_id(self, id: int) -> Model:
        return await self._select_one(self.model.id == id)

    async def get_by_email(self, email: str) -> Model:
        return await self._select_one(self.model.email == email)

    async def create_user(self, obj_in: UserCreate) -> Model:
        payload = obj_in.__dict__
        payload['hashed_password'] = self._password_hasher.get_password_hash(obj_in.password)
        del payload['password']
        return await self._insert(**payload)

    async def activate_user(self, email: str):
        payload = {'is_active': True}
        return await self._update(self.model.email == email, **payload)

    async def password_change_user(self, email: str, password: str):
        payload = {'hashed_password': self._password_hasher.get_password_hash(password)}
        return await self._update(self.model.email == email, **payload)

    async def delete_user(self, email: str):
        return await self._delete(self.model.email, email)
