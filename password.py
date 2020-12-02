import string
import random
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://Jonalton:MariaJude5856%21@cluster0.pknpr.mongodb.net/test?retryWrites=true&w=majority")

db = client['Passwords']
collections = db['Passwords']

#RETURNS PASSWORD WITHOUT SYMBOLS
def defaultPW(pw):
	i = 0
	while(i<16):
		pw = pw + random.choice(string.ascii_letters + string.digits)
		i = i + 1
	return pw

#RETURNS PASSWORD WITH SYMBOLS
def symbolPW(pw):
	i = 0
	while(i<16):
		pw = pw + random.choice(string.ascii_letters + string.digits + string.punctuation)
		i = i + 1
	return pw

#RETURNS SERVICE NAME
def getServiceName():
	return input("What is the service name? ")

#RETURNS USERNAME
def getUserame():
	return input("What is the username? ")

#RETURNS PASSWORD
def getPassword():
	val = input("Does the password need symbols? ")
	pw = ""
	if (val == "y"):
		pw = symbolPW(pw)
	elif (val == "n"):
		pw = defaultPW(pw)
	return pw

#RETURNS A FORMATTED POST
def createPost(service,username,pw):
	post = {"service":service,"username":username,"password":pw}
	return post

#RETURNS A FORMATTED POST TO UPDATE EXISTING POST
def modifyPost(service,username,pw):
	post = {"$set": {"service":service,"username":username,"password":pw}}
	return post

#MODIFYS EXISTING DATA
def modifyDataSet(collections,x,username,service,password):
	print("Do you want to update with given info?" + username + password)
	inputChoice = int(input("Enter 1 for yes 0 for no "))
	if inputChoice == 1:
		newPost = modifyPost(service,username,password)
	#newPost = {"$set": {post}}
	else:
		u = getUserame()
		p = getPassword()
		newPost = modifyPost(service,u,p)
	#print(newPost)
	collections.update_one(x,newPost)

#CHECKS IF USER HAS A PASSWORD UNDER THE SERVICE NAME ALREADY
def checkifServiceExsits(db,collections,service,username,password):
	for x in collections.find({"service":service}):
		#print("You already have a password for"+service+"with the following parameters\n")
		print(x['service']+ " " + x['username'] +" "+ x['password'])
		choice = int(input("Enter a number for your options: 1 - Replace data 2 - delete old data 3 - create copy "))
		if choice == 1:	
			modifyDataSet(collections,x,username,service,password)
		elif choice == 2:
			collections.deleteOne(x)
		elif choice == 3 :
			print("Create copy of service")

#STORES IN DATABASE
def storeInDB(postList):
	while (confirm != -1):
		confirm = int(input("Enter -1 to exit loop -2 to insert all or enter individual number to insert: "))
		if (confirm == -2):	
			if (len(postList) > 1):
				for post in postList:
					db.Passwords.insert_one(post)
		elif (confirm == -1):
			break
		else:
			db.Passwords.insert_one(postList[confirm])






#pw = ""
postList = []

repeat = 1
while (repeat == 1):
	pw = ""
	service = getServiceName()
	username = getUserame()
	pw = getPassword()
	print(pw)
	postList.append(createPost(service,username,pw))
	checkifServiceExsits(db,collections,service,username,pw)
	repeat = int(input("Do you want to enter another? "))


print(postList)

#print(postList.length)
#db.posts.insertMany(postList)

