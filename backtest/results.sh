#!/bin/bash

mkdir -p results


GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)

for i in SPY NVDA TSLA XLE MSFT
do
    rm -f results/$i
    for x in `ls -1 *py`
    do
        echo
        echo " --->>>  Exec [${GREEN}$x -t $i -l results/$i${NORMAL}]"
        python3 $x -t $i -l results/$i
        sleep 1
    done
    cat results/$i | sort -nr -k 3 | tee results/$i.tmp
    mv -f results/$i.tmp results/$i
done

