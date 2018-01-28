#!/usr/bin/env bash
python print_logo.py
python demand.py -e 300 'demand001||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python demand.py -e 300 'demand002||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python demand.py -e 300 'demand003||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python demand.py -e 300 'demand004||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python demand.py -e 300 'demand005||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|12.00,6.00|'
python bid.py 'bid001||demand001'
python bid.py 'bid002||demand002'
python bid.py 'bid003||demand002,demand003'
python bid.py 'bid004||demand003,demand004,demand005'
echo "=========================================================================================="
echo "bid001 has demand001"
echo "bid002 has demand002"
echo "bid003 has demand002 and demand003"
echo "bid004 has demand003, demand004 and demand005"
echo "=========================================================================================="
echo "bid001 should be accepted"
echo "bid002 should be accepted"
echo "bid003 should be rejected"
echo "bid003 should be accepted"
echo "========================="