#!/bin/bash
# Usage: sudo ./change_firewall.sh 10001
ufw enable
ufw allow $1/tcp
ufw reload

