import rsa
import sys
import sqlite3
import os
import time
from termcolor import colored, cprint
from getpass import getpass
import hashlib

# Path to database file
DB_PATH = '/YOUR/PATH/database.db'
# Path to folder containing RSA keys and keychain master password hash
KEY_PATH = '/YOUR/PATH'

# Connect to db
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Add new item
def add(mode=0):
	if mode == 1:
		account = sys.argv[2]
		email = sys.argv[3]
		password = sys.argv[4]
		username = sys.argv[5]
		pin = sys.argv[6]
	else:
		account = input("Account: ")
		email = input("Email: ")
		password = input("Password: ")
		username = input("Username: ")
		pin = input("PIN: ")


	pub = rsa.PublicKey.load_pkcs1(open(KEY_PATH + '/pub','r').read())
	encrPwd = rsa.encrypt(password.encode(), pub)

	# Check if email exists, if not, add
	check = cur.execute(f''' SELECT account FROM data WHERE account=\"{account}\" ''').fetchone()
	if check == None:
		cur.execute(f''' INSERT INTO data (account,email,password,username,pin) VALUES (\"{account}\",\"{email}\",\"{encrPwd.hex()}\",\"{username}\", \"{pin}\") ''')
		print("Item successfully added...")
	# If so, update item
	else:
		cur.execute(f''' UPDATE data SET email = \"{email}\" WHERE account = \"{account}\" ''')
		cur.execute(f''' UPDATE data SET password = \"{encrPwd.hex()}\" WHERE account = \"{account}\" ''')
		cur.execute(f''' UPDATE data SET username = \"{username}\" WHERE account = \"{account}\" ''')
		cur.execute(f''' UPDATE data SET pin = \"{pin}\" WHERE account = \"{account}\" ''')
		print("Item successfully updated...")

	conn.commit()
	time.sleep(1)
	os.system('clear')
	
# Remove item from db
def remove():
	selection = input("Account to remove: ")
	if selection == "x":
		cprint("Cancelled...",'red')
	else:
		check = cur.execute(f''' SELECT account FROM data WHERE account=\"{selection}\" ''').fetchone()
		if check == None:
			print("That item does not exist...")
			return

		cur.execute(f"DELETE FROM data WHERE account = \"{selection}\";")
		conn.commit()
		print("Item successfully removed... ")

	time.sleep(1)
	os.system('clear')

# Search for account
def search():
	priv = rsa.PrivateKey.load_pkcs1(open(KEY_PATH + '/.priv_key','r').read())

	selection = input(colored("Search: ",'magenta'))
	os.system('clear')
	rows = cur.execute("SELECT * FROM data").fetchall()

	print(colored(f"{'[account]':25}   {'[email]':25}   {'[password]':25}   {'[username]':25}   {'[pin]':10}", 'blue'))
	for row in rows:
		data = f"{row[0]} {row[1]} {rsa.decrypt(b''.fromhex(row[2]), priv).decode()} {row[3]} {row[4]}".lower()
		if selection in data:
			print(f"{row[0]:25} - {row[1]:25} - {rsa.decrypt(b''.fromhex(row[2]), priv).decode():25} - {row[3]:25} - {row[4]:10}")
			

	
# Menu to view emails:passwords
def menu():
	print(colored(" Menu", 'blue'))
	print(colored("=======", 'blue'))
	print("a) Add Item")
	print("r) Remove Item")
	print("s) Search")
	print("l) List Items")
	print("x) Exit")
	return input(":: ")
	
	


# Display all items in db
def display():
	os.system('clear')
	priv = rsa.PrivateKey.load_pkcs1(open(KEY_PATH + '/.priv_key','r').read())

	rows = cur.execute("SELECT * FROM data").fetchall()
	print(colored(f"{'[account]':25}   {'[email]':25}   {'[password]':25}   {'[username]':25}   {'[pin]':10}", 'blue'))
	cprint("---------------------------------------", 'blue')
	for row in rows:
		print(f"{row[0]:25} - {row[1]:25} - {rsa.decrypt(b''.fromhex(row[2]), priv).decode():25} - {row[3]:25} - {row[4]:10}")
	cprint("\n---------------------------------------",'blue')

# Menu loop
def view():
	while True:
		selection = menu()
		if selection == 'a':
			add()
		elif selection == 'r':
			remove()
		elif selection == 's':
			search()
		elif selection == 'l':
			display()
		elif selection == 'x':
			print("Exiting...")
			conn.close()
			exit(0)
		else:
			print(colored("Invalid selection...", 'red'))
			time.sleep(1)
			os.system('clear')


# Main
# =====
if __name__ == "__main__":
	# Master password prompt
	pwd = getpass("Password: ")
	sha = hashlib.sha256()
	sha.update(pwd.encode())
	master = open(KEY_PATH + '/master','r').read()

	if sha.hexdigest() != master[0:len(master) - 1]:
		print("NOPE")
		exit()

	# Check arguments
	if len(sys.argv) > 1:
		if sys.argv[1] == 'add':
			add(1)
		elif sys.argv[1] == 'view':
			display()
	else:
		view()
