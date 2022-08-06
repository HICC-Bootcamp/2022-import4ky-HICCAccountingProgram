from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage

import msoffcrypto
import pathlib
import pandas as pd
import numpy as np
import json
import os
from collections import deque

# Create your views here.
leftTable = pd.DataFrame({'거래일시': [], '거래금액': [], '내용': [], '메모': []})
rightTable = pd.DataFrame({'거래일시': [], '거래금액': [], '내용': [], '메모': []})
totalStatistics = [0, 0, 0, 0]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 왼쪽 에서 부터 데이터 가 쌓이며 10개를 넘어갈 시 가장 오래된 데이터(맨 오른쪽)는 삭제 된다.
dataset_queue = deque()
dataset_queue.appendleft(rightTable)
queue_index = 0

intersection_index = list()


def intro(request):
    context = {}
    if request.method == 'POST' and 'excel' in request.FILES:
        uploaded_file = request.FILES['excel']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context = {
            'url': fs.url(name),
            'password_error': False
        }

    if request.method == "POST" and 'password' in request.POST:
        pw = request.POST.get('password')
        try:
            unlock_main(pw)
            readExel()
            context['leftTable'] = True
            context.update({'password_error': False})

        except msoffcrypto.exceptions.InvalidKeyError:
            context.update({'password_error': True})

    return render(request, 'HIAC/intro.html', context)


def account_setting(request):
    global dataset_queue, queue_index, leftTable, rightTable, totalStatistics

    leftTable = leftTable.fillna("n/a")
    rightTable = rightTable.fillna("n/a")

    left_data = leftTable
    right_data = rightTable
    total_statistics_ = totalStatistics

    left_datalist = left_data.values.tolist()
    right_datalist = right_data.values.tolist()

    context = {
        'left_datalist': left_datalist,
        'right_datalist': right_datalist,
        'total_statistics': total_statistics_
    }

    # 옮기기 버튼을 눌렀을 때
    if request.method == "POST" and 'right_move' in request.POST:
        left_checklist = request.POST.getlist('left_checkbox[]')

        # checklist 받아온 것을 정수로 변환 하여 1씩 뺀 list => 선택된 데이터 의 행을 가져 와서 rightTable 에 넘긴다.
        if left_checklist:
            moveRight(extract_rows(left_data, list(map(lambda x: x-1, list(map(int, left_checklist))))))
            deleteOverlap()
            push_deque(rightTable)

        right_data = rightTable
        right_datalist = right_data.values.tolist()
        context['right_datalist'] = right_datalist

        # statistics 계산
        if right_datalist:
            total = total_statistics(right_datalist)
            totalStatistics = total
            context.update({'total_statistics': total})
        else:
            context.update({'total_statistics': [0, 0, 0, 0]})

    # 삭제 하기 버튼을 눌렀을 때
    if request.method == "POST" and 'delete_data' in request.POST:
        right_checklist = request.POST.getlist('right_checkbox[]')

        if right_checklist:
            deleteRow(list(map(lambda x: x - 1, list(map(int, right_checklist)))))
            push_deque(rightTable)

        new_right_data = rightTable
        new_right_datalist = new_right_data.values.tolist()
        context.update({'right_datalist': new_right_datalist})

        if new_right_datalist:
            new_total = total_statistics(new_right_datalist)
            totalStatistics = new_total
            context.update({'total_statistics': new_total})
        else:
            context.update({'total_statistics': [0, 0, 0, 0]})

    # 뒤로 가기 버튼을 눌렀을 때
    if request.method == "POST" and 'undo_data' in request.POST:
        if undo_data():
            print(queue_index)
            right_datalist = dataset_queue[queue_index].values.tolist()
            context.update({'right_datalist': right_datalist})

            if right_datalist:
                total = total_statistics(right_datalist)
                totalStatistics = total
                context.update({'total_statistics': total})
            else:
                context.update({'total_statistics': [0, 0, 0, 0]})

        rightTable = dataset_queue[queue_index]

    # 앞으로 가기 버튼을 눌렀을 때
    if request.method == "POST" and 'redo_data' in request.POST:
        if redo_data():
            right_datalist = dataset_queue[queue_index].values.tolist()
            context.update({'right_datalist': right_datalist})

            if right_datalist:
                total = total_statistics(right_datalist)
                totalStatistics = total
                context.update({'total_statistics': total})
            else:
                context.update({'total_statistics': [0, 0, 0, 0]})

        rightTable = dataset_queue[queue_index]

    return render(request, 'HIAC/account_setting.html', context)


def search_data(request):
    json_object = json.loads(request.body)

    start = json_object.get('date_start')
    end = json_object.get('date_end')
    detail = json_object.get('detail')
    balance = json_object.get('balance')
    memo = json_object.get('memo')

    start_ = first_column_in_row(start)
    end_ = first_column_in_row(end)

    print(start_)
    print(end_)
    print(detail)
    print(balance)
    print(memo)

    intersection(detail, balance, start_, end_, memo)
    search_dataframe = extract_rows(leftTable, intersection_index)

    solve_nan_search_dataframe = search_dataframe.fillna('n/a')
    # nan 처리를 해줘야 JSON parse 를 사용할 수 있다.

    search_dataframe_to_list = solve_nan_search_dataframe.values.tolist()

    search_list = []

    for i in range(0, len(search_dataframe_to_list)):
        search_dict = {
            'search_index': intersection_index[i],
            'transaction_time': search_dataframe_to_list[i][0],
            'transaction_balance': search_dataframe_to_list[i][1],
            'transaction_detail': search_dataframe_to_list[i][2],
            'transaction_memo': search_dataframe_to_list[i][3]
        }

        # 비어 있는 값이면 공백 으로 처리
        if search_dataframe_to_list[i][3] == 'n/a':
            search_dict.update({'transaction_memo': " "})

        search_list.append(search_dict)

    return JsonResponse({'dlist': search_list}, json_dumps_params={'ensure_ascii': False}, content_type="application/json")


def ok_button(request):
    global leftTable, totalStatistics
    json_response = json.loads(request.body)
    modal_checklist_not_num = json_response.get('check_list')

    modal_checklist = list(map(int, modal_checklist_not_num))
    print(modal_checklist)

    context = {}

    if modal_checklist:
        table_ = extract_rows(leftTable, list(map(int, modal_checklist)))
        print(table_)
        moveRight(table_)
        deleteOverlap()
        print(rightTable)
        push_deque(rightTable)

    right_data = rightTable
    right_datalist = right_data.values.tolist()
    context['right_datalist'] = right_datalist

    # statistics 계산
    if right_datalist:
        total = total_statistics(right_datalist)
        totalStatistics = total
        context['total_statistics'] = total
    else:
        context['total_statistics'] = [0, 0, 0, 0]

    return render(request, 'HIAC/account_setting.html', context)


def download_button(request):
    global totalStatistics, rightTable

    statistics_dict = {
        '총 인원': totalStatistics[0],
        '총 입금': totalStatistics[1],
        '총 지출': totalStatistics[2],
        '입금-지출 차액': totalStatistics[3]
    }

    print(statistics_dict)

    statistics_dataframe = pd.DataFrame(statistics_dict, index=['통계'])

    xlsx_dir = pathlib.Path(r'./HIAC/xlsx/xlsx3/output.xlsx')

    with pd.ExcelWriter(xlsx_dir) as writer:
        rightTable.to_excel(writer, sheet_name="추출 결과", index=False)
        statistics_dataframe.to_excel(writer, sheet_name="통계", index=False)

    return JsonResponse({"success_": "success"})


# download modal window 안의 저장 버튼을 눌렀을 때 파일 저장
def download(request):
    file_name = request.POST.get('file_name')

    src = pathlib.Path(r'./HIAC/xlsx/xlsx3/output.xlsx')
    xlsx_dir = pathlib.Path(r'./HIAC/xlsx/xlsx3')

    if file_name != "":
        file_name_change = file_name + '.xlsx'
        dst = os.path.join(xlsx_dir, file_name_change)
        os.rename(src, dst)

        fs = FileSystemStorage(xlsx_dir)
        response = FileResponse(fs.open(file_name_change, 'rb'), content_type='application/vnd.ms-excel')

        return response

    else:
        file_name_change = 'HIAC.xlsx'
        dst = os.path.join(xlsx_dir, file_name_change)
        os.rename(src, dst)

        fs = FileSystemStorage(xlsx_dir)
        response = FileResponse(fs.open(file_name_change, 'rb'), content_type='application/vnd.ms-excel')

        return response


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


def first_column_in_row(data):
    valid_str = data.replace('-', '.')

    return valid_str


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


# 필요한 테이블 가져 오는 함수
def read_table():
    url = pathlib.Path(r'./HIAC/xlsx/xlsx2')
    excel_files = list(url.glob('*.xlsx'))
    df = pd.read_excel(excel_files[0], header=10, usecols=[1, 3, 6, 7], engine='openpyxl')
    return df


# 원하는 행(가로줄)의 정보를 가져 오는 함수
def extract_rows(table, row_list):
    return table.loc[row_list]


# 원하는 열(새로줄)의 정보를 가져 오는 함수
def extract_cols(table, col_list):
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


def push_deque(right_table):
    global dataset_queue, queue_index
    for i in range(0, queue_index):
        dataset_queue.popleft()

    if len(dataset_queue) <= 10:
        dataset_queue.appendleft(right_table)
    else:
        dataset_queue.pop()
        dataset_queue.appendleft(right_table)

    queue_index = 0


def undo_data():
    global queue_index
    if dataset_queue:
        if len(dataset_queue) == queue_index + 1:
            pass
        else:
            queue_index += 1
        return True
    else:
        return False


def redo_data():
    global queue_index
    if dataset_queue:
        if queue_index == 0:
            pass
        else:
            queue_index -= 1

        return True
    else:
        return False


def date_select(date_start, date_end, total_index):
    date_list = extract_cols(leftTable, '거래일시')
    adjust_date_end = date_end + ' 23:59:59'

    index_date = list()
    a = 0
    if date_start == "" and date_end == "":
        index_date = total_index

    elif date_start != '' and date_end == '':
        for i in date_list:
            if date_start <= i:
                index_date.append(a)
            a += 1

    elif date_start == "" and date_end != "":
        for i in date_list:
            if i <= adjust_date_end:
                index_date.append(a)
            a += 1
    else:
        for i in date_list:
            if date_start <= i <= adjust_date_end:
                index_date.append(a)
            a += 1

    print(index_date)
    return index_date


def money_select(money, total_index):
    money_list = extract_cols(leftTable, '거래금액')
    new_money_list = third_column_in_row(money_list)
    if money == '':
        index_money = total_index
    else:
        new_money = money.replace(',', '')
        new_money = new_money.replace('.', '')
        new_money = new_money.replace(' ', '')
        index_money = [i for i in range(len(new_money_list)) if new_money in new_money_list[i]]
    print(index_money)
    return index_money


def name_select(name, total_index):
    namelist = extract_cols(leftTable, '내용')

    if name == '':
        index_name = total_index
    else:
        index_name = [i for i in range(len(namelist)) if name in namelist[i]]
    print(index_name)
    return index_name


def memo_select(memo, total_index):
    memo_list = extract_cols(leftTable, '메모')
    if memo == '':
        index_memo = total_index
    else:
        index_memo = [i for i in range(len(memo_list)) if memo in memo_list[i]]
    print(index_memo)
    return index_memo


def intersection(name, money, date_start, date_end, memo):
    global intersection_index
    total_index_list = index_maker(len(leftTable))
    date_index = date_select(date_start, date_end, total_index_list)
    name_index = name_select(name, total_index_list)
    money_index = money_select(money, total_index_list)
    memo_index = memo_select(memo, total_index_list)
    intersection_index = list(set(name_index) & set(money_index) & set(date_index) & set(memo_index))
    intersection_index.sort()
    print(intersection_index)


def index_maker(total_index):
    index = []
    for i in range(0, total_index):
        index.append(i)
    return index


# unlock_main('981227')

# 회계정보페이지 test
# row_list = [1, 2, 3, 4]
# col_list = ['거래일시']
table = read_table()
# print(extract_rows(table, row_list))
# print(extract_cols(table, col_list))
# print(extract_cols(table, '내용'))
# len(extract_cols(table, '내용'))
readExel()
# data={'거래일시':'2022.06.30 23:33:34','거래금액':'-370,500','내용':'어른이대공원(본점)','메모' : np.nan}
# rightTable = leftTable
# moveRight(data)
# deleteOverlap()
# print(leftTable)
