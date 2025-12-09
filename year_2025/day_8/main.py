#!/usr/bin/env python
# encoding: utf-8
from __future__ import annotations

import encodings
import itertools
import math
import pathlib
import typing

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Boxe:
    def __init__(
        self,
        p_id: int,
        p_x: int,
        p_y: int,
        p_z: int,
        p_circuit: Circuit | None = None
    ):
        self.__id: int = p_id
        self.__x: int = p_x
        self.__y: int = p_y
        self.__z: int = p_z

        self.__circuit: Circuit
        if p_circuit is None:
            self.__circuit = Circuit(
                p_id=self.id,
                p_boxes=(self,),
            )
        else:
            self.__circuit = p_circuit

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

    @property
    def z(
        self,
    ) -> int:
        return self.__z

    @property
    def circuit(
        self,
    ) -> Circuit:
        return self.__circuit

    @circuit.setter
    def circuit(
        self,
        p_new_circuit: Circuit,
    ):
        self.__circuit = p_new_circuit

    def calculate_distance(
        self,
        p_other_boxe: typing.Self,
    ) -> float:
        return math.sqrt(
            sum((
                pow(self.x - p_other_boxe.x, 2),
                pow(self.y - p_other_boxe.y, 2),
                pow(self.z - p_other_boxe.z, 2),
            ))
        )

    def __str__(
        self,
    ) -> str:
        return str({
            "id": self.id,
            "X": self.x,
            "Y": self.y,
            "Z": self.z,
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_boxe: object,
    ) -> bool:
        if isinstance(p_other_boxe, Boxe):
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


def get_boxes_distances(
    p_boxes: typing.Iterable[Boxe]
) -> dict[tuple[int, int], float]:
    return {
        (boxe1.id, boxe2.id): boxe1.calculate_distance(
            p_other_boxe=boxe2,
        )
        for (boxe1, boxe2) in itertools.combinations(
            iterable=p_boxes,
            r=2,
        )
    }


class Circuit:
    def __init__(
        self,
        p_id: int,
        p_boxes: typing.Iterable[Boxe],
    ):
        self.__id: int = p_id
        self.__boxes: set[Boxe] = set(p_boxes)

    @property
    def id(
        self,
    ) -> int:
        return self.__id

    @property
    def boxes(
        self,
    ) -> set[Boxe]:
        return self.__boxes.copy()

    def add_boxe(
        self,
        p_boxe: Boxe,
    ):
        assert (p_boxe in self.__boxes) == (self == p_boxe.circuit)

        if p_boxe not in self.__boxes:
            for boxe in p_boxe.circuit.boxes:
                boxe.circuit = self
                self.__boxes.add(boxe)

    def __str__(
        self,
    ) -> str:
        return str({
            "id": self.id,
            "boxes": tuple(map(
                lambda boxe: boxe.id,
                self.boxes,
            )),
        })

    def __repr__(
        self,
    ) -> str:
        return str(self)

    def __eq__(
        self,
        p_other_circuit: object,
    ) -> bool:
        if isinstance(p_other_circuit, Circuit):
            return self.id == p_other_circuit.id
        else:
            raise TypeError(
                "unsupported operand type(s) for ==: " +
                " and ".join(map(
                    lambda obj: f"'{obj.__class__.__name__}'",
                    (self, p_other_circuit),
                ))
            )

    def __hash__(
        self,
    ) -> int:
        return hash(self.id)

    def __len__(
        self,
    ) -> int:
        return len(self.__boxes)


def main() -> None:
    nb_connections_to_make: int
    if TEST:
        nb_connections_to_make = 10
    else:
        nb_connections_to_make = 1_000
    nb_circuit_size_to_multiply: int = 3
    boxes: tuple[Boxe, ...] = tuple(
        Boxe(
            p_id=l_id,
            p_x=int(x),
            p_y=int(y),
            p_z=int(z),
        ) for l_id, (x, y, z) in enumerate(
            map(
                lambda line: line.split(","),
                inputs_file_path.read_text(
                    encoding=encodings.utf_8.getregentry().name,
                ).splitlines()
            )
        )
    )

    boxes_distances_sorted: list[tuple[tuple[int, int], float]] = sorted(
        list(get_boxes_distances(
            p_boxes=boxes,
        ).items()),
        key=lambda key_value: key_value[1],
    )
    for index in range(nb_connections_to_make):
        id_boxe1, id_boxe2 = boxes_distances_sorted[index][0]
        boxe1, boxe2 = map(
            lambda id_boxe: next(filter(
                lambda boxe: boxe.id == id_boxe,
                boxes,
            )),
            (id_boxe1, id_boxe2),
        )
        boxe1.circuit.add_boxe(
            p_boxe=boxe2,
        )

    circuits: list[Circuit] = sorted(
        list(set(map(
            lambda boxe: boxe.circuit,
            boxes,
        ))),
        key=lambda circuit: len(circuit.boxes),
        reverse=True,
    )
    product: int = 1
    for circuit in circuits[:nb_circuit_size_to_multiply]:
        product *= len(circuit)

    print(product)


if __name__ == "__main__":
    main()
