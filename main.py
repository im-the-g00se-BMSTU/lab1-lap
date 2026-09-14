"""Консольный интерфейс. Запуск: python3 main.py."""

import csv

from file_io import read_data, print_table
from logic import calculate_statistics, get_numbers, get_regions, select_region


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
    column_ids = []
    for index in range(len(headers)):
        if index != region_id:
            column_ids.append(index)
            print(f"{len(column_ids)}: {headers[index]}")

    if not column_ids:
        print("В файле нет колонок для расчёта статистики.")
        return

    while True:
        try:
            column_number = int(input("ID числовой колонки: "))
        except ValueError:
            print("ID колонки должен быть целым числом.")
            continue
        try:
            if column_number < 1 or column_number > len(column_ids):
                print(f"Введите целый ID от 1 до {len(column_ids)}.")
                continue
            column_id = column_ids[column_number - 1]
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
