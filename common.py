import datetime

INPUT_FILE = 'input.csv'


class Demand:
    def __init__(self, id, timestamp, col_time, col_loc, del_time, del_loc, expiry):
        self.id = id
        self.timestamp = parse_ts(timestamp)
        self.col_time = parse_ts(col_time)
        self.col_loc = parse_loc(col_loc)
        self.del_time = parse_ts(del_time)
        self.del_loc = parse_loc(del_loc)
        self.expiry = parse_ts(expiry)

    def to_csv(self):
        return [
            self.__class__.__name__,
            self.id,
            format_ts(self.timestamp),
            format_ts(self.col_time),
            format_loc(self.col_loc),
            format_ts(self.del_time),
            format_loc(self.del_loc),
            format_ts(self.expiry)]


class Bid:
    def __init__(self, id, timestamp, demand_ids):
        self.id = id
        self.timestamp = parse_ts(timestamp)
        self.demand_ids = demand_ids.split(',')

    def to_csv(self):
        return [self.__class__.__name__, self.id, format_ts(self.timestamp), ','.join(self.demand_ids)]


def parse_ts(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')


def format_ts(ts):
    return ts.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def parse_loc(s):
    return [float(a) for a in s.split(',')]


def format_loc(loc):
    return ','.join([str(f) for f in loc])
