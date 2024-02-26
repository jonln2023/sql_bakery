#!/bin/bash
ip_addr=$(ip a|grep 'inet '|grep -v '127.0.0.1'|awk '{print $2}'|cut -d'/' -f1)
#uncomment this line to get the gateway address. Might be useful later.
#networkPart=$(echo $ip_addr|cut -d'.' -f-3)
echo $ip_addr 


