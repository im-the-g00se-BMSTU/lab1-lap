import csv

from file_read import read_data

from logic import calculate_statistics, get_numbers, get_regions, select_region

def ask_file():
    while True:
        path = input("Путь к CSV-файлу (UTF-8, разделитель — запятая): ").strip()
        try:
            return read_data(path)
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            print(f"Не удалось прочитать файл: {error}")


def ask_number(prompt, count):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue
        if number < 1 or number > count:
            print(f"Введите номер от 1 до {count}.")
            continue
        return number


def ask_region(rows, region_id):
    regions = get_regions(rows, region_id)
    print("\nРегионы:")
    for index in range(len(regions)):
        print(f"{index + 1}: {regions[index]}")

    region_number = ask_number("Номер региона: ", len(regions))
    return select_region(rows, region_id, regions[region_number - 1])


def show_columns(headers, region_id):
    print("\nКолонки:")
    column_ids = []
    for index in range(len(headers)):
        if index != region_id:
            column_ids.append(index)
            print(f"{len(column_ids)}: {headers[index]}")
    return column_ids


def ask_statistics(rows, column_ids):
    while True:
        column_number = ask_number("ID числовой колонки: ", len(column_ids))
        column_id = column_ids[column_number - 1]
        try:
            numbers = get_numbers(rows, column_id)
            return column_id, calculate_statistics(numbers)
        except ValueError as error:
            print(f"Ошибка выбора или данных: {error}")


def show_statistics(column_name, statistics):
    minimum, maximum, median, average, percentiles = statistics
    print(f"\nСтатистика колонки {column_name}:")
    print(f"Максимум: {maximum:.6g}")
    print(f"Минимум: {minimum:.6g}")
    print(f"Медиана: {median:.6g}")
    print(f"Среднее значение: {average:.6g}")
    percentile_rows = []
    for percent, value in percentiles:
        percentile_rows.append([str(percent), f"{value:.6g}"])
    print("\nПерцентили (линейная интерполяция):")
    print_table(["Перцентиль", "Значение"], percentile_rows)

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