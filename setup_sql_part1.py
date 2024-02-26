#!/bin/python3

#Week 6
#First steps to establishing a custom database
import os
import sys
import pexpect
from subprocess import run, PIPE
def setup_sql():
	if os.getuid() != 0:
		print("Please run as root!")
		sys.exit()
	password="better458WORD*()"
	child=pexpect.spawn('sudo mysql')
	child.sendline(f"alter user 'root'@'localhost' identified with mysql_native_password by '{password}';")
	run(['mysql_secure_installation'])
	child.sendline("alter user 'root'@'localhost' identified with auth_socket;")
	#print('2',child.readline())
	child.sendline('quit')
	child.close()
	return
	
#usage: copy_mysqld.py $(get_ip.sh)

#import sys
def copy_mysqld():
	output = run(["bash", "get_ip.sh"], stdout=PIPE)
	IP_ADDR = output.stdout.decode('utf-8')
	OUTPUT_FILE = "mysqld.cnf.backup"
	INPUT_FILE = "mysqld.cnf"
	DESTINATION_FILE = "/etc/mysql/mysql.conf.d/mysqld.cnf"

	line_port = f"port\t\t= 10001\n"
	line_bind_addr = f"bind-address\t\t= {IP_ADDR}\n"
	print(IP_ADDR)
	return
	with open(INPUT_FILE,'r') as input_file, open(OUTPUT_FILE,'w') as output_file:
		while True:
			line=input_file.readline()
			if not line:
				break
			elif line.startswith("bind-address\t\t="):
				output_file.write(line_bind_addr)
			elif line.startswith("port"):
				output_file.write(line_port)
			else:
				output_file.write(line)
	print("Copy was successful")
	print(f"Now run 'sudo cp {OUTPUT_FILE} {DESTINATION_FILE}'")


def make_user():
	if os.getuid() != 0:
		print("Please run as root!")
		sys.exit()

	user="Jon"	#Your name here
	KALI_IP="10.0.0.209"	#doesn't have to be Kali

	child=pexpect.spawn('sudo mysql')
	child.sendline(f"create user '{user}'@'{KALI_IP}' identified by 'PASS456word&*(';")
	child.sendline(f"grant select, update on classicmodels.* to '{user}'@'{KALI_IP}';")
	child.sendline("quit")
	child.close()

copy_mysqld()
setup_sql()
