#!/bin/bash

#give full size of sample you want
fullsize=$1

#split by 32
size=$((fullsize / 32))

for i in {0..31}
do shuf -n $size firsts$i.out >> sample.$i.out &
done

wait

for j in {0..31}
do perl get_lang.perl sample.$j.out 1>> complete.out
done
