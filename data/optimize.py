# -*- coding: utf8 -*-

import csv

def main():
    with open('test.csv', 'r', encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print (row['name'], row['categories'])


if __name__ == '__main__':
    main()