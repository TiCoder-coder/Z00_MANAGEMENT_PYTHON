from enum import Enum

class CustomEnum(Enum):
    @property
    def description(self):
        pass

class Gender(CustomEnum):
    pass

class HealthStatus(CustomEnum):
    pass

class TypeFood(CustomEnum):
    pass

class Climate(CustomEnum):
    pass

class Role(CustomEnum):
    pass
