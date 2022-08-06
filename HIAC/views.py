from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from collections import deque
from datetime import datetime
from .models import AccountData

import msoffcrypto
import pathlib
import pandas as pd
import numpy as np
import json
import os


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
current_username = ''


def signup(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password1'),
                email=request.POST.get('email'),
            )
            auth.login(request, user)
            return redirect('HIAC:login')
        return render(request, 'HIAC/signup.html')
    else:
        form = UserCreationForm
        return render(request, 'HIAC/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('HIAC:intro')
        else:
            context = {
                'error': 'username or password is incorrect.'
            }
            return render(request, 'HIAC/login.html', context)
    else:
        return render(request, 'HIAC/login.html')


def logout(request):
    auth.logout(request)
    return redirect('HIAC:login')


def intro(request):
    context = {}
    user = request.user
    context['user'] = user
    if request.method == 'POST' and 'excel' in request.FILES:
        uploaded_file = request.FILES['excel']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context = {
            'url': fs.url(name),
            'password_error': False
        }

    if request.method == "POST" and 'password_excel' in request.POST:
        pw = request.POST.get('password_excel')
        try:
            unlock_main(pw)
            read_exel()
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
            move_right(extract_rows(left_data, list(map(lambda x: x - 1, list(map(int, left_checklist))))))
            delete_overlap()
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
            delete_row(list(map(lambda x: x - 1, list(map(int, right_checklist)))))
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

    intersection(detail, balance, start_, end_, memo, False)
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

    return JsonResponse({'dlist': search_list}, json_dumps_params={'ensure_ascii': False},
                        content_type="application/json")


def ok_button(request):
    global leftTable, totalStatistics
    json_response = json.loads(request.body)
    modal_checklist_not_num = json_response.get('check_list')

    modal_checklist = list(map(int, modal_checklist_not_num))

    context = {}

    if modal_checklist:
        table_ = extract_rows(leftTable, list(map(int, modal_checklist)))
        move_right(table_)
        delete_overlap()
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


def upload_data(request):
    global rightTable

    if not rightTable.empty:
        # 거래 일시를 db에 넣기 위해 날짜 포맷을 변경 한다.
        date_list = extract_cols(rightTable, '거래일시').values.tolist()
        balance_list = extract_cols(rightTable, '거래금액').values.tolist()

        format_date_list = list()

        # 날짜 포맷
        for date_ in date_list:
            format_date_list.append(date_format_conversion(date_))

        # 금액 포맷
        format_balance_list = third_column_in_row(balance_list)

        rightTable['거래일시'] = format_date_list
        rightTable['거래금액'] = format_balance_list

        for index, row in rightTable.iterrows():
            model = AccountData.objects.create(
                user=request.user.username,
                transaction_date=row['거래일시'],
                transaction_balance=row['거래금액'],
                transaction_detail=row['내용'],
                transaction_memo=row['메모']
            )
            model.save()

        # 중복 제거 작업 (들어갈 때 중복이 없더라도 무조건 다시 넣는다.)
        df = pd.DataFrame(list(AccountData.objects.all().values()))
        df = df.drop_duplicates(subset=["user", "transaction_date"], keep="first")
        AccountData.objects.all().delete()

        for index, row in df.iterrows():
            delete_duplicate_model = AccountData.objects.create(
                id=index,
                user=row['user'],
                transaction_date=row['transaction_date'],
                transaction_balance=row['transaction_balance'],
                transaction_detail=row['transaction_detail'],
                transaction_memo=row['transaction_memo']
            )
            delete_duplicate_model.save()

        context = {
            'result': True
        }

    else:
        context = {
            'result': False
        }

    return render(request, 'HIAC/account_setting.html', context)


def show_data(request):
    global current_username
    database_ = AccountData.objects.filter(user=request.user.username).values()
    current_username = request.user.username

    try:
        user_delete_dataframe = pd.DataFrame(list(database_)).drop(["user", "id"], axis=1)
        dataframe_tolist = user_delete_dataframe.values.tolist()
        total_statistics_ = total_statistics(dataframe_tolist)

        context = {
            'datalist': database_,
            'total_statistics': total_statistics_
        }

    except KeyError:
        context = {
            'datalist': database_,
            'total_statistics': [0, 0, 0, 0]
        }

    # 검색 버튼을 눌렀을 때
    if request.method == "POST":
        date_checkbox = request.POST.get('search_date_feed')
        balance_checkbox = request.POST.get('search_balance_feed')
        detail_checkbox = request.POST.get('search_detail_feed')
        memo_checkbox = request.POST.get('search_memo_feed')
        start_date = request.POST.get('search_start_day')
        end_date = request.POST.get('search_end_day')
        balance = request.POST.get('search_balance_input')
        detail = request.POST.get('search_detail_input')
        memo = request.POST.get('search_memo_input')

        search_requirement = list()

        if date_checkbox:
            search_requirement.append(first_column_in_row(start_date))
            search_requirement.append(first_column_in_row(end_date))
        else:
            search_requirement.append("")
            search_requirement.append("")

        if balance_checkbox:
            balance_ = balance.replace(',', '')
            balance_ = balance_.replace('.', '')
            balance_ = balance_.replace(' ', '')
            search_requirement.append(balance_)
        else:
            search_requirement.append("")

        if detail_checkbox:
            search_requirement.append(detail)
        else:
            search_requirement.append("")

        if memo_checkbox:
            search_requirement.append(memo)
        else:
            search_requirement.append("")

        search_ = AccountData.objects.filter(user=request.user.username).values()

        try:
            search_to_dataframe = pd.DataFrame(list(search_)).drop(["user", "id"], axis=1)

            database_tolist = search_to_dataframe.values.tolist()

            for i in range(0, len(database_tolist)):
                database_tolist[i][0] = datetime_to_str(database_tolist[i][0])
                database_tolist[i][1] = money_to_str(database_tolist[i][1])

            database_time_str = list(zip(*database_tolist))[0]
            database_balance_str = list(zip(*database_tolist))[1]

            search_to_dataframe['transaction_date'] = database_time_str
            search_to_dataframe['transaction_balance'] = database_balance_str

            search_to_dataframe.columns = ['거래일시', '거래금액', '내용', '메모']

            # detail, balance, start_, end_, memo
            intersection(search_requirement[3], search_requirement[2],
                         search_requirement[0], search_requirement[1],
                         search_requirement[4], True, search_to_dataframe)

            search_result = extract_rows(search_to_dataframe, intersection_index)

            search_result_tolist = search_result.values.tolist()

            search_list = []

            for i in range(0, len(search_result_tolist)):
                search_dict = {
                    'transaction_date': search_result_tolist[i][0],
                    'transaction_balance': search_result_tolist[i][1],
                    'transaction_detail': search_result_tolist[i][2],
                    'transaction_memo': search_result_tolist[i][3]
                }

                # 비어 있는 값이면 공백 으로 처리
                if search_result_tolist[i][3] == 'n/a':
                    search_dict.update({'transaction_memo': " "})

                search_list.append(search_dict)

            total_statistics_ = total_statistics(search_result_tolist)

            context.update({'datalist': search_list})
            context.update({'total_statistics': total_statistics_})

        except KeyError:
            context.update({'datalist': search_})
            context.update({'total_statistics': [0, 0, 0, 0]})

        except IndexError:
            non = pd.DataFrame({'transaction_date': [], 'transaction_balance': [],
                                'transaction_detail': [], 'transaction_memo': []})

            context.update({'datalist': non})
            context.update({'total_statistics': [0, 0, 0, 0]})

    return render(request, 'HIAC/show_data.html', context)


def database_download(request):
    database_ = AccountData.objects.filter(user=current_username).values()
    database_to_dataframe = pd.DataFrame(list(database_)).drop(["user", "id"], axis=1)
    database_tolist = database_to_dataframe.values.tolist()

    for i in range(0, len(database_tolist)):
        database_tolist[i][0] = datetime_to_str(database_tolist[i][0])

    database_time_str = list(zip(*database_tolist))[0]

    database_to_dataframe['transaction_date'] = database_time_str

    total_statistics_ = total_statistics(database_tolist)

    statistics_dict = {
        '총 인원': total_statistics_[0],
        '총 입금': total_statistics_[1],
        '총 지출': total_statistics_[2],
        '입금-지출 차액': total_statistics_[3]
    }

    statistics_dataframe = pd.DataFrame(statistics_dict, index=['통계'])

    xlsx_dir = pathlib.Path(r'./HIAC/xlsx/xlsx4/output.xlsx')

    with pd.ExcelWriter(xlsx_dir) as writer:
        database_to_dataframe.to_excel(writer, sheet_name="추출 결과", index=False)
        statistics_dataframe.to_excel(writer, sheet_name="통계", index=False)

    return JsonResponse({"success_": "success"})


# db 창 안에 있는 download modal window 안의 저장 버튼을 눌렀을 때 파일 저장
def db_download(request):
    file_name = request.POST.get('db_file_name')

    src = pathlib.Path(r'./HIAC/xlsx/xlsx4/output.xlsx')
    xlsx_dir = pathlib.Path(r'./HIAC/xlsx/xlsx4')

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


def db_reset(request):
    AccountData.objects.filter(user=current_username).delete()
    return redirect('HIAC:show_data')


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
        if type(data[index]) == str:
            valid_list.append(data[index].replace(',', ''))
        else:
            valid_list.append(data[index])

    return valid_list


def first_column_in_row(data):
    valid_str = data.replace('-', '.')

    return valid_str


def date_format_conversion(date_str):
    date_formatter = "%Y.%m.%d %H:%M:%S"
    return datetime.strptime(date_str, date_formatter)


def datetime_to_str(date_):
    date_formatter = "%Y.%m.%d %H:%M:%S"
    return date_.strftime(date_formatter)


def money_to_str(balance):
    return str(balance)


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
def extract_rows(table_, row_list):
    return table_.loc[row_list]


# 원하는 열(새로줄)의 정보를 가져 오는 함수
def extract_cols(table_, col_list):
    return table_[col_list]


# 회계 정보 페이지
def read_exel():
    global leftTable
    leftTable = read_table()


def move_right(data):
    global rightTable
    rightTable = rightTable.append(data, ignore_index=True)
    sort_and_reindex()


def delete_overlap():
    global rightTable
    rightTable = rightTable.drop_duplicates()
    sort_and_reindex()


# 행 삭제 함수
def delete_row(row_index):
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


def date_select(table_, date_start, date_end, total_index):
    date_list = extract_cols(table_, '거래일시')
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


def money_select(table_, money, total_index):
    money_list = extract_cols(table_, '거래금액')
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


def name_select(table_, name, total_index):
    namelist = extract_cols(table_, '내용')

    if name == '':
        index_name = total_index
    else:
        index_name = [i for i in range(len(namelist)) if name in namelist[i]]
    print(index_name)
    return index_name


def memo_select(table_, memo, total_index):
    memo_list = extract_cols(table_, '메모')
    if memo == '':
        index_memo = total_index
    else:
        index_memo = [i for i in range(len(memo_list)) if memo in memo_list[i]]
    print(index_memo)
    return index_memo


def intersection(name, money, date_start, date_end, memo, is_db, db=None):
    global intersection_index, leftTable
    if not is_db:
        total_index_list = index_maker(len(leftTable))
        date_index = date_select(leftTable, date_start, date_end, total_index_list)
        name_index = name_select(leftTable, name, total_index_list)
        money_index = money_select(leftTable, money, total_index_list)
        memo_index = memo_select(leftTable, memo, total_index_list)
        intersection_index = list(set(name_index) & set(money_index) & set(date_index) & set(memo_index))
        intersection_index.sort()
        print(intersection_index)
    else:
        total_index_list = index_maker(len(db))
        date_index = date_select(db, date_start, date_end, total_index_list)
        name_index = name_select(db, name, total_index_list)
        money_index = money_select(db, money, total_index_list)
        memo_index = memo_select(db, memo, total_index_list)
        intersection_index = list(set(name_index) & set(money_index) & set(date_index) & set(memo_index))
        intersection_index.sort()
        print(intersection_index)


def index_maker(total_index):
    index = []
    for i in range(0, total_index):
        index.append(i)
    return index


table = read_table()
read_exel()
