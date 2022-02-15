#!/bin/bash

for i in {0..24}
  do perl get_auths.perl $i &
done

wait 

for i in {25..49}
  do perl get_auths.perl $i &
done

wait

for i in {50..74}
  do perl get_auths.perl $i &
done

wait

for i in {75..99}
  do perl get_auths.perl $i &
done
