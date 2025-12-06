#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Bank:
    def __init__(
        self,
        p_joltage_line: str,
    ):
        self.__joltage_line: str = p_joltage_line

    def find_max_joltage(
        self,
        p_nb_digits_to_use: int = 2,
    ) -> int:
        digits_available: tuple[int, ...] = tuple(map(
            int,
            self.__joltage_line
        ))
        digits_to_use: list[int] = list()
        index_last_digit: int = -1
        for nb_digits_to_keep in range(p_nb_digits_to_use - 1, -1, -1):
            if nb_digits_to_keep == 0:
                index_max: int = len(digits_available)
            else:
                index_max: int = -nb_digits_to_keep
            digits_to_use.append(max(
                digits_available[index_last_digit+1:index_max]
            ))
            index_last_digit: int = digits_available.index(
                digits_to_use[-1],
                index_last_digit+1,
            )

        return int("".join(map(str, digits_to_use)))


def main() -> None:
    banks: tuple[Bank, ...] = tuple(map(
        Bank,
        inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ).split(),
    ))

    max_joltages: tuple[int, ...] = tuple(map(
        lambda bank: bank.find_max_joltage(
            p_nb_digits_to_use=12,
        ),
        banks,
    ))

    if TEST:
        for max_joltage in max_joltages:
            print(max_joltage)

    print(f"SUM: {sum(max_joltages)}")


if __name__ == "__main__":
    main()
