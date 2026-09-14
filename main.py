from console_io import ask_file, ask_region, show_columns, ask_statistics, show_statistics, print_table


def main():
    print("Статистика по регионам")

    headers, rows = ask_file()
    region_id = headers.index("region")
    selected = ask_region(rows, region_id)

    print("\nДанные выбранного региона:")
    print_table(headers, selected)

    column_ids = show_columns(headers, region_id)
    if not column_ids:
        print("В файле нет колонок для расчёта статистики.")
        return
    
    column_id, statistics = ask_statistics(selected, column_ids)
    show_statistics(headers[column_id], statistics)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы завершена.")
