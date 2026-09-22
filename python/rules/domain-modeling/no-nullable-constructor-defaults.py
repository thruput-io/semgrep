from typing import Optional, Union

class AbstractTokenProvider:
    pass

class TokenService:
    # ruleid: python-no-nullable-constructor-defaults
    def __init__(self, token_provider: AbstractTokenProvider | None = None):
        self.token_provider = token_provider

class OptionalService:
    # ruleid: python-no-nullable-constructor-defaults
    def __init__(self, token_provider: Optional[AbstractTokenProvider] = None):
        self.token_provider = token_provider

class UnionService:
    # ruleid: python-no-nullable-constructor-defaults
    def __init__(self, token_provider: Union[AbstractTokenProvider, None] = None):
        self.token_provider = token_provider

class KeywordOnlyService:
    # ruleid: python-no-nullable-constructor-defaults
    def __init__(self, *, token_provider: AbstractTokenProvider | None = None):
        self.token_provider = token_provider

class UntypedService:
    # ruleid: python-no-nullable-constructor-defaults
    def __init__(self, token_provider = None):
        self.token_provider = token_provider

class ExplicitService:
    # ok: python-no-nullable-constructor-defaults
    def __init__(self, token_provider: AbstractTokenProvider):
        self.token_provider = token_provider
