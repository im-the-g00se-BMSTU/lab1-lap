"""Консольный интерфейс. Запуск: python3 main.py."""

import csv

from file_io import read_data
from logic import calculate_statistics, get_numbers, get_regions, select_region


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


def main():
    print("Статистика по регионам")
    while True:
        path = input("Путь к CSV-файлу (UTF-8, разделитель — запятая): ").strip()
        try:
            headers, rows = read_data(path)
            break
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            print(f"Не удалось прочитать файл: {error}")

    region_id = headers.index("region")
    regions = get_regions(rows, region_id)
    print("\nРегионы:")
    for index in range(len(regions)):
        print(f"{index + 1}: {regions[index]}")

    while True:
        try:
            region_number = int(input("Номер региона: "))
        except ValueError:
            print("Номер региона должен быть целым числом.")
            continue
        if region_number < 1 or region_number > len(regions):
            print(f"Введите номер от 1 до {len(regions)}.")
            continue
        selected = select_region(rows, region_id, regions[region_number - 1])
        break

    print("\nДанные выбранного региона:")
    print_table(headers, selected)
    print("\nКолонки:")
    for index in range(len(headers)):
        print(f"{index + 1}: {headers[index]}")

    while True:
        try:
            column_id = int(input("ID числовой колонки: ")) - 1
        except ValueError:
            print("ID колонки должен быть целым числом.")
            continue
        try:
            if column_id < 0 or column_id >= len(headers):
                print(f"Введите целый ID от 1 до {len(headers)}.")
                continue
            if headers[column_id] == "region":
                print("Выберите числовую колонку, а не название региона.")
                continue
            numbers = get_numbers(selected, column_id)
            minimum, maximum, median, average, percentiles = calculate_statistics(
                numbers
            )
            break
        except ValueError as error:
            print(f"Ошибка выбора или данных: {error}")

    print(f"\nСтатистика колонки {headers[column_id]}:")
    print(f"Максимум: {maximum:.6g}")
    print(f"Минимум: {minimum:.6g}")
    print(f"Медиана: {median:.6g}")
    print(f"Среднее значение: {average:.6g}")
    percentile_rows = []
    for percent, value in percentiles:
        percentile_rows.append([str(percent), f"{value:.6g}"])
    print("\nПерцентили (линейная интерполяция):")
    print_table(["Перцентиль", "Значение"], percentile_rows)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы завершена.")
