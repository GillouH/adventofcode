#!/usr/bin/env python
# encoding: utf-8
from __future__ import annotations

import encodings
import itertools
import pathlib
import typing

TEST: bool = False
inputs_file_path: pathlib.Path
if TEST:
    inputs_file_path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path = pathlib.Path("inputs.txt")


class Tile:
    def __init__(
        self,
        p_x: int,
        p_y: int,
    ):
        self.__x: int = p_x
        self.__y: int = p_y

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

    @property
    def id(
        self,
    ) -> tuple[int, int]:
        return self.x, self.y

    def __str__(
        self,
    ) -> str:
        return str({
            "X": self.x,
            "Y": self.y,
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_object: object,
    ) -> bool:
        result: bool
        if isinstance(p_other_object, self.__class__):
            result = self.id == p_other_object.id
        else:
            result = False
        return result

    def __lt__(
        self,
        p_other_tile: Tile,
    ) -> bool:
        if isinstance(p_other_tile, self.__class__):
            result: bool
            if self.x != p_other_tile.x:
                result = self.x < p_other_tile.x
            else:
                result = self.y < p_other_tile.y
        else:
            raise TypeError(
                "unsupported operand type(s) for <: " +
                " and ".join(map(
                    lambda obj: f"'{obj.__class__.__name__}'",
                    (self, p_other_tile),
                ))
            )
        return result

    def __hash__(
        self,
    ) -> int:
        return hash(self.id)


class Rectangle:
    def __init__(
        self,
        p_tiles: typing.Iterable[Tile],
    ):
        tiles: tuple[Tile, ...] = tuple(p_tiles)
        assert len(tiles) == 2
        self.__tiles: tuple[Tile, Tile] = tiles

    @property
    def tiles(
        self,
    ) -> tuple[Tile, Tile]:
        tiles: tuple[Tile, ...] = tuple(sorted(list(self.__tiles)))
        assert len(tiles) == 2
        return tiles

    @property
    def id(
        self,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        tiles_id: tuple[tuple[int, int], ...] = tuple(
            tile.id for tile in self.tiles
        )
        assert len(tiles_id) == 2
        return tiles_id

    @property
    def min_x(
        self,
    ) -> int:
        return min(tile.x for tile in self.tiles)

    @property
    def max_x(
            self,
    ) -> int:
        return max(tile.x for tile in self.tiles)

    @property
    def min_y(
            self,
    ) -> int:
        return min(tile.y for tile in self.tiles)

    @property
    def max_y(
            self,
    ) -> int:
        return max(tile.y for tile in self.tiles)

    @property
    def corner_tiles(
            self,
    ) -> tuple[Tile, Tile, Tile, Tile]:
        corner_tiles: tuple[Tile, ...] = tuple(
            Tile(
                p_x=x,
                p_y=y,
            ) for x, y in itertools.product(
                (self.min_x, self.max_x),
                (self.min_y, self.max_y),
            )
        )
        assert len(corner_tiles) == 4
        return corner_tiles

    @property
    def border_tiles(
        self,
    ) -> typing.Iterator[Tile]:
        line_1: typing.Iterator[Tile] = (
            Tile(
                p_x=x,
                p_y=self.max_y,
            ) for x in range(self.min_x, self.max_x)
        )
        line_2: typing.Iterator[Tile] = (
            Tile(
                p_x=self.max_x,
                p_y=y,
            ) for y in range(self.max_y, self.min_y, -1)
        )
        line_3: typing.Iterator[Tile] = (
            Tile(
                p_x=x,
                p_y=self.min_y,
            ) for x in range(self.max_x, self.min_x, -1)
        )
        line_4: typing.Iterator[Tile] = (
            Tile(
                p_x=self.min_x,
                p_y=y,
            ) for y in range(self.min_y, self.max_y)
        )
        return itertools.chain(
            line_1, line_2, line_3, line_4,
        )

    @property
    def all_tiles(
            self,
    ) -> typing.Iterator[Tile]:
        return (
            Tile(
                p_x=x,
                p_y=y,
            )
            for x in range(self.min_x, self.max_x + 1)
            for y in range(self.min_y, self.max_y + 1)
        )

    @property
    def width(
        self,
    ) -> int:
        return self.max_x - self.min_x + 1

    @property
    def height(
        self,
    ) -> int:
        return self.max_y - self.min_y + 1

    @property
    def perimeter(
        self,
    ) -> int:
        return 2 * (self.width + self.height)

    @property
    def area(
        self,
    ) -> float:
        return self.width * self.height

    def __contains__(
        self,
        p_object: object,
    ) -> bool:
        result: bool
        if isinstance(p_object, Tile):
            result = all((
                self.min_x <= p_object.x <= self.max_x,
                self.min_y <= p_object.y <= self.max_y,
            ))
        else:
            result = False
        return result

    def __str__(
        self,
    ) -> str:
        return str({
            "tiles": self.__tiles,
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_object: object,
    ) -> bool:
        result: bool
        if isinstance(p_other_object, self.__class__):
            result = self.id == p_other_object.id
        else:
            result = False
        return result

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

    rectangles: list[Rectangle] = list(
        Rectangle(
            p_tiles=(tile_1, tile_2),
        ) for tile_1, tile_2 in itertools.combinations(
            iterable=tiles,
            r=2,
        )
    )

    rectangles.sort(
        key=lambda rectangle: rectangle.area,
        reverse=True,
    )

    rectangle_to_keep: Rectangle = rectangles[0]

    print(rectangle_to_keep.area)


if __name__ == "__main__":
    main()
