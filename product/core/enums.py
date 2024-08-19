from enum import IntEnum


class Limits(IntEnum):
    # Максимальная длина email (CustomUser)
    MAX_LEN_EMAIL_FIELD = 250
    # Минимальный баланс юзера(CustomUser)
    MIN_BALANCE_AMOUNT = 0
    # Минимальный цена курса(Course)
    MIN_COURSE_PRICE = 0
