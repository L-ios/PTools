#!/usr/bin/python
# -*- coding:utf-8 -*-
import io
import os
import sys

import sqlite3
from io import StringIO
from optparse import OptionParser

from scan import CLOMUN_NAMES, BASE_TABLE_NAME, CLOMUN_PACKAGE, CLOMUN_VALUE, BRICK_DB_DIR, BRICK_DB
from options import deal_trope

build_package_name = 'android.build'
BUILD_PROP = 'build.prop'
FILTER = False
brick_db = None
build_prop_dir = None
brick_temp = 'out/temp/'

option_f = {
    'name': ('-f', '--filter'),
    'help': u'过滤android.build中未配置的配置项目',
    'nargs': 0,
}
option_i = {
    'name': ('-i', '--input'),
    'help': u'数据库文件,默认读取当前目录下的brick_pack/brick/brick.db',
    'nargs': 1,
}
option_o = {
    'name': ('-o', '--outdir'),
    'help': u'输出的文件位置， 默认输出到当前目录下的out/temp目录中',
    'nargs': 1,
}
option_u = {
    'name': ('-u', '--update-file'),
    'help': u'需要更新的build.prop文件',
    'nargs': 1,
}

options = [option_f, option_i, option_o, option_u]


def get_data():
    if os.path.exists(brick_db) is False:
        exit(unicode(brick_db) + u'不存在')
    with sqlite3.connect(brick_db) as brick_sqlite:
        brick_cursor = brick_sqlite.cursor()
        select_sql = 'SELECT "' + CLOMUN_NAMES + '","' \
                     + CLOMUN_VALUE + '" ' \
                     + 'FROM "' + BASE_TABLE_NAME + '" ' \
                     + 'WHERE "' + CLOMUN_PACKAGE + '" is "' + build_package_name + '"'
        brick_cursor.execute(select_sql)
        build_info = {}
        for row in brick_cursor.fetchall():
            values = deal_trope(row[1])
            if len(values) != 1:
                print(u'存在问题的配置为：')
                exit(row[0])
            else:
                build_info[row[0]] = values[0].rstrip()

        return build_info


def update_info(update_file, build_info):
    '''
    更新build.prop文件
    :param update_file: 需要更新的build.prop文件地址
    :return: 
    '''
    global FILTER
    if os.path.exists(update_file) is False:
        print(u'%s不存在' % update_file)
        return

    # build_prop_str = u''
    strio = StringIO()
    with io.open(os.path.abspath(update_file), mode='r+', encoding='utf-8') as build_prop_file:
        if build_prop_file.seekable():
            build_prop_file.seek(0)
        if build_prop_file.readable():
            while True:
                str_line = build_prop_file.readline()
                if len(str_line) == 0:
                    break
                str_line = str_line.rstrip('\n')
                key = str_line.split('=', 1)[0]
                if build_info.get(key) is not None:
                    continue
                else:
                    strio.write(str_line + '\n')
            for k, v in build_info.items():
                if FILTER and len(v) == 0:
                    continue
                line_string = k + '=' + v + '\n'
                strio.write(line_string)
        if build_prop_file.seekable():
            build_prop_file.seek(0)
        if build_prop_file.writable():
            build_prop_file.write(strio.getvalue())


def save_data(build_info):
    global FILTER, build_prop_dir
    join, exists = os.path.join, os.path.exists
    if exists(build_prop_dir) is False:
        os.makedirs(build_prop_dir)
    build_prop = join(build_prop_dir, BUILD_PROP)
    with io.open(build_prop, mode='w') as build_prop_file:
        for k, v in build_info.items():
            if FILTER and len(v) == 0:
                continue
            line_string = k + '=' + v + '\n'
            build_prop_file.write(line_string)


def post_main():
    build_info = get_data()
    save_data(build_info)


def main(options, arguments):
    global FILTER, brick_db, build_prop_dir
    if options.filter is not None:
        FILTER = True

    if options.input is not None:
        brick_db = options.input
    else:
        brick_db = os.path.join(BRICK_DB_DIR, BRICK_DB)

    if options.outdir is not None:
        build_prop_dir = options.outdir
    else:
        build_prop_dir = brick_temp

    if options.update_file is None:
        post_main()
    else:
        # build_info = get_data()
        build_info = []
        update_info(options.update_file, build_info)

if __name__ == '__main__':
    script_path = os.path.abspath(sys.argv[0])
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
