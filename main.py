#!/usr/bin/env python3
import csv
import sys

CSV_TABLE_STDIN = 'stdin.csv'  # 原始数据文件
CSV_TABLE_RESULT = 'result.csv'  # 转换格式后的数据文件

# 列表头和明细行的列数不一致，请检查。
INDEX_ERROR_MESSAGE = 'The number of columns in the header is inconsistent with the number of columns in the detail, please check it.'

"""
最下方包含测试用数据
"""


# 1. Read a CSV table from stdin.
def read_data_from_stdin():
    in_data_list = []
    out_data_list = []
    header = []
    i = 0
    col_length = 0

    # 接收输入的批量数据
    while True:
        row = str.strip(sys.stdin.readline())
        if row == "":
            break
        # 保存原始数据列表头的数目
        if i == 0:
            col_length = row.count(',') + 1
        i += 1
        columns = row.split(',')

        in_data_list.append(columns)

    # 第一行数据作为列表头放入header, 其余明细行数据放入out_data_list
    try:
        for row_num, row in enumerate(in_data_list):
            if row_num == 0:
                for col_id in range(col_length):
                    header.append(row[col_id])
            else:
                columns = {}
                for col_id in range(col_length):
                    columns[header[col_id]] = row[col_id]

                if len(header) != len(row):
                    # 列表头和明细行的列数不一致，请检查。
                    print(INDEX_ERROR_MESSAGE)
                    return [], {}

                out_data_list.append(columns)
    except IndexError as e:
        # 列表头和明细行的列数不一致，请检查。
        print(INDEX_ERROR_MESSAGE, e)
        return [], {}

    # 返回值
    return header, out_data_list


# save header and data_list to the csv_file
def write_data_to_csv_file(header, data_list, file):
    with open(file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data_list)


# 2. Reshape the table by collapsing several columns into two.
def reshape_data(source_file, dest_file):
    data_list = []
    with open(source_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        col_length = len(reader.fieldnames)
        for row in reader:
            for col in range(1, col_length):
                data_list.append({"country": row[reader.fieldnames[0]], "year": reader.fieldnames[col],
                                  "cases": row[reader.fieldnames[col]]})
        data_list.sort(key=lambda year: year['year'])
    # 3. Write the reshaped data to stdout.
    with open(dest_file, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=('country', 'year', 'cases'))
        writer.writeheader()
        writer.writerows(data_list)

    # 输出显示最终结果
    output_result(dest_file)


# output the final result.
def output_result(dest_file):
    with open(dest_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(f'{row[0]},{row[1]},{row[2]}')


if __name__ == '__main__':
    # 接收批量输入的原始数据
    headers, data = read_data_from_stdin()
    # 将原始数据存入 CSV_TABLE_INPUT文件
    write_data_to_csv_file(headers, data, CSV_TABLE_STDIN)
    # 只读 CSV_TABLE_INPUT文件的数据转换格式后另存为 CSV_TABLE_RESULT文件并输出结果.
    reshape_data(CSV_TABLE_STDIN, CSV_TABLE_RESULT)

"""
场景1
测试数据:
country,1999,2000
A,0.7K,2K
B,37K,80K
C,212K,213K

期待结果:有正确输出
"""

"""
场景2
测试数据:
country,1999,2000,2001,2002,2003
A,0.7K,2K,3K,4K,5K
B,37K,80K,90K,100K,110K
C,212K,213K,214K,215K,216K
D,1K,2K,3K,4K,5K

期待结果:有正确输出
"""

"""
场景3
测试数据:空数据

期待结果:正常输出列表头country,year,cases
"""

"""
场景4
测试数据:只有列表头
country,1999,2000

期待结果:正常输出列表头country,year,cases
"""

"""
场景5
测试数据:乱输入
fdg测jk,uプio,ip试of,xcキk,fdg
moにkf,gjあi,miすo,a🐰sp,Привет.[
skdl,asdif,l;'k,&l%$,{*(&$23

期待结果:有正确输出
"""

"""
场景6
测试数据:列表头少一列
country,1999
A,0.7K,2K
B,37K,80K
C,212K,213K

期待结果:列表头和明细行的列数不一致，请检查。
"""

"""
场景7
测试数据:某明细行少一列
country,1999,2000
A,0.7K
B,37K,80K
C,212K,213K

期待结果:列表头和明细行的列数不一致，请检查。
"""
