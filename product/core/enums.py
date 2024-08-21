from enum import IntEnum


class Limits(IntEnum):
    # Максимальная длина email для (CustomUser)
    MAX_LEN_EMAIL_FIELD = 250
    # Минимальный баланс для (CustomUser)
    MIN_BALANCE_AMOUNT = 0
    # Стартовй баланс для нового (CustomUser)
    START_BALANCE = 1000
    # Минимальная цена (Course)
    MIN_COURSE_PRICE = 0
