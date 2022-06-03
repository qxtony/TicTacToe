from enum import Enum


class CellState(Enum):
    EMPTY: str = "*"
    X: str = "X"
    O: str = "O"
