#!/usr/bin/env python
# encoding: utf-8

import encodings
import pathlib
import typing

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Worksheet:
    def __init__(
        self,
        p_data: str,
    ):
        lines: list[list[str]] = list(map(
            lambda line: list(filter(
                lambda elem: len(elem),
                line.split(),
            )),
            p_data.splitlines()
        ))
        nb_columns: int = len(lines[0])
        assert all(
            len(line) == nb_columns
            for line in lines[1:]
        )

        self.__columns: list[list[str | int]] = [[] for _ in range(nb_columns)]
        for line in lines:
            for index, elem in enumerate(line):
                self.__columns[index].append(
                    int(elem)
                    if line != lines[-1] else
                    elem
                )

    def process_column(
        self,
        p_index: int,
    ) -> int:
        if self.__columns[p_index][-1] == "+":
            result: int = sum(self.__columns[p_index][:-1])
        else:
            result: int = 1
            for elem in self.__columns[p_index][:-1]:
                result *= elem
        return result

    def process_all_columns(
        self,
    ) -> typing.Generator[int, None, None]:
        return (self.process_column(
            p_index=index,
        ) for index in range(len(self.__columns)))

    def solve_problem(
        self,
    ) -> int:
        return sum(self.process_all_columns())


def main() -> None:
    worksheet: Worksheet = Worksheet(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    print(worksheet.solve_problem())


if __name__ == "__main__":
    main()
