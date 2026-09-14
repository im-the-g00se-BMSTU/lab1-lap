"""Чтение и проверка структуры CSV-файла."""

import csv

def print_table(headers, rows):
    widths = []
    for column in range(len(headers)):
        width = len(headers[column])
        for row in rows:
            width = max(width, len(str(row[column])))
        widths.append(width)

    separator = "+"
    for width in widths:
        separator += "-" * (width + 2) + "+"
    print(separator)
    for row in [headers] + rows:
        line = "|"
        for column in range(len(headers)):
            line += " " + str(row[column]).ljust(widths[column]) + " |"
        print(line)
        if row is headers:
            print(separator)
    print(separator)

def read_data(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, strict=True)
        headers = next(reader, None)
        if not headers:
            raise ValueError("Файл пуст или первая строка не содержит заголовков.")

        headers = [name.strip() for name in headers]
        for name in headers:
            if not name or headers.count(name) > 1:
                raise ValueError("Заголовки должны быть непустыми и уникальными.")
        if "region" not in headers:
            raise ValueError("В файле отсутствует колонка region.")

        region_id = headers.index("region")
        for row in reader:
            if not row:
                continue
            if len(row) != len(headers):
                raise ValueError(
                    f"Строка {reader.line_num}: неверное количество колонок."
                )
            row = [cell.strip() for cell in row]
            if not row[region_id]:
                raise ValueError(f"Строка {reader.line_num}: не указан регион.")
            rows.append(row)

    if not rows:
        raise ValueError("В файле нет строк с данными.")
    return headers, rows
