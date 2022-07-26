from services.database.models.product import Comment
from services.database.repositories.base import Base


class CommentRepository(Base):
    model = Comment

    async def add_comment(self, obj_in, user_id):
        payload = obj_in.__dict__
        payload['user_id'] = user_id
        return await self._insert(**payload)

    async def delete_comment(self, comment_id: int):
        return await self._delete(self.model.id, comment_id)
