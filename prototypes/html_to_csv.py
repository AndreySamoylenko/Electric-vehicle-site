import csv
import html
import sys
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.current_row = []
        elif tag == "td":
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag == "td" and self.in_cell:
            self.current_row.append(self.current_cell)
            self.in_cell = False
        elif tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

def html_to_csv(html_text, csv_path):
    parser = TableParser()
    parser.feed(html_text)

    if not parser.rows:
        print("Таблица не найдена в введённых данных.")
        return

    with open(csv_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in parser.rows:
            # Раскодируем HTML-сущности обратно в нормальный текст
            writer.writerow([html.unescape(cell) for cell in row])

    print(f"Готово: {csv_path} (строк: {len(parser.rows)})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python html_to_csv.py output.csv")
        sys.exit(1)

    print("--- ВСТАВЬТЕ HTML-ТАБЛИЦУ В КОНСОЛЬ ---")
    print("Когда закончите:")
    print("Ctrl+Z, затем Enter")


    try:
        html_text = sys.stdin.read()
        html_to_csv(html_text, sys.argv[1])
    except KeyboardInterrupt:
        print("\nПрервано.")
    except Exception as e:
        print(f"Ошибка: {e}")