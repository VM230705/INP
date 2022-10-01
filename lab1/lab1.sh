#!/bin/sh
tcpdump -r lab_tcpdump.pcap -v > packet2.txt
ttl=$(cat packet2.txt | awk -F'[, ]' 'BEGIN{OFS='\t'} length($7)<=3 {print $7}' | sort -n | tail -1)
echo "${ttl}"
tcpdump -r lab_tcpdump.pcap -v -X ip[8]==${ttl} > magic2.txt
cat magic2.txt | awk '{print $10}' | awk -F'[. {]' 'BEGIN{OFS='\t'} NR>=3&&/[A-Za-z0-9+/]{7}/{print $1, $4, $5}' | base64 -d
# cat out.txt | base64 -d
