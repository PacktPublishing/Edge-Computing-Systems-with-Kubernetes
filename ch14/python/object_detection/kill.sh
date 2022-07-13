P=$(ps -ax | grep kubectl | grep -v grep | awk '{ print $1 }');for p in ${P[*]}; do kill $p; done
