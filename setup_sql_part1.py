#!/bin/python3

#Week 6
#First steps to establishing a custom database
import os
import sys
import pexpect
from subprocess import run, PIPE
from shutil import copy

def setup_sql():
	password="better458WORD*()"
	child=pexpect.spawn('sudo mysql')
	child.sendline(f"alter user 'root'@'localhost' identified with mysql_native_password by '{password}';")

	#Comment this out if you don't want to run it over and over again.
	run(['mysql_secure_installation'])
	child.sendline("alter user 'root'@'localhost' identified with auth_socket;")
	child.sendline('quit')
	child.close()
	return

def copy_mysqld():
	# Copy mysqld.cnf with the user's IP address. 
	# This will allow external connections.
	output = run(["bash", "get_ip.sh"], stdout=PIPE)
	IP_ADDR = output.stdout.decode('utf-8')
	OUTPUT_FILE = "mysqld.cnf.backup"
	INPUT_FILE = "mysqld.cnf"
	DESTINATION_FILE = "/etc/mysql/mysql.conf.d/mysqld.cnf"

	line_port = f"port\t\t= 10001\n"
	line_bind_addr = f"bind-address\t\t= {IP_ADDR}\n"
	input_file=open(INPUT_FILE, 'r')
	output_file=open(OUTPUT_FILE,'w')
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
	#print("Copy was successful")
	input_file.close()
	output_file.close()
	copy(OUTPUT_FILE, DESTINATION_FILE)

def make_user():
	#2/27: gotta test this again. The syntax is technically correct but needs testing.
	# Make a user for external connections.
	# This assumes the user has a MySQL client installed on their computer.
	user="Jon"	#Your name here
	KALI_IP="10.0.0.209"	# doesn't have to be Kali.

	child=pexpect.spawn('sudo mysql')
	child.sendline(f"create user '{user}'@'{KALI_IP}' identified by 'PASS456word&*(';")
	child.sendline(f"grant select, update on classicmodels.* to '{user}'@'{KALI_IP}';")
	child.sendline("quit")
	child.close()


if os.getuid() != 0:
	print("Please run as root!")
	sys.exit()
setup_sql()
copy_mysqld()
#make_user()
