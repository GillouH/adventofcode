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
            if len(id_str) % 2 == 0:
                first_part: str = id_str[:int(len(id_str) / 2)]
                second_part: str = id_str[int(len(id_str) / 2):]
                if first_part == second_part:
                    invalid_ids.append(id)

    print(sum(invalid_ids))


if __name__ == "__main__":
    main()
