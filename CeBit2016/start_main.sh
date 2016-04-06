#!/bin/sh
exist1=`ps ax |grep -c "main.py"`
echo "exist main.py: $exist1"
if [ $exist1 -lt 3 ]
then
  echo "Neustart main.py"
  sudo /home/pi/snom_smarthome/CeBit2016/main.py > /home/pi/snom_smarthome/CeBit2016/switch.log &
fi

