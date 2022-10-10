from enum import Enum


class AuthTypesEnum(Enum):
    BEARER = 'bearer'
    BASIC = 'basic'
    DIGEST = 'digest'
