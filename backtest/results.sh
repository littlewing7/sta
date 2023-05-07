#!/bin/bash

rm -f results.txt; date > results.txt; for i in `ls -1 *py | egrep -v BENCH`;do ( sleep 3; test -x $i && python3 $i | egrep Profit >> results.txt; echo >> results.txt);done
git add . && git commit -m 'backtest results update' && git push

