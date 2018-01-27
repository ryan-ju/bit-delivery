import click
import csv
from common import *


@click.command()
@click.argument('demand_str')
@click.option('--over-timestamp', '-ot', 'override_timestamp')
@click.option('--expiry', '-e', 'expiry')
def main(demand_str, override_timestamp, expiry):
    demand_arr = demand_str.split('|')
    if override_timestamp:
        demand_arr[1] = override_timestamp
    else:
        demand_arr[1] = format_ts(datetime.datetime.now())
    if expiry:
        demand_arr[6] = format_ts(datetime.datetime.now() + datetime.timedelta(seconds=int(expiry)))

    demand = Demand(*demand_arr)
    fl = open(INPUT_FILE, 'a')
    writer = csv.writer(fl, delimiter='|')
    writer.writerow(demand.to_csv())
    print(f'Added demand, id = {demand.id}')


if __name__ == '__main__':
    main()
