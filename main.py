import csv

from console_io import ask_number, print_table, show_columns, show_regions, show_statistics
from file_read import read_data
from logic import calculate_statistics, get_numbers, get_regions, select_region


def main():
    default_path = "sample_csv/russian_demography.csv"
    while True:
        path = input(f"Путь к CSV-файлу (Enter — {default_path}): ").strip()
        if not path:
            path = default_path
        try:
            headers, rows = read_data(path)
            break
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            print(f"Не удалось прочитать файл: {error}")

    region_id = headers.index("region")
    regions = get_regions(rows, region_id)
    show_regions(regions)
    region_number = ask_number("Номер региона: ", len(regions))
    region = regions[region_number - 1]
    selected = select_region(rows, region_id, region)

    print("\nДанные выбранного региона:")
    print_table(headers, selected)

    column_ids = []
    columns = []
    for index in range(len(headers)):
        if index != region_id:
            column_ids.append(index)
            columns.append(headers[index])
    if not column_ids:
        print("В файле нет колонок для расчёта статистики.")
        return
    show_columns(columns)

    while True:
        column_number = ask_number("ID числовой колонки: ", len(column_ids))
        column_id = column_ids[column_number - 1]
        try:
            numbers = get_numbers(selected, column_id)
            statistics = calculate_statistics(numbers)
            break
        except ValueError as error:
            print(f"Ошибка выбора или данных: {error}")

    show_statistics(headers[column_id], statistics)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы завершена.")
