#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings
import typing

inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Dial:
    def __init__(
        self,
        p_number_max: int = 100,
        p_pointing_number: int = 0,
    ):
        self.numbers: tuple[int, ...] = tuple(range(p_number_max))
        self.__position: int = self.numbers.index(p_pointing_number)

    @property
    def pointing_number(
        self,
    ) -> int:
        return self.numbers[self.__position]

    def __turn_up(
        self,
    ):
        self.__position = (self.__position + 1) % len(self.numbers)

    def __turn_down(
        self,
    ):
        self.__position = (self.__position - 1) % len(self.numbers)

    def move(
        self,
        p_rotation: str,
    ) -> typing.Generator[int, None, None]:
        assert len(p_rotation) > 1
        direction: str = p_rotation[0]
        nb_clicks: str = p_rotation[1:]
        assert direction in ("L", "R")
        assert nb_clicks.isdecimal()
        method_to_turn = (
            self.__turn_down
            if direction == "L" else
            self.__turn_up
        )

        for _ in range(int(nb_clicks)):
            method_to_turn()
            yield self.pointing_number


def main() -> None:
    my_dial: Dial = Dial(
        p_pointing_number=50,
    )
    rotations: list[str] = inputs_file_path.read_text(
        encoding=encodings.utf_8.getregentry().name,
    ).split()

    nb_position_at_0: int = int(my_dial.pointing_number == 0)
    for rotation in rotations:
        pointing_number: tuple[int, ...] = tuple(my_dial.move(
            p_rotation=rotation,
        ))
        nb_position_at_0 += pointing_number.count(0)

    print(nb_position_at_0)


if __name__ == "__main__":
    main()
