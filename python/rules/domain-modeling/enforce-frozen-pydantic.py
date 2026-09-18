from pydantic import BaseModel, ConfigDict
import pydantic

# ruleid: python-enforce-frozen-pydantic
class MutableUser(BaseModel):
    id: str
    name: str

# ruleid: python-enforce-frozen-pydantic
class MutableAccount(pydantic.BaseModel):
    account_number: str

# ok: python-enforce-frozen-pydantic
class ImmutableUserV2(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    name: str

# ok: python-enforce-frozen-pydantic
class ImmutableAccountV1(BaseModel):
    id: str
    
    class Config:
        frozen = True

# ok: python-enforce-frozen-pydantic
class ImmutableDictConfig(BaseModel):
    model_config = {"frozen": True}
    id: str
