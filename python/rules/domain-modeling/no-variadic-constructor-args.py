class VehicleRepository:
    pass

class CustomerRepository:
    pass

class TypeService:
    pass

class VehicleService:
    # ruleid: python-no-variadic-constructor-args
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        customer_repository: CustomerRepository,
        *args: TypeService | None,
        **services: TypeService | None,
    ):
        self.vehicle_repository = vehicle_repository
        self.customer_repository = customer_repository
        self.type_service = args[0] if args else services.get("type_service")

class DynamicKwargsService:
    # ruleid: python-no-variadic-constructor-args
    def __init__(self, **kwargs):
        self.settings = kwargs

class ExplicitVehicleService:
    # ok: python-no-variadic-constructor-args
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        customer_repository: CustomerRepository,
        type_service: TypeService,
    ):
        self.vehicle_repository = vehicle_repository
        self.customer_repository = customer_repository
        self.type_service = type_service
