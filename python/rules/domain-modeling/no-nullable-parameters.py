from abc import abstractmethod
from typing import Optional, Union, override
import typing
import typing_extensions

class BaseModel:
    pass

class EventPublisher:
    # ruleid: python-no-nullable-parameters
    @abstractmethod
    async def publish(self, event: BaseModel, key: str | None) -> None:
        pass

    # ruleid: python-no-nullable-parameters
    def publish_opt(self, event: BaseModel, key: Optional[str]) -> None:
        pass

    # ruleid: python-no-nullable-parameters
    def publish_union(self, event: BaseModel, key: Union[str, None]) -> None:
        pass

    # ruleid: python-no-nullable-parameters
    def publish_default(self, event: BaseModel, key = None) -> None:
        pass

    # ruleid: python-no-nullable-parameters
    def kwarg_only(*, flag: bool | None = None):
        pass

    # ok: python-no-nullable-parameters
    def safe_publish(self, event: BaseModel, key: str) -> None:
        pass

    # ok: python-no-nullable-parameters
    def default_value(self, event: BaseModel, timeout: int = 30) -> None:
        pass

class ConcretePublisher(EventPublisher):
    # ok: python-no-nullable-parameters
    def __init__(self, client=None):
        self.client = client

    # ok: python-no-nullable-parameters
    @override
    async def publish(self, event: BaseModel, key: str | None) -> None:
        pass

    # ok: python-no-nullable-parameters
    @typing.override
    def publish_opt(self, event: BaseModel, key: Optional[str]) -> None:
        pass

    # ok: python-no-nullable-parameters
    @typing_extensions.override
    def publish_union(self, event: BaseModel, key: Union[str, None]) -> None:
        pass
