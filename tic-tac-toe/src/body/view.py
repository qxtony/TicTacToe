class View:
    def __init__(self, model):
        self.model = model

    def join_field(self) -> str:
        return "\n".join([" ".join(line) for line in self.model.rows])

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

        for lineIndex, line in zip(cells, self.model.rows):
            for symbolIndex, symbol in zip(lineIndex, line):
                game_table[symbolIndex] = symbol

        return "".join(game_table)
