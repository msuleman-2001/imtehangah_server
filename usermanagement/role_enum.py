from enum import Enum


class RoleEnum(Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]
