from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import msoffcrypto
import pathlib
import pandas as pd
import numpy as np
from functools import reduce

# Create your views here.
leftTable = pd.DataFrame({'거래일시': [], '거래금액': [], '내용': [], '메모': []})
rightTable = pd.DataFrame({'거래일시': [], '거래금액': [], '내용': [], '메모': []})

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def intro(request):
    context = {}
    if request.method == 'POST' and 'excel' in request.FILES:
        uploaded_file = request.FILES['excel']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context = {
            'url': fs.url(name),
        }

    if request.method == "POST" and 'password' in request.POST:
        pw = request.POST.get('password')
        unlock_main(pw)
        print("password 해제 완료!")
        readExel()
        print(leftTable)
        context['leftTable'] = True

    return render(request, 'HIAC/intro.html', context)


def account_setting(request):
    left_data = leftTable

    left_datalist = left_data.values.tolist()

    context = {
        'left_datalist': left_datalist,
    }

    if request.method == "POST" and 'right_move' in request.POST:
        left_checklist = request.POST.getlist('left_checkbox[]')

        # checklist 받아온 것을 정수로 변환 하여 1씩 뺀 list => 선택된 데이터 의 행을 가져 와서 rightTable 에 넘긴다.
        if left_checklist:
            moveRight(extract_rows(left_data, list(map(lambda x: x-1, list(map(int, left_checklist))))))
            deleteOverlap()

        right_data = rightTable
        right_datalist = right_data.values.tolist()
        context['right_datalist'] = right_datalist

        # statistics 계산
        if right_datalist:
            total = total_statistics(right_datalist)
            context['total_statistics'] = total
        else:
            context['total_statistics'] = [0, 0, 0, 0]

    if request.method == "POST" and 'delete_data' in request.POST:
        right_checklist = request.POST.getlist('right_checkbox[]')

        if right_checklist:
            deleteRow(list(map(lambda x: x - 1, list(map(int, right_checklist)))))
            print(rightTable)

        new_right_data = rightTable
        new_right_datalist = new_right_data.values.tolist()
        context.update({'right_datalist': new_right_datalist})

        if new_right_datalist:
            new_total = total_statistics(new_right_datalist)
            context.update({'total_statistics': new_total})
        else:
            context.update({'total_statistics': [0, 0, 0, 0]})

    return render(request, 'HIAC/account_setting.html', context)


# 통계를 출력 하는 함수
def total_statistics(right_data):
    balance_list = list(map(int, third_column_in_row(np.array(right_data).T[1].tolist())))

    total_number = len(right_data)
    total_deposit = sum_positive(balance_list)
    total_expenditure = sum_negative(balance_list)
    total_difference = total_deposit - total_expenditure

    context = [total_number, total_deposit, total_expenditure, total_difference]

    return context


# 천의 자리 콤마 없애 주는 함수
def third_column_in_row(data):
    valid_list = list()

    for index in range(0, len(data)):
        valid_list.append(data[index].replace(',', ''))

    return valid_list


# 총 입금액 계산
def sum_positive(balance_list):
    deposit = 0
    for i in balance_list:
        if i >= 0:
            deposit += i

    return deposit


# 총 출금액 계산
def sum_negative(balance_list):
    expenditure = 0
    for i in balance_list:
        if i < 0:
            expenditure += i

    return -expenditure


def unlock_main(password):
    url = pathlib.Path(r'./HIAC/xlsx')
    excel_files = list(url.glob('*.xlsx'))
    for i in excel_files:
        unlock(i, password, r'./HIAC/xlsx/xlsx2')


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


def read_table(): # 필요한 테이블 가져 오는 함수
    url = pathlib.Path(r'./HIAC/xlsx/xlsx2')
    excel_files = list(url.glob('*.xlsx'))
    df = pd.read_excel(excel_files[0], header=10, usecols=[1, 3, 6, 7], engine='openpyxl')
    return df


def extract_rows(table, row_list): # 원하는 열(가로줄)의 정보를 가져 오는 함수
    return table.loc[row_list]


def extract_cols(table, col_list): # 원하는 행(새로줄)의 정보를 가져 오는 함수
    return table[col_list]


# 회계 정보 페이지
def readExel():
    global leftTable
    leftTable = read_table()


def moveRight(data):
    global rightTable
    rightTable = rightTable.append(data, ignore_index=True)
    print(rightTable)
    sort_and_reindex()
    print(rightTable)


def deleteOverlap():
    global rightTable
    rightTable = rightTable.drop_duplicates()
    sort_and_reindex()
    print(rightTable)


# 행 삭제 함수
def deleteRow(row_index):
    global rightTable
    rightTable = rightTable.drop(row_index, axis=0)
    sort_and_reindex()


def sort_and_reindex():
    global rightTable
    rightTable = rightTable.sort_values(by='거래일시')
    row_count = len(rightTable.index)
    rightTable.index = list(range(0, row_count))


#unlock_main('981227')

#회계정보페이지 test
row_list = [1, 2, 3, 4]
col_list = ['거래일시']
table = read_table()
#print(extract_rows(table, row_list))
#print(extract_cols(table, col_list))
#print(extract_cols(table, '내용'))
len(extract_cols(table, '내용'))
readExel()
#data={'거래일시':'2022.06.30 23:33:34','거래금액':'-370,500','내용':'어른이대공원(본점)','메모' : np.nan}
#rightTable = leftTable
#moveRight(data)
#deleteOverlap()
#print(leftTable)