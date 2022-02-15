#!/bin/bash
#made smaller so it doesn't use too much processes

for i in {0..100..10}; do
  if [[ $i -eq 100 ]]; then
    break
  fi

  for j in {0..9}; do
    k=$((i + j))
    perl get_firstlast.perl $k & 
  done

  wait

done

