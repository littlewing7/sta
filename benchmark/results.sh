#!/bin/bash

rm -f results.txt; for i in `ls -1 *py | egrep -v BENCH`;do ( test -x $i && python3 $i | egrep Profit >> results.txt; echo >> results.txt);done

