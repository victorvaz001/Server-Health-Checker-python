#!/bin/bash

calculaSpace()
{
    sudo docker info 2> /dev/null | grep  "Data Space $1:"  |  awk '{
    if ($5 == "GB")
        print $4;
    else
        print $4/1024;
    }'
}

calculaSpacePercent ()
{
    Usado=$(calculaSpace Used)
    Total=$(calculaSpace Total)
    Percentual=$(echo "scale=2;$Usado*100/$Total" | bc)
    echo $Percentual
}

case $1 in
    Total) calculaSpace $1 ;;
    Used)  calculaSpace $1 ;;
    Percent) calculaSpacePercent ;;
esac
