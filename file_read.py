"""Чтение CSV-файла и вывод таблиц."""

import csv

def read_headers(reader):
    headers = next(reader, None)
    if not headers:
        raise ValueError("Файл пуст или первая строка не содержит заголовков.")
    headers = [name.strip() for name in headers]
    for name in headers:
        if not name or headers.count(name) > 1:
            raise ValueError("Заголовки должны быть непустыми и уникальными.")
    if "region" not in headers:
        raise ValueError("В файле отсутствует колонка region.")
    return headers


def read_rows(reader, headers):
    rows = []
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
    return rows


def read_data(path):
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, strict=True)
        headers = read_headers(reader)
        rows = read_rows(reader, headers)
    return headers, rows
