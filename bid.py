import click
import csv
from common import *


@click.command()
@click.argument('bid_str')
@click.option('--over-timestamp', '-ot', 'override_timestamp')
def main(bid_str, override_timestamp):
    bid_arr = bid_str.split('|')
    if override_timestamp:
        bid_arr[1] = override_timestamp
    else:
        bid_arr[1] = format_ts(datetime.datetime.now())
    bid = Bid(*bid_arr)
    fl = open(INPUT_FILE, 'a')
    writer = csv.writer(fl, delimiter='|')
    writer.writerow(bid.to_csv())
    print(f'Added bid, id = {bid.id}')


if __name__ == '__main__':
    main()
