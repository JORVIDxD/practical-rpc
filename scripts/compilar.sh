#!/bin/bash
cd $(dirname $0)/../src
javac -cp ".:../lib/*" mx/ipn/esimecu/rpc/*.java
echo "Compilacion completada con exito."
