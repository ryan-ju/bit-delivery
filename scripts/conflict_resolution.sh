#!/usr/bin/env bash
python print_logo.py
python demand.py -e 300 'demand001||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand002||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand003||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand004||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python bid.py 'bid001||demand001,demand002'
python bid.py 'bid002||demand001,demand002,demand003'
python bid.py 'bid003||demand002,demand003'
echo "========================================================================================================"
echo "bid002 consolidates 3 demands, bid001 and bid003 consolidate 2 demands"
echo "========================================================================================================"
echo "bid001 should be rejected"
echo "bid002 should be accepted"
echo "bid003 should be rejected"
echo "========================="
