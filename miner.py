import click
import csv
import os
from common import *

DISTANCE_THRESHOLD = 4
TIME_THRESHOLD = datetime.timedelta(hours=1)


def extract_timestamp(obj):
    return obj.timestamp


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
    print_marker('Mining')
    demand_ids = []
    demand_map = {}

    # Read history block files
    history = [f for f in os.listdir('.') if f.startswith('block')]
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
    next_bid_map = {}
    first_run = True
    consolidated = True
    # We may need to run this consolidation process several times.  This is to solve this problem:
    # bid1: d1
    # bid2: d1, d2
    # bid3: d2, d3, d4
    # Then bid1 and bid3 should be accepted, bid2 should be rejected.
    losers = []
    while first_run or not consolidated:
        consolidated = True
        for k_const, bid_const in bid_map.items():
            conflict = False
            loser = None
            for k, bid in next_bid_map.items():
                for demand_id in bid_const.demand_ids:
                    # Now we need to decide the winner
                    if demand_id in bid.demand_ids:
                        conflict = True
                        # Longest wins, otherwise first wins
                        if k_const not in losers and len(bid.demand_ids) < len(bid_const.demand_ids):
                            loser = k
                            losers.append(k)
                        else:
                            loser = None
            if not conflict or loser is not None:
                if not conflict:
                    print(f'Bid {k_const} with demands {bid_const.demand_ids} was added')
                else:
                    print(f'Bid {k_const} with demands {bid_const.demand_ids} replaced {loser} with demands {bid_map[loser].demand_ids}')
                next_bid_map.pop(loser, None)
                next_bid_map[bid_const.id] = bid_const
                consolidated = False
        first_run = False

    print('Consolidated')
    bid_map = next_bid_map
    new_records = []
    new_records.extend(new_demands)
    new_records.extend(bid_map.values())
    new_records.sort(key=extract_timestamp)

    # Write new block
    next_block_id = len(history)
    fl = open(f'block{next_block_id}.csv', 'w+')
    writer = csv.writer(fl, delimiter='|')
    for row in [r.to_csv() for r in new_records]:
        writer.writerow(row)

    if delete:
        # Remove input block file
        os.remove(INPUT_FILE)


if __name__ == '__main__':
    main()
