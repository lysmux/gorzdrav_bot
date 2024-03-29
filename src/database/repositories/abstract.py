from abc import abstractmethod, ABC
from typing import Sequence

from sqlalchemy import delete, select, ColumnExpressionArgument, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.functions import count

from ..models import BaseModel

type ClauseExp = ColumnExpressionArgument | tuple[*ColumnExpressionArgument]
type OrderExp = InstrumentedAttribute | tuple[*InstrumentedAttribute]


class AbstractRepo[T: BaseModel](ABC):
    def __init__(
            self,
            session: AsyncSession,
            model_type: type[T]
    ):
        self.session = session
        self.model_type = model_type

    @abstractmethod
    async def new(self, *args, **kwargs) -> T:
        pass

    async def delete(
            self,
            clause: ClauseExp
    ) -> None:
        if not isinstance(clause, tuple):
            clause = (clause,)

        stmt = delete(self.model_type).where(*clause)
        await self.session.execute(stmt)

    async def get(
            self,
            clause: ClauseExp
    ) -> T:
        if not isinstance(clause, tuple):
            clause = (clause,)

        stmt = select(self.model_type).where(*clause)
        result = await self.session.execute(stmt)

        return result.scalar()

    async def get_all_iter(
            self,
            clause: ClauseExp | None = None,
            order_by: OrderExp | None = None,
            limit: int | None = None
    ) -> ScalarResult[T]:
        stmt = select(self.model_type).limit(limit)

        if clause is not None:
            if not isinstance(clause, tuple):
                clause = (clause,)
            stmt = stmt.where(*clause)

        if order_by is not None:
            if not isinstance(order_by, tuple):
                order_by = (order_by,)
            stmt = stmt.order_by(*order_by)

        result = await self.session.execute(stmt)

        return result.scalars()

    async def get_all(
            self,
            clause: ClauseExp | None = None,
            order_by: OrderExp | None = None,
            limit: int | None = None
    ) -> Sequence[T]:
        result = await self.get_all_iter(
            clause=clause,
            order_by=order_by,
            limit=limit
        )

        return result.all()

    async def count(
            self,
            clause: ClauseExp | None = None
    ) -> int:
        stmt = select(count()).select_from(self.model_type)

        if clause is not None:
            if not isinstance(clause, tuple):
                clause = (clause,)
            stmt = stmt.where(*clause)

        result = await self.session.execute(stmt)

        return result.scalar()
