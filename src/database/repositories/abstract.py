from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Sequence

from sqlalchemy import delete, select, ColumnExpressionArgument, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.functions import count

from ..models import BaseModel

AbstractModel = TypeVar("AbstractModel", bound=BaseModel)


class AbstractRepo(ABC, Generic[AbstractModel]):
    def __init__(
            self,
            session: AsyncSession,
            model_type: type[AbstractModel]
    ):
        self.session = session
        self.model_type = model_type

    @abstractmethod
    async def new(self, *args, **kwargs) -> AbstractModel:
        pass

    async def delete(
            self,
            clause: ColumnExpressionArgument | tuple[ColumnExpressionArgument]
    ) -> None:
        if not isinstance(clause, tuple):
            clause = (clause,)

        stmt = delete(self.model_type).where(*clause)
        await self.session.execute(stmt)

    async def get(
            self,
            clause: ColumnExpressionArgument | tuple[ColumnExpressionArgument]
    ) -> AbstractModel:
        if not isinstance(clause, tuple):
            clause = (clause,)

        stmt = select(self.model_type).where(*clause)
        result = await self.session.execute(stmt)

        return result.scalar()

    async def get_all_iter(
            self,
            clause: ColumnExpressionArgument | tuple[ColumnExpressionArgument] | None = None,
            order_by: InstrumentedAttribute | tuple[InstrumentedAttribute] | None = None,
            limit: int = None
    ) -> ScalarResult[AbstractModel]:
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
            clause: ColumnExpressionArgument | tuple[ColumnExpressionArgument] | None = None,
            order_by: InstrumentedAttribute | tuple[InstrumentedAttribute] | None = None,
            limit: int = None
    ) -> Sequence[AbstractModel]:
        result = await self.get_all_iter(
            clause=clause,
            order_by=order_by,
            limit=limit
        )

        return result.all()

    async def count(
            self,
            clause: ColumnExpressionArgument | tuple[ColumnExpressionArgument] | None = None
    ) -> int:
        stmt = select(count()).select_from(self.model_type)

        if clause is not None:
            if not isinstance(clause, tuple):
                clause = (clause,)
            stmt = stmt.where(*clause)

        result = await self.session.execute(stmt)

        return result.scalar()
