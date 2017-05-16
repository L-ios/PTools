#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import hashlib

try:
    import xlsxwriter
except ImportError:
    print('"sudo apt install xlsxwrite" or "sudo -H pip install xlsxwrite"]')
    exit(1)

'''
主要是用于查找相同的文件
收集大小，然后获取sha-1 md5.
'''


def write_row(worksheet, row, *arg):
    col = 0
    for item in arg:
        worksheet.write(row, col, item)
        col += 1


def main():
    workbook = xlsxwriter.Workbook('myexcel.xlsx')
    worksheet = workbook.add_worksheet('collection')

    row = 0
    for rootdir, _, files in os.walk(local_path):
        for file in files:
            write_row(worksheet, row, file, os.path.abspath(file), os.path.getsize(file), os.path.getatime(file), calc_md5(file), calc_sha1(file))
            row += 1


def calc_sha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        #print(hash)
        return hash


def calc_md5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        #print(hash)
        return hash


if __name__ == '__main__':
    local_path = '.'
    main()