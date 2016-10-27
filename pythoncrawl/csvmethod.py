#!/usr/bin/env python
# encoding: utf-8

import csv

class Method():
# dialect是访问csv文件时需要指定的参数之一，用来确定csv文件的数据格式
# 下面这个函数列举系统支持的dialect有哪些，默认值是'excel'，用户也可
# 以从Dialect派生一个类，使用该类的实例作为dialect参数。
    #print csv.list_dialects()
    def test_writer():
    # csv文件必须以二进制方式open
        with open('eggs.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    def test_reader():
        with open('eggs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                print (row)
                # sniffer 用来推断csv文件的格式，不是很准确
    def test_sniffer():
        with open('eggs.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ')
            spamwriter.writerow(['Spam'] * 2 + ['Baked Beans'])
            spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        # 通常你需要指定与写入者相同的文件格式才能正确的读取数据
        with open('eggs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for row in spamreader:
                print (', '.join(row))
            # 如果不知道文件格式，sniffer就可以派上用场了
        with open('eggs.csv', 'rb') as csvfile:
        # 用sniffer推断文件格式，从而得到dialect
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            print (dialect.delimiter, dialect.quotechar)
            # 文件重新移动
            csvfile.seek(0)
            # 用推断出来的dialect创建reader
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                print (', '.join(row))
