#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings
import typing

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Database:
    def __init__(
        self,
        p_data: str,
    ):
        lines: list[str] = p_data.splitlines()
        self.__ranges: list[range] = list()
        self.__ids: list[int] = list()

        first_part: bool = True
        for line in lines:
            if line == str():
                first_part: bool = False
            elif first_part:
                range_numbers: list[int] = list(map(int, line.split("-")))
                self.__ranges.append(range(
                    range_numbers[0],
                    range_numbers[1] + 1,
                ))
            else:
                self.__ids.append(int(line))

    def is_fresh(
        self,
        p_id: int,
    ) -> bool:
        return any(p_id in l_range for l_range in self.__ranges)

    def get_fresh_ids(
        self,
    ) -> typing.Generator[int, None, None]:
        yield from filter(
            lambda p_id: any(
                p_id in l_range
                for l_range in self.__ranges
            ),
            self.__ids,
        )


def main() -> None:
    database: Database = Database(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    print(len(tuple(database.get_fresh_ids())))


if __name__ == "__main__":
    main()
