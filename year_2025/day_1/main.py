#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings

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
        p_nb_clicks: int = 1,
    ):
        self.__position = (self.__position + p_nb_clicks) % len(self.numbers)

    def __turn_down(
        self,
        p_nb_clicks: int = 1,
    ):
        self.__position = (self.__position - p_nb_clicks) % len(self.numbers)

    def move(
        self,
        p_rotation: str,
    ) -> int:
        assert len(p_rotation) > 1
        direction: str = p_rotation[0]
        nb_clicks: str = p_rotation[1:]
        assert direction in ("L", "R")
        assert nb_clicks.isdecimal()
        (
            self.__turn_down
            if direction == "L" else
            self.__turn_up
        )(
            p_nb_clicks=int(nb_clicks)
        )
        return self.pointing_number


def main() -> None:
    my_dial: Dial = Dial(
        p_pointing_number=50,
    )
    rotations: list[str] = inputs_file_path.read_text(
        encoding=encodings.utf_8.getregentry().name,
    ).split()

    nb_position_at_0: int = int(my_dial.pointing_number == 0)
    for rotation in rotations:
        my_dial.move(
            p_rotation=rotation,
        )
        nb_position_at_0 += int(my_dial.pointing_number == 0)

    print(nb_position_at_0)


if __name__ == "__main__":
    main()
