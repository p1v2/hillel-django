import gspread
import os

CREDENTIALS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "credentials.json"
)

gc = gspread.service_account(filename=CREDENTIALS_PATH)


def read_from_sheet():
    sh = gc.open("Hillel Django")
    worksheet = sh.sheet1

    return worksheet.get_all_values()


def write_to_sheet(data):
    sh = gc.open("Hillel Django")
    worksheet = sh.sheet1

    worksheet.append_rows(data)


if __name__ == "__main__":
    data = read_from_sheet()
    print(data)
