from random import choice
from typing import Any, Dict, List, Optional, Tuple, Union

from src.state import CellState


class Bot:
    def __init__(self, model):
        self.model = model

    def move(self) -> Optional[str]:

        if self.model.check_a_tie():
            return "Ничья!"

        x, y = self.get_best_move()
        self.model.rows[x][y] = self.model.player.value
        self.model.switch_player()

    def create_dict_from_rows(
        self, check_on_opponent: bool = False
    ) -> Dict[int, str]:

        list_from_rows: List[str] = sum(self.model.rows.copy(), [])
        dict_from_rows: Dict[int, str] = {
            position: value
            for position, value in enumerate(list_from_rows)
            if (
                value == self.model.get_opponent()
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

        if self.model.count_human_movements < 2:
            return self.get_first_move()

        elif self.model.count_human_movements in [4, 5]:
            return self.get_last_remaining_cell()

        return self.get_basic_move()

    def check_a_good_move(
        self,
        fixed_value: int,
        movements_check: Tuple[int, int, int],
        is_bot: bool = False,
    ) -> Dict[str, Any]:

        all_moves = [
            self.model.rows[movements_check[index]][fixed_value]
            for index in range(3)
        ] + [
            self.model.rows[fixed_value][movements_check[index]]
            for index in range(3)
        ]

        if is_bot:
            which_player_to_check = (
                self.model.player.value,
                self.model.get_opponent(),
            )

        else:
            which_player_to_check = (
                self.model.get_opponent(),
                self.model.player.value,
            )

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
        y, x = self.model.get_cell_coordinates(random_key)

        return (y, x)

    def get_first_move(self) -> Tuple[int, int]:

        if self.model.rows[1][1] == self.model.get_opponent():
            return self.get_random_cell([0, 2, 6, 8])

        elif self.model.rows[1][1] == CellState.EMPTY.value:
            return (1, 1)

        rows = self.create_dict_from_rows()
        cell_number: int = 8 - list(rows.keys())[0]

        return self.get_random_cell([cell_number])

    def get_last_remaining_cell(self) -> Tuple[int, int]:

        rows = self.create_dict_from_rows()
        first_cell_in_rows = list(rows.keys())[0]

        y, x = self.model.get_cell_coordinates(first_cell_in_rows)
        return (y, x)

    def get_diagonal_move(self, is_opponent: bool = True) -> Tuple[int, int]:

        win_indices = [[0, 0, 2, 2], [2, 2, 0, 0], [0, 2, 2, 0], [2, 0, 0, 2]]
        player = (
            self.model.player.value
            if is_opponent
            else self.model.get_opponent()
        )

        for x, y, check_x, check_y in win_indices:

            if (
                set([self.model.rows[x][y], self.model.rows[1][1]])
                == set(player)
                and self.model.rows[check_x][check_y]
                == CellState.EMPTY.value
            ):
                return (check_x, check_y)

    def get_extra_move(self, number_row: int) -> Tuple[int, int]:

        indices = [[0, 1], [1, 2]]

        for x, y in indices:

            if (
                self.model.rows[number_row][x] == self.model.player.value
                and self.model.rows[number_row][y] == CellState.EMPTY.value
            ):
                return (number_row, y)

            elif (
                self.model.rows[x][number_row] == self.model.player.value
                and self.model.rows[y][number_row] == CellState.EMPTY.value
            ):
                return (y, number_row)

    def get_basic_move(self) -> Union[Tuple[int, int], Any]:

        for number_row in range(self.model.size):

            for x in range(self.model.size - 1):
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
