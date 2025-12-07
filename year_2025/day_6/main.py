#!/usr/bin/env python
# encoding: utf-8

import encodings
import pathlib
import typing

TEST: bool = False
if TEST:
    inputs_file_path: pathlib.Path = pathlib.Path("test_inputs.txt")
else:
    inputs_file_path: pathlib.Path = pathlib.Path("inputs.txt")


class Worksheet:
    def __init__(
        self,
        p_data: str,
    ):
        lines: list[str] = p_data.splitlines()
        last_line: str = lines.pop()
        self.__columns_data: list[tuple[str, int, list[str]]] = list()
        column_size: int = 1
        actual_ope: str = last_line[0]
        for elem in last_line[1:]:
            if elem == " ":
                column_size += 1
            elif elem in ("*", "+"):
                column_size -= 1
                self.__columns_data.append((actual_ope, column_size, list()))
                actual_ope = elem
                column_size = 1
            else:
                raise Exception(f"{elem=}")
        else:
            self.__columns_data.append((actual_ope, column_size, list()))

        for line in lines:
            index: int = 0
            for _, column_size, column_numbers in self.__columns_data:
                column_numbers.append(
                    line[index:index + column_size]
                )
                index += column_size + 1

    def get_column_numbers(
        self,
        p_index: int,
    ) -> typing.Generator[int, None, None]:
        column_size, numbers = self.__columns_data[p_index][1:]
        for index_in_column in range(column_size-1, -1, -1):
            v_number: str = "".join(
                h_number[index_in_column]
                for h_number in numbers
            )
            yield int(v_number)

    def process_column(
        self,
        p_index: int,
    ) -> int:
        if self.__columns_data[p_index][0] == "+":
            result: int = sum(self.get_column_numbers(
                p_index=p_index,
            ))
        else:
            result: int = 1
            for elem in self.get_column_numbers(
                p_index=p_index,
            ):
                result *= elem
        return result

    def process_all_columns(
        self,
    ) -> typing.Generator[int, None, None]:
        return (self.process_column(
            p_index=index,
        ) for index in range(len(self.__columns_data)))

    def solve_problem(
        self,
    ) -> int:
        return sum(self.process_all_columns())


def main() -> None:
    worksheet: Worksheet = Worksheet(
        p_data=inputs_file_path.read_text(
            encoding=encodings.utf_8.getregentry().name,
        ),
    )

    if TEST:
        for i in range(4):
            print(f"Nombre dans la colonne {i}")
            print(list(worksheet.get_column_numbers(
                p_index=i,
            )))
            print(f"Résultat de l'opération de la colonne {i}")
            print(worksheet.process_column(
                p_index=i,
            ))
            print()
        print("Résultat de l'ensemble des colonnes")
        print(tuple(worksheet.process_all_columns()))

        print("Somme des résultats")
        print(worksheet.solve_problem())
    else:
        print(worksheet.solve_problem())


if __name__ == "__main__":
    main()
