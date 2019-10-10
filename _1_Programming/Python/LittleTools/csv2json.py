"""
$ python csv2json.py csv_example.csv result_example.json
"""
from csv import DictReader
from json import dump
from sys import argv

if __name__ == '__main__':
    csv_file = argv[1]
    json_file = argv[2]
    with open(csv_file, 'r') as c, open(json_file, 'w') as j:
        reader = DictReader(c)
        datas = []
        for row in reader:
            datas.append(row)
        dump(datas, j)
