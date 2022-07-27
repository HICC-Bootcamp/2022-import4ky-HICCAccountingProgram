# 2022-import4ky-HICCAccountingProgram

HICC 회계 자동화 프로그램 (HIAC)

-----------

### 1. Introduce

카카오뱅크 거래내역 파일을 업로드하면 거래 일자, 금액, 내용, 메모를 볼 수 있으며 원하는 거래내역을 골라서 엑셀 파일을 다운로드 할 수 있다.

다운로드 받을 때 금전출납부를 업로드하면 금전출납부를 업데이트 시켜줄 수 있다.



51기 HICC 회장 겸 1학기 총무였던 김진호가 금전출납부와 기타 돈 관리를 수동으로 하는 것에 매우 불편함을 느꼈고 2학기 총무에게 이 귀찮음을 물려주고 싶지 않아서 이 프로젝트를 기획하게 되었다.



### 2. Development Environment

+ Win 11 64bit

+ IDE : Pycharm Professional verson

+ Python : 3.10.5



### 3. Import module

| Package          | Version |
| ---------------- | ------- |
| Django           | 4.0.6   |
| asgiref          | 3.5.2   |
| cffi             | 1.15.1  |
| cryptography     | 37.0.4  |
| et-xmlfile       | 1.1.0   |
| msoffcrypto-tool | 5.0.0   |
| numpy            | 1.23.1  |
| olefile          | 0.46    |
| openpyxl         | 3.0.10  |
| pandas           | 1.4.3   |
| pathlib          | 1.0.1   |
| pip              | 21.3.1  |
| pycparser        | 2.21    |
| python-dateutil  | 2.8.2   |
| pytz             | 2022.1  |
| setuptools       | 60.2.0  |
| six              | 1.16.0  |
| sqlparse         | 0.4.2   |
| tzdata           | 2022.1  |
| wheel            | 0.37.1  |



### 4. Collaborator

| FS/기획/팀장                                                                                                                                                 | BE                                                                                                                                                            | 기획                                                                                                                                                   | BE                                                                                                                                                     | FE                                                                                                                                                           |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------- |:---------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------ |:------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 김진호                                                                                                                                                      | 김준호                                                                                                                                                           | 김석준                                                                                                                                                  | 김지은                                                                                                                                                    | 윤찬호                                                                                                                                                          |
| <img src="https://avatars.githubusercontent.com/u/81083461?v=4" width="100px" height="100px"><br/><a href="https://github.com/jinhokim98">jinhokim98</a> | <img src="https://avatars.githubusercontent.com/u/79552567?v=4" width="100px" height="100px"><br><a href="https://github.com/darkenergy814">darkenergy814</a> | <img src="https://avatars.githubusercontent.com/u/108185213?v=4" width="100px" height="100px"><br><a href="https://github.com/SJSK0517">SJSK0517</a> | <img src="https://avatars.githubusercontent.com/u/108122992?v=4" width="100px" height="100px"><br><a href="https://github.com/rlawldms1">rlawldms1</a> | <img src="https://avatars.githubusercontent.com/u/108210104?v=4" width="100px" height="100px"><br><a href="https://github.com/yooooonshine">yooooonshine</a> |