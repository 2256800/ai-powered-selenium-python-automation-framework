from openpyxl import load_workbook


def read_login_data(file_path):
    workbook = load_workbook(file_path)
    sheet = workbook["LoginData"]

    login_data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        username, password, expected_result = row

        login_data.append(
            (username, password, expected_result)
        )

    workbook.close()

    return login_data
