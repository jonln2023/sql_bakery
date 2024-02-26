#!/bin/bash
ufw enable
ufw allow $1/tcp
ufw reload

