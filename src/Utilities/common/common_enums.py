from enum import Enum


class Status(Enum):
    EQUAL = "equal"
    NOT_EQUAL = "not equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"


class Menue(Enum):
    CUSTOMERS = "Customers"


class Page(Enum):
    CUSTOMERS = "Customers"
