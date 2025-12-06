#!/usr/bin/env python
# encoding: utf-8

import pathlib
import encodings

inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


def create_range(
    p_range_numbers: str,
) -> range:
    min_number, max_number = map(int, p_range_numbers.split("-"))
    return range(min_number, max_number + 1)


def main() -> None:
    ranges: list[range] = list(map(
        create_range,
        inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ).split(
            sep=","
        )
    ))
    invalid_ids: list[int] = list()

    for current_range in ranges:
        for id in current_range:
            id_str: str = str(id)
            for pattern_size in range(1, int(len(id_str) / 2) + 1):
                if len(id_str) % pattern_size == 0:
                    pattern: str = id_str[:pattern_size]
                    nb_repetition: int = int(len(id_str) / pattern_size)
                    if id_str == pattern * nb_repetition:
                        invalid_ids.append(id)
                        break

    print(sum(invalid_ids))


if __name__ == "__main__":
    main()
