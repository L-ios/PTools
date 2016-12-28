#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlsxwriter

'''
主要是用于查找相同的文件
收集大小，然后获取sha-1 md5.
'''


def write_row():
    pass




def main():
    workbook = xlsxwriter.Workbook('myexcel.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 1, 1)
    workbook.close()


if __name__ == '__main__':
    main()