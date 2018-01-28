#!/usr/bin/env bash
python print_logo.py
python demand.py -e 300 'demand001||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand002||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand003||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand004||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand005||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python bid.py 'bid001||demand001,demand002'
python bid.py 'bid002||demand001,demand002,demand003'
python bid.py 'bid003||demand002,demand003'
python miner.py -d
python demand.py -e 300 'demand006||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python bid.py 'bid004||demand004,demand005'
python bid.py 'bid005||demand004,demand005,demand006'
python bid.py 'bid006||demand006'
python bid.py 'bid007||demand003,demand004,demand005,demand006'
python miner.py -d
python demand.py -e 300 'demand007||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand008||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand009||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python demand.py -e 300 'demand010||2018-02-01T15:15:00.000Z|5.00,5.00|2018-02-01T23:00:00.000Z|8.00,8.00|'
python bid.py 'bid008||demand008'
python bid.py 'bid009||demand007,demand008,demand009'
python bid.py 'bid010||demand006'
python miner.py
echo "========================="
echo "bid001 should be rejected"
echo "bid002 should be accepted"
echo "bid003 should be rejected"
echo "bid004 should be rejected"
echo "bid005 should be rejected"
echo "bid006 should be rejected"
echo "bid007 should be accepted"
echo "bid008 should be rejected"
echo "bid009 should be accepted"
echo "bid010 should be rejected (should be, but I have a bug to fix)"
echo "========================="