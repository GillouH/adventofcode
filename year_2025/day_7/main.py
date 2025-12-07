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

    def get_tachyon_indexes_possibilities(
        self,
        p_line: str,
        p_tachyon_indexes_ponderated_before: list[int],
    ) -> list[int]:
        new_tachyon_indexes_ponderated_before: list[int] = [
            0 for _ in range(len(self.__lines[0]))
        ]
        for index, index_ponderated in enumerate(
            p_tachyon_indexes_ponderated_before
        ):
            if p_line[index] == ".":
                new_tachyon_indexes_ponderated_before[index] += index_ponderated
            elif p_line[index] == "^":
                new_tachyon_indexes_ponderated_before[index - 1] += \
                    index_ponderated
                new_tachyon_indexes_ponderated_before[index + 1] += \
                    index_ponderated
            else:
                raise Exception(p_line[index])

        return new_tachyon_indexes_ponderated_before

    def get_nb_timeline(
        self,
    ) -> int:
        tachyon_indexes_ponderated: list[int] = [
            0 for _ in range(len(self.__lines[0]))
        ]
        tachyon_indexes_ponderated[self.__lines[0].find("S")] = 1
        for line in self.__lines[1:]:
            tachyon_indexes_ponderated = self.get_tachyon_indexes_possibilities(
                p_line=line,
                p_tachyon_indexes_ponderated_before=tachyon_indexes_ponderated,
            )
        return sum(tachyon_indexes_ponderated)


def main() -> None:
    diagram: Diagram = Diagram(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )
    print(diagram.get_nb_timeline())


if __name__ == "__main__":
    main()
