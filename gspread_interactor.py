import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import string


class GspreadInteractor(object):

    def __init__(self):

        filename = '/Users/giovannid/Python/MyProject-0b16ad7766d3.json'
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
        self.gs = gspread.authorize(credentials)

    def open_spreadsheet(self, url):

        self.spreadsheet = self.gs.open_by_url(url)
        self.url = url
        self.worksheets = self.spreadsheet.worksheets()
        self.worksheets_names = [i.title for i in self.worksheets]
        self._names2worksheets = {k: self.worksheets[i] for i, k in enumerate(self.worksheets_names)}
        print(self.worksheets_names)

    def add_sheet(self, worksheet_name, rows="1000", cols="50"):
        worksheet = self.spreadsheet.add_worksheet(title=worksheet_name, rows=rows, cols=cols)
        return worksheet

    def _get_worksheet(self, _worksheet):
        if isinstance(_worksheet, str):
            if _worksheet in self.worksheets_names:
                worksheet = self._names2worksheets[_worksheet]
                return worksheet
            else:
                worksheet = self.add_sheet(_worksheet)
                self.worksheets_names += [_worksheet]
                self.worksheets += worksheet
                self._names2worksheets[_worksheet] = worksheet
                print("Worksheet not in spreadsheet - a new worksheet was created")

        elif worksheet not in self.worksheets:
            raise ValueError("Worksheet not in spreadsheet")
        else:
            raise RuntimeError("Worksheet not in spreadsheet")

    def write_df2sheet(self, df, worksheet):
        worksheet = self._get_worksheet(worksheet)
        _df = df.copy()
        _df.reset_index(inplace=True)
        columns = _df.columns
        n_rows = _df.shape[0]
        n_cols = _df.shape[1]
        d = dict({num: alph for num, alph in enumerate(string.ascii_uppercase)})
        col_range = '''A1:{}1'''.format(d[n_cols - 1])
        cells = worksheet.range(col_range)
        for icell, cell in enumerate(cells):
            row = cell.row
            col = cell.col
            cell.value = columns[icell]
        worksheet.update_cells(cells)
        col_range = '''A2:{}{}'''.format(d[n_cols-1], n_rows+1)
        cells = worksheet.range(col_range)
        for icell, cell in enumerate(cells):
            row = cell.row
            col = cell.col
            print row, col
            cell.value = _df.iloc[row-2, col-1]
        worksheet.update_cells(cells)

    def read_sheet2df(self, worksheet):
        worksheet = self._get_worksheet(worksheet)
        values = worksheet.get_all_values()
        if values == []:
            print("Reading empty DataFrame!")
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(values[1:], columns=values[0])
            df.set_index(values[0][0], inplace=True)
        return df
