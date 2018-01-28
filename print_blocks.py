import click
import csv
import os
from common import *


@click.command()
def main():
    # Read history block files
    history = [f for f in os.listdir('.') if f.startswith('block')]
    print(LOGO)
    for his in history:
        fl = open(his, 'r')
        read_csv = csv.reader(fl, delimiter='|')
        records = [construct_obj(row) for row in read_csv if len(row) > 0]
        bar = '=' * (20 + len(his))
        print(bar)
        print(f'||        {his}        ||')
        print(bar)
        for record in records:
            print(f'{record.__class__.__name__}: {record.to_string()}')
            print()


if __name__ == '__main__':
    main()
