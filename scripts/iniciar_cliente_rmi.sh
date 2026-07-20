#!/bin/bash
cd $(dirname $0)/../src
IP=${1:-192.168.56.103}
java -cp ".:../lib/*" \
  -Djava.security.policy=../security/java.policy \
  -Djavax.net.ssl.trustStore=../security/keystore.jks \
  -Djavax.net.ssl.trustStorePassword=ipn2026 \
  mx.ipn.esimecu.rpc.ClienteRMI $IP
