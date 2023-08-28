from enum import Enum


class Common(Enum):
    STEP_NUMBER="Step {}:"
    FAILED=f"{'-'*40} Failed"


class Menue(Enum):
    CUSTOMERS = "Customers"


class Page(Enum):
    CUSTOMERS = "Customers"
