#!/bin/sh
exist1=`ps ax |grep -c "main.py"`
echo "exist main.py: $exist1"
if [ $exist1 -lt 3 ]
then
  echo "Neustart main.py"
  sudo /root/python/snom/CeBit.new/main.py > /root/python/snom/CeBit.new/switch.log &
fi

