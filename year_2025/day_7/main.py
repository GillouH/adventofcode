#!/usr/bin/env python
# encoding: utf-8

import encodings
import pathlib

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Diagram:
    def __init__(
        self,
        p_data: str,
    ):
        self.__lines: list[str] = p_data.splitlines()

    def get_nb_split(
        self,
    ) -> int:
        nb_split: int = 0
        tachyon_indexes: list[int] = [self.__lines[0].index("S")]
        for line in self.__lines[1:]:
            new_tachyon_indexes: list[int] = list()
            for tachyon_index in tachyon_indexes:
                if line[tachyon_index] == "^":
                    new_tachyon_indexes.extend(
                        (tachyon_index - 1, tachyon_index + 1)
                    )
                    nb_split += 1
                elif line[tachyon_index] == ".":
                    new_tachyon_indexes.append(tachyon_index)
                else:
                    raise Exception(line[tachyon_index])
            tachyon_indexes = list(set(new_tachyon_indexes))

        return nb_split


def main() -> None:
    diagram: Diagram = Diagram(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    print(diagram.get_nb_split())


if __name__ == "__main__":
    main()
