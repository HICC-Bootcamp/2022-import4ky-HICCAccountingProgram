# str = ['기러기', '윤찬호', '별똥별', '역삼역', '윤찬호', '우영우', '인도인', 스위스']
# target = '윤찬호'
# index = -1
# while True:
#     index = str.find(target, index + 1)
#     if index == -1:
#         break
#     print('start=%d' % index)
total_index = 40
namelist = ['기러기', '윤찬호', '별똥별', '역삼역', '오윤찬호오', '우영우', '인도인', '스위스']
datelist = ['22.01.01', '22.05.05', '24.02.05', '21.12.21', '14.05.14', '18.11.25']
moneylist = ['15,000', '15,154', '11,115', '15', '11,150', '11,450', '8,400', '4,000']
name = '윤찬호'
date = ''
money = '15'
intersection_index = ''
def name_select(name) :

    if name == '' :
        index_name = total_index_list
    else:
        index_name = [i for i in range(len(namelist)) if name in namelist[i]]
    print(index_name)
    return index_name


def date_select(date):

    if date == '':
        index_date = total_index_list

    else:
        index_date = [i for i in range(len(datelist)) if date in datelist[i]]
    print(index_date)
    return index_date


def money_select(money):
    if money == '' :
        index_money = total_index_list
    else :
        index_money = [i for i in range(len(moneylist)) if money in moneylist[i]]
    print(index_money)
    return index_money

def intersection(name, money, date):
    global intersection_index
    name_index = name_select(name)
    money_index = money_select(money)
    date_index = date_select(date)
    intersection_index = list(set(name_index)&set(money_index)&set(date_index))
    print(intersection_index)

def indexmaker(total_index):
    index = []
    for i in range(0,total_index):
        index.append(i)
    return index

total_index_list= indexmaker(total_index)
print(total_index_list)
intersection(name, money, date)