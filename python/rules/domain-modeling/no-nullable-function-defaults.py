from typing import Optional, Union, override
import typing
import typing_extensions

# ruleid: python-no-nullable-function-defaults
def process_data(user_id: str, options: dict | None = None):
    pass

# ruleid: python-no-nullable-function-defaults
async def fetch_record(record_id: str, timeout: Optional[int] = None):
    pass

# ruleid: python-no-nullable-function-defaults
def format_output(data: str, formatter: Union[str, None] = None):
    pass

# ruleid: python-no-nullable-function-defaults
def untyped_func(name, extra=None):
    pass

# ruleid: python-no-nullable-function-defaults
def kwarg_only(*, flag: bool | None = None):
    pass

class BaseService:
    # ruleid: python-no-nullable-function-defaults
    def execute(self, task_id: str, context: dict | None = None):
        pass

class DataService(BaseService):
    # ok: python-no-nullable-function-defaults
    def __init__(self, client=None):
        self.client = client

    # ok: python-no-nullable-function-defaults
    @override
    def execute(self, task_id: str, context: dict | None = None):
        pass

    # ok: python-no-nullable-function-defaults
    @typing.override
    def execute_typed(self, task_id: str, context: dict | None = None):
        pass

    # ok: python-no-nullable-function-defaults
    @typing_extensions.override
    async def execute_async(self, task_id: str, context: dict | None = None):
        pass

    # ruleid: python-no-nullable-function-defaults
    def transform(self, data: str, formatter: str | None = None):
        return data

    # ruleid: python-no-nullable-function-defaults
    async def transform_async(self, data: str, formatter: str | None = None):
        return data

    # ok: python-no-nullable-function-defaults
    def explicit_transform(self, data: str, formatter: str):
        return data

    # ok: python-no-nullable-function-defaults
    def non_null_default(self, data: str, timeout: int = 30):
        return data
