import click
import csv
import os
from common import *


DISTANCE_THRESHOLD = 4
TIME_THRESHOLD = datetime.timedelta(hours=1)


def extract_timestamp(obj):
    return obj.timestamp


def construct_obj(row):
    if row[0] == Demand.__name__:
        return Demand(*row[1:])
    else:
        return Bid(*row[1:])


def compute_distance(loc1, loc2):
    x = loc1[0] - loc2[0]
    y = loc1[1] - loc2[1]
    return x * x + y * y


def validate_consolidation(demand_ids, demand_map):
    for demand_id1 in demand_ids:
        demand1 = demand_map[demand_id1]
        for demand_id2 in demand_ids:
            demand2 = demand_map[demand_id2]
            dis = compute_distance(demand1.del_loc, demand2.del_loc)
            if dis > DISTANCE_THRESHOLD:
                print(f'validate_consolidation: demands delivery locations are too far apart, demand_id1 = {demand_id1}, demand_id2 = {demand_id2}, distance = {dis}')
                return False
            td = abs(demand1.del_time - demand2.del_time)
            if td > TIME_THRESHOLD:
                print(f'validate_consolidation: demands delivery time are too far apart, demand_id1 = {demand_id1}, demand_id2 = {demand_id2}, tiemdelta = {td}')
                return False
    return True


@click.command()
@click.option('--delete-workset', '-d', 'delete', is_flag=True)
def main(delete):
    demand_ids = []
    demand_map = {}
    closed_demand_ids = []

    # Read history block files
    history = [f for f in os.listdir('.') if f.startswith('output')]
    for his in history:
        fl = open(his, 'r')
        read_csv = csv.reader(fl, delimiter='|')
        records = [construct_obj(row) for row in read_csv if len(row) > 0]
        for record in records:
            if isinstance(record, Demand):
                demand_ids.append(record.id)
                demand_map[record.id] = record
                if record.expiry < datetime.datetime.now():
                    print(f'History demand {record.id} has expired, will not be considered.')
                    closed_demand_ids.append(record.id)
            else:
                closed_demand_ids.extend(record.demand_ids)

    # Process current block
    fl = open(INPUT_FILE, 'r')
    read_csv = csv.reader(fl, delimiter='|')
    records = [construct_obj(row) for row in read_csv if len(row) > 0]
    records.sort(key=extract_timestamp)
    new_demands = []
    bid_map = {}

    for record in records:
        if isinstance(record, Demand):
            if record.id in demand_ids:
                print(f'Ignore duplicate demand ID {record.id}')
                continue
            demand_ids.append(record.id)
            demand_map[record.id] = record
            new_demands.append(record)
        else:
            valid_bid = True
            for demand_id in record.demand_ids:
                if demand_id not in demand_ids:
                    print(f'Bid {record.id} contains non-existent demand ID {demand_id}')
                    valid_bid = False
                    break
                if demand_map[demand_id].expiry < record.timestamp:
                    print(f'Bid {record.id} contains demand ID {demand_id} that has expired.  record.timestamp = {format_ts(record.timestamp)}, demand.expiry = {format_ts(demand.expiry)}')
                    valid_bid = False
                    break
            if not valid_bid:
                continue
            if not validate_consolidation(record.demand_ids, demand_map):
                print(f'Consolidation invalid, reject bid ID {record.id}')
                continue
            bid_map[record.id] = record

    # Go through the current bids and find if any other bids contain the same demand_id
    next_bid_map = bid_map.copy()
    # Might need to run the consolidation multiple times, to reach stability
    consolidated = True
    while not consolidated:
        for k, bid in next_bid_map:
            for demand_id in record.demand_ids:
                # Now we need to decide the winner
                if demand_id in bid.demand_ids:
                    # Longest wins, otherwise earliest wins, otherwise first wins
                    if len(bid.demand_ids) < len(record.demand_ids):
                        next_bid_map[record.id] = record
                        print(f'Bid {record.id} with demands {record.demand_ids} replaced {k} with demands {record.demand_ids}')
                        consolidated = False
                else:
                    # Bid still valid, add it
                    next_bid_map[k] = bid

    print('Consolidated')
    bid_map = next_bid_map
    new_records = []
    new_records.extend(new_demands)
    new_records.extend(bid_map.values())
    new_records.sort(key=extract_timestamp)

    # Write new block
    next_block_id = len(history)
    fl = open(f'output{next_block_id}.csv', 'w+')
    writer = csv.writer(fl, delimiter='|')
    for row in [r.to_csv() for r in new_records]:
        writer.writerow(row)

    if delete:
        # Remove input block file
        os.remove(INPUT_FILE)


if __name__ == '__main__':
    main()
