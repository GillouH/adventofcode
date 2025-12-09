#!/usr/bin/env python
# encoding: utf-8
from __future__ import annotations

import encodings
import itertools
import pathlib

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Tile:
    __ID: int = 0

    def __init__(
        self,
        p_x: int,
        p_y: int,
    ):
        self.__id: int = self.__class__.__ID
        self.__class__.__ID += 1
        self.__x: int = p_x
        self.__y: int = p_y

    @property
    def id(
        self,
    ) -> int:
        return self.__id

    @property
    def x(
        self,
    ) -> int:
        return self.__x

    @property
    def y(
        self,
    ) -> int:
        return self.__y

    def __str__(
        self,
    ) -> str:
        return str({
            "id": self.id,
            "X": self.x,
            "Y": self.y,
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_boxe: object,
    ) -> bool:
        if isinstance(p_other_boxe, Tile):
            return self.id == p_other_boxe.id
        else:
            raise TypeError(
                "unsupported operand type(s) for ==: " +
                " and ".join(map(
                    lambda obj: f"'{obj.__class__.__name__}'",
                    (self, p_other_boxe),
                ))
            )

    def __hash__(
        self,
    ) -> int:
        return hash(self.id)


class Rectangle:
    __ID: int = 0

    def __init__(
        self,
        p_tiles: tuple[Tile, Tile],
    ):
        self.__id: int = self.__class__.__ID
        self.__class__.__ID += 1
        self.__tiles: tuple[Tile, Tile] = p_tiles

    @property
    def id(
        self,
    ) -> int:
        return self.__id

    @property
    def tiles(
        self,
    ) -> tuple[Tile, Tile]:
        return self.__tiles

    @property
    def area(
        self,
    ) -> float:
        return (
            abs(self.__tiles[0].x - self.__tiles[1].x) + 1
        ) * (
            abs(self.__tiles[0].y - self.__tiles[1].y) + 1
        )

    def __str__(
        self,
    ) -> str:
        return str({
            "id": self.id,
            "tiles": self.__tiles,
            "area": self.area,
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_boxe: object,
    ) -> bool:
        if isinstance(p_other_boxe, Tile):
            return self.id == p_other_boxe.id
        else:
            raise TypeError(
                "unsupported operand type(s) for ==: " +
                " and ".join(map(
                    lambda obj: f"'{obj.__class__.__name__}'",
                    (self, p_other_boxe),
                ))
            )

    def __hash__(
        self,
    ) -> int:
        return hash(self.id)


def main() -> None:
    tiles: tuple[Tile, ...] = tuple(
        Tile(
            p_x=int(x),
            p_y=int(y),
        ) for x, y in map(
            lambda line: line.split(","),
            inputs_file_path.read_text(
                encoding=encodings.utf_8.getregentry().name,
            ).splitlines()
        )
    )

    rectangles: tuple[Rectangle, ...] = tuple(
        Rectangle(
            p_tiles=(tile_1, tile_2),
        ) for tile_1, tile_2 in itertools.combinations(
            iterable=tiles,
            r=2,
        )
    )

    print(
        sorted(
            rectangles,
            key=lambda rectangle: rectangle.area,
            reverse=True,
        )[0].area,
    )


if __name__ == "__main__":
    main()
