#!/usr/bin/env bash
python print_logo.py
python demand.py -e 300 'demand001||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python demand.py -e 300 'demand002||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand003||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|14.00,8.00|'
python demand.py -e 300 'demand004||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|14.00,10.00|'
python bid.py 'bid001||demand001,demand002'
python bid.py 'bid002||demand001,demand002,demand003'
python bid.py 'bid003||demand003,demand004'
echo "========================================================================================================"
echo "demand001 and demand002 and demand003 are temporally distant, demand003 and demand4 are temporally close"
echo "========================================================================================================"
echo "bid001 should be rejected"
echo "bid002 should be rejected"
echo "bid003 should be accepted"
echo "========================="