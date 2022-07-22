from django.shortcuts import render

import msoffcrypto
import pathlib
import pandas as pd

# Create your views here.
leftTable=list()
rightTable=list()

def intro(request):
    return render(request, 'HIAC/intro.html', {})


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def unlock_main(password):
    url = pathlib.Path(r'./xlsx')
    excel_files = list(url.glob('*.xlsx'))
    for i in excel_files:
        unlock(i, password, r'./xlsx/xlsx2')


def unlock(file_name, passwd, output_folder):
    temp = open(file_name, 'rb')
    excel = msoffcrypto.OfficeFile(temp)
    excel.load_key(passwd)
    out_path = pathlib.Path(output_folder)
    if not out_path.exists():
        out_path.mkdir()

    with open(str(out_path/file_name.name), 'wb') as f:
        excel.decrypt(f)
    temp.close()


def read_table(): # 필요한 테이블 가져오는 함수
    url = pathlib.Path(r'./xlsx/xlsx2')
    excel_files = list(url.glob('*.xlsx'))
    df=pd.read_excel(excel_files[0], header=10, usecols=[1, 3, 4, 6, 7], engine='openpyxl')
    print(df)
    return df


def extract_rows(table, row_list): # 원하는 열(가로줄)의 정보를 가져오는 함수
    return table.loc[row_list]


def extract_cols(table, col_list): # 원하는 행(새로줄)의 정보를 가져오는 함수
    return table[col_list]

#회계 정보 페이지
def readExel():
    global leftTable
    leftTable = read_table()

unlock_main('000814')

#row_list=[1, 2, 3, 4]
#col_list=['거래일시']
table=read_table()
#print(extract_rows(table, row_list))
#print(extract_cols(table, col_list))
print(extract_cols(table, '내용'))
len(extract_cols(table, '내용'))
