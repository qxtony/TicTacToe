from random import choice
from typing import Any, Dict, List, NoReturn, Optional, Tuple, Union

from src.state import CellState


class TicTacToe:
    def __init__(self):

        self.size: int = 3
        self.player: CellState = self.get_random_first_player()
        self.rows: List[List[str]] = self.init_field()
        self.count_human_movements: int = 0
        self.bot_goes_first = False

        if self.player == CellState.O:
            self.move_bot()
            self.bot_goes_first = True

    def get_random_first_player(self) -> CellState:
        return choice([CellState.X, CellState.O])

    def init_field(self) -> List[List[str]]:
        return [[CellState.EMPTY.value] * self.size for _ in range(self.size)]

    def join_field(self) -> str:
        return "\n".join([" ".join(line) for line in self.rows])

    def create_borders(self) -> str:

        game_table = list(
            "┏━━━┳━━━┳━━━┓\n"
            "┃   ┃   ┃   ┃\n"
            "┣━━━╋━━━╋━━━┫\n"
            "┃   ┃   ┃   ┃\n"
            "┣━━━╋━━━╋━━━┫\n"
            "┃   ┃   ┃   ┃\n"
            "┗━━━┻━━━┻━━━┛"
        )

        cells = [[16, 20, 24], [44, 48, 52], [72, 76, 80]]

        for lineIndex, line in zip(cells, self.rows):
            for symbolIndex, symbol in zip(lineIndex, line):
                game_table[symbolIndex] = symbol

        return "".join(game_table)

    def check_valid_type_cell(self, cell: Any) -> Dict[str, Any]:

        if not cell.isdigit():
            return {"status": False, "value": "Вы не ввели номер клетки."}

        cell = int(cell)

        if cell > 9 or cell < 1:
            return {
                "status": False,
                "value": "Пожалуйста, выберите число в диапазоне от 1 до 9.",
            }

        return {"status": True, "value": cell}

    def move(self, cell: str) -> Optional[Any]:

        if self.player == CellState.O:
            self.move_bot()

        elif self.check_a_tie():
            return "Ничья!"

        response = self.check_valid_type_cell(cell)

        if not response["status"]:
            return response["value"]

        value = response["value"]

        y, x = self.get_cell_coordinates(value - 1)
        field = self.rows[y][x]

        if field == self.player.value:
            return "Вы уже выполнили ход на эту клетку."

        elif field == self.get_opponent():
            return "В это место уже сходил БОТ."

        self.rows[y][x] = self.player.value
        self.count_human_movements += 1

        self.switch_player()
        return self.move_bot()

    def move_bot(self) -> Optional[str]:

        if self.check_a_tie():
            return "Ничья!"

        x, y = self.get_best_move()

        self.rows[x][y] = self.player.value
        self.switch_player()

    def get_cell_coordinates(self, cell_number: int) -> Tuple[int, int]:
        return divmod(cell_number, self.size)

    def switch_player(self) -> NoReturn:
        self.player = [CellState.X, CellState.O][self.player == CellState.X]

    def get_opponent(self) -> str:

        return [CellState.X.value, CellState.O.value][
            self.player.value == CellState.X.value
        ]

    def check_a_tie(self) -> bool:

        field_of_cells: List[str] = sum(self.rows.copy(), [])
        return not (CellState.EMPTY.value in field_of_cells)

    def check_a_win(self) -> Union[str, bool]:

        inverted_board = [
            [line[index] for line in self.rows] for index in range(3)
        ]

        diagonal_board = [
            [self.rows[0][0], self.rows[1][1], self.rows[2][2]],
            [self.rows[2][0], self.rows[1][1], self.rows[0][2]],
        ]

        for check_element in [self.rows, inverted_board, diagonal_board]:
            answer = self.line_taken(check_element)

            if answer:
                return answer

        return False

    def line_taken(self, plaing_field: List[List[str]]) -> Union[str, bool]:

        for line in plaing_field:
            player = "".join(set(line))

            if len(player) == 1 and player in [
                CellState.X.value,
                CellState.O.value,
            ]:
                return player

        return False

    def create_dict_from_rows(
        self, check_on_opponent: bool = False
    ) -> Dict[int, str]:

        list_from_rows: List[str] = sum(self.rows.copy(), [])
        dict_from_rows: Dict[int, str] = {
            position: value
            for position, value in enumerate(list_from_rows)
            if (
                value == self.get_opponent()
                if check_on_opponent
                else value == CellState.EMPTY.value
            )
        }

        return dict_from_rows

    def delete_items(
        self, rows: Dict[int, str], items: List[int]
    ) -> Dict[int, str]:

        for value in rows.copy().keys():
            if value in items:
                del rows[value]

        return rows

    def get_best_move(self) -> Tuple[int, int]:

        if self.count_human_movements < 2:
            return self.get_first_move()

        elif self.count_human_movements in [4, 5]:
            return self.get_last_remaining_cell()

        return self.get_basic_move()

    def check_a_good_move(
        self,
        fixed_value: int,
        movements_check: Tuple[int, int, int],
        is_bot: bool = False,
    ) -> Dict[str, Any]:

        all_moves = [
            self.rows[movements_check[index]][fixed_value]
            for index in range(3)
        ] + [
            self.rows[fixed_value][movements_check[index]]
            for index in range(3)
        ]

        if is_bot:
            which_player_to_check = (self.player.value, self.get_opponent())

        else:
            which_player_to_check = (self.get_opponent(), self.player.value)

        is_possible_to_walk = (
            set([all_moves[3], all_moves[4]]) == set(which_player_to_check[0])
            and set([all_moves[5]]) != set(which_player_to_check[1]),
            set([all_moves[0], all_moves[1]]) == set(which_player_to_check[0])
            and set([all_moves[2]]) != set(which_player_to_check[1]),
        )

        if is_possible_to_walk[0]:
            return {"can": True, "data": (fixed_value, movements_check[2])}

        elif is_possible_to_walk[1]:
            return {"can": True, "data": (movements_check[2], fixed_value)}

        return {"can": False}

    def get_random_cell(
        self, items_to_removed: List[int] = []
    ) -> Tuple[int, int]:

        dictionary_field = self.create_dict_from_rows()
        dictionary_field = self.delete_items(
            dictionary_field, items_to_removed
        )

        random_key = choice(list(dictionary_field.keys()))
        y, x = self.get_cell_coordinates(random_key)

        return (y, x)

    def get_first_move(self) -> Tuple[int, int]:

        if self.rows[1][1] == self.get_opponent():
            return self.get_random_cell([0, 2, 6, 8])

        elif self.rows[1][1] == CellState.EMPTY.value:
            return (1, 1)

        rows = self.create_dict_from_rows()
        cell_number: int = 8 - list(rows.keys())[0]

        return self.get_random_cell([cell_number])

    def get_last_remaining_cell(self) -> Tuple[int, int]:

        rows = self.create_dict_from_rows()
        first_cell_in_rows = list(rows.keys())[0]

        y, x = self.get_cell_coordinates(first_cell_in_rows)
        return (y, x)

    def get_diagonal_move(self, is_opponent: bool = True) -> Tuple[int, int]:

        win_indices = [[0, 0, 2, 2], [2, 2, 0, 0], [0, 2, 2, 0], [2, 0, 0, 2]]
        player = self.player.value if is_opponent else self.get_opponent()

        for x, y, check_x, check_y in win_indices:

            if (
                set([self.rows[x][y], self.rows[1][1]]) == set(player)
                and self.rows[check_x][check_y] == CellState.EMPTY.value
            ):
                return (check_x, check_y)

    def get_extra_move(self, number_row: int) -> Tuple[int, int]:

        indices = [[0, 1], [1, 2]]

        for x, y in indices:

            if (
                self.rows[number_row][x] == self.player.value
                and self.rows[number_row][y] == CellState.EMPTY.value
            ):
                return (number_row, y)

            elif (
                self.rows[x][number_row] == self.player.value
                and self.rows[y][number_row] == CellState.EMPTY.value
            ):
                return (y, number_row)

    def get_basic_move(self) -> Union[Tuple[int, int], Any]:

        for number_row in range(self.size):

            for x in range(self.size - 1):
                number_row += x
                indices = [(0, 1, 2), (1, 2, 0), (0, 2, 1)]

                for Coordinates in indices:
                    if (
                        dictionary_answer := self.check_a_good_move(
                            number_row, Coordinates
                        )
                    )["can"]:
                        return dictionary_answer["data"]

                    elif (
                        dictionary_answer := self.check_a_good_move(
                            number_row, Coordinates, True
                        )
                    )["can"]:
                        return dictionary_answer["data"]

            if coordinates := self.get_diagonal_move():
                return coordinates

            elif coordinates := self.get_diagonal_move(is_opponent=False):
                return coordinates

            elif answer := self.get_extra_move(number_row):
                return answer
