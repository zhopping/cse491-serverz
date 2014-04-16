# account manager API
import sqlite3

class Account:
	def __init__(self, username, password):
		self.username = username
		self.password = password

def add_account(account):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	db.execute('INSERT INTO account_store (username, password) VALUES (?,?)', 
	(account.username, account.password))
	db.commit()
	db.close()

def exists_username(username):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT username FROM account_store WHERE username=?', (username,))
	data = c.fetchone()
	db.close()
	if data is None:
		return False
	return True

def is_valid_login(account):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT username, password FROM account_store WHERE username=? AND password=?', 
		(account.username, account.password))

	data = c.fetchone()
	db.close()
	if (data is None):
		return False
	return True
