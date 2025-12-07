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

        self.__ranges.sort(
            key=lambda l_range: (l_range.start, l_range.stop - l_range.start)
        )

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

    def get_max_nb_fresh_ids(
        self,
    ) -> int:
        min_id: int = min(map(lambda l_range: l_range.start, self.__ranges))
        max_id: int = max(map(lambda l_range: l_range.stop, self.__ranges))

        nb_fresh_id: int = 0
        nb_id_to_check: int = max_id - min_id
        id_to_check: int = min_id

        while id_to_check < max_id:
            purcent: float = (id_to_check - min_id) / nb_id_to_check
            print(f"{purcent: >7.2%}")
            for l_range in self.__ranges:
                if id_to_check in l_range:
                    nb_fresh_id += l_range.stop - id_to_check
                    id_to_check = l_range.stop
                    break
            else:
                id_to_check = min(
                    l_range.start
                    for l_range in self.__ranges
                    if l_range.start > id_to_check
                )

        return nb_fresh_id


def main() -> None:
    database: Database = Database(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    print(database.get_max_nb_fresh_ids())


if __name__ == "__main__":
    main()
