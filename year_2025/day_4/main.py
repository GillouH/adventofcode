#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings
import itertools
import typing

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Grid:
    def __init__(
        self,
        p_diagram: str,
    ):
        self.__lines: tuple[str, ...] = tuple(p_diagram.splitlines())
        assert all(
            len(line) == len(self.__lines[0])
            for line in self.__lines[1:]
        )

    @property
    def nb_lines(
        self,
    ) -> int:
        return len(self.__lines)

    @property
    def nb_columns(
        self,
    ) -> int:
        return len(self.__lines[0])

    def get_rolls_position(
        self,
    ) -> typing.Generator[tuple[int, int], None, None]:
        for line_index, line in enumerate(self.__lines):
            for column_index, element in enumerate(line):
                if element == "@":
                    yield line_index, column_index

    def get_adjacent_elements(
        self,
        p_line_index: int,
        p_column_index: int,
    ) -> typing.Generator[str, None, None]:
        adjacent_lines: tuple[int, ...] = tuple(filter(
            lambda line_index: 0 <= line_index < self.nb_lines,
            range(p_line_index-1, p_line_index+2),
        ))
        adjacent_columns: tuple[int, ...] = tuple(filter(
            lambda column_index: 0 <= column_index < self.nb_columns,
            range(p_column_index - 1, p_column_index + 2),
        ))

        for line_index, column_index in itertools.product(
            adjacent_lines,
            adjacent_columns,
        ):
            if (line_index, column_index) != (p_line_index, p_column_index):
                yield self.__lines[line_index][column_index]


def main() -> None:
    grid: Grid = Grid(
        p_diagram=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    nb_rolls_accessible: int = 0
    for roll_position in grid.get_rolls_position():
        line, column = roll_position
        nb_adjacent_rolls: int = tuple(grid.get_adjacent_elements(
            p_line_index=line,
            p_column_index=column,
        )).count("@")
        nb_rolls_accessible += int(nb_adjacent_rolls < 4)

    print(nb_rolls_accessible)


if __name__ == "__main__":
    main()
