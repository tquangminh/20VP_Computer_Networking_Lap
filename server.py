import socket
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox 
import json
import threading
import sqlite3
import os

# Read json user file to list
def readFile():
	global list_user
	with open('users.json') as json_file:
		data = json.load(json_file)
		for i in data['Information of Users']:
			list_user.extend((i['username'], i['password']))
            
# Write json user file
def writeFile(info):
	with open('users.json', 'r+') as file:
		data = json.load(file)
		data['Information of Users'].append(info)
		file.seek(0)
		json.dump(data, file, indent = 4)

#Sign Up
def checkSignUp(username, password):
    global list_user
    global add_info
    i = 0
    while i < len(list_user):
        if username == list_user[i]:
            return False
        i += 2

    list_user.extend((username, password))
    add_info.extend((username, password))
    
    print("Adding new info")
    i = 0
    while i < len(add_info):
        info = {'username': add_info[i], 'password': add_info[i+1]}
        writeFile(info)
        i += 2

    sqliteConnection = sqlite3.connect('user_note.db')
    cursor = sqliteConnection.cursor()
    
    cursor.execute("CREATE TABLE '%s' ('noteId' INTEGER NOT NULL, 'type' TEXT NOT NULL, 'tittle' TEXT, 'content' TEXT, PRIMARY KEY('noteId' AUTOINCREMENT));"%(username))
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
    return True

#Log In
def checkLogIn(username, password):
	global list_user
	i=0
	while i < len(list_user):
		if username == list_user[i] and password == list_user[i+1]:
			feedback = "Log in successfully\n"+"Welcome " + username
			return feedback, True

		elif username == list_user[i] and password != list_user[i+1]:
			feedback = "Wrong password"
			return feedback, False

		i += 2
	
	feedback = "Account has not been signed up yet"
	return feedback, False

def threaded_client(con, addr):
    global list_user
    global add_info
    global stop_thread

    req = con.recv(1024).decode("utf8")	
    												#1.1
    con.sendall("Received Requestment".encode("utf8"))									#1.2

    username = con.recv(1024).decode("utf8")											#2.1
    con.sendall("Received Username".encode("utf8"))										#2.2

    password = con.recv(1024).decode("utf8")											#3.1

    print("Requestment: " + req)
	
    if req == "Sign up":
        if checkSignUp(username, password) == True:
            con.sendall("Sign up successfully".encode("utf8"))							#4.1
            con.recv(1024)																#4.2
        else:
            con.sendall("Account has existed".encode("utf8"))							#4.1
            con.recv(1024)																#4.2

    elif req == "Log in":
        feedback , criteria = checkLogIn(username, password)
        con.sendall(feedback.encode("utf8"))											#4.1
        con.recv(1024)																	#4.2

        if criteria == False:
            con.sendall("Disconnect".encode("utf8"))									#5.1

        elif criteria == True:

            con.sendall("Connect".encode("utf8"))                
            sqliteConnection = sqlite3.connect('user_note.db')
            print("Database created and Successfully Connected to SQLite")
            while True:
                if stop_thread:
                    break
                req = con.recv(1024).decode("utf8")
                if req == "Add Note":
                    con.sendall("Received adding note request".encode("utf8"))
                    type = con.recv(1024).decode("utf8")
                    con.sendall("Received type note".encode("utf8"))
                    if type == "Text":
                        tittle = con.recv(1024).decode("utf8")
                        con.sendall("Recevied tittle".encode("utf8"))
                        content = con.recv(4096).decode("utf8")
                    elif type == "Image": 
                        tittle = con.recv(1024).decode("utf8")
                        con.sendall("Recevied tittle".encode("utf8"))
                        filename = con.recv(1024).decode("utf8")
                        con.sendall('Received File Name'.encode("utf8"))
                        filesize = con.recv(1024)
                        con.sendall('Received File Size'.encode("utf8"))

                        filename = "disk/" + os.path.basename(filename)
                        filesize = int(filesize)
                        with open(filename, "wb") as f:

                                # read 1024 bytes from the socket (receive)
                                bytes_read = con.recv(filesize+1024) 
                                # write to the file the bytes we just received
                                f.write(bytes_read)                                              
                                    # update the progress bar
                        content = filename
                    elif type == "File": 
                        tittle = con.recv(1024).decode("utf8")
                        con.sendall("Recevied tittle".encode("utf8"))
                        filename = con.recv(1024).decode("utf8")
                        con.sendall('Received File Name'.encode("utf8"))
                        filesize = con.recv(1024)
                        con.sendall('Received File Size'.encode("utf8"))

                        filename = "disk/" + os.path.basename(filename)
                        filesize = int(filesize)
                        with open(filename, "wb") as f:

                                # read 1024 bytes from the socket (receive)
                                bytes_read = con.recv(filesize+1024)
                                # write to the file the bytes we just received
                                f.write(bytes_read)                                              
                                    # update the progress bar
                        content = filename

                    try:
                        cursor = sqliteConnection.cursor()
                        cursor.execute("INSERT INTO %s (type,tittle,content) VALUES ('%s', '%s', '%s')" %(username, type, tittle, content))
                        sqliteConnection.commit()
                        con.sendall("Saved".encode("utf8"))
                        cursor.close()
                    except: 
                        con.sendall("Cannot Saved".encode("utf8"))

                elif req == "View Note":
                    sqliteConnection = sqlite3.connect('user_note.db') 
                    cursor = sqliteConnection.cursor()
                    cursor.execute("Select tittle from %s"%(username))
                    topicList = cursor.fetchall()
                    csvTopicList = topicList[0][0]
                    for i in topicList[1:]:
                        csvTopicList += "," + i[0]

                    con.sendall(csvTopicList.encode("utf8"))
                    topicSelected = con.recv(1024).decode("utf8")
                    if topicSelected == 'Back':
                        continue   
                    else:              
                        cursor.execute("Select type, content from %s where tittle == '%s' "%(username, topicSelected))
                        type_content = cursor.fetchall()

                        if type_content[0][0] == 'Text':
                            con.sendall('Text'.encode("utf8"))
                            con.recv(1024)
                            con.sendall(type_content[0][1].encode("utf8"))
                        elif type_content[0][0] == 'File' or type_content[0][0] == 'Image':
                            if type_content[0][0] == 'File':
                                con.sendall('File'.encode("utf8"))
                            else: 
                                con.sendall('Image'.encode("utf8"))
                            con.recv(1024)
                            filename = (type_content[0][1])
                            filesize =os.path.getsize(filename)
                            con.sendall(filename.encode("utf8"))
                            con.recv(1024)
                            
                            con.sendall(str(filesize).encode("utf8"))
                            con.recv(1024)

                            with open(filename, "rb") as f:
                                    # read the bytes from the file
                                    bytes_read = f.read(filesize+1024)
                                    con.sendall(bytes_read)
                        cursor.close()
                        sqliteConnection.close()


                else:
                    break
            sqliteConnection.close()
    con.close()

#def start server:
def start_server():
    print("Start")
    while True:
        try:
            con, addr = s.accept()
            print("Connected to: " + str(addr))
            iden = con.recv(1024).decode("utf8")
            if iden == "Client":
                con.sendall("Welcome Client".encode("utf8"))
                client = threading.Thread(target=threaded_client, args=(con,addr))
                client.daemon = True
                client.start()
        except:
            print("Disconnect")
            break
            


#server_thread
def server_thread():
    root.config(bg="#2ecc71")
    global stop_thread
    stop_thread = False

    global check
    if check == 1:
        messagebox.showinfo("Status", "Server has been running")
        return

    check = 1

    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    HOST = str(ip_addr)
    PORT = 1239

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    s.listen(5)
    print("IP: " + HOST + '; Port: ' + str(PORT))
    print("Waiting for a Connection...")

    sv = threading.Thread(target=start_server)
    sv.daemon = True
    sv.start()

def add_and_close():
	root.config(bg="white")
	global check
	global stop_thread
	if check == 0:
		messagebox.showinfo("Status", "Server has not been started yet")
		return
	
	check = 0

	stop_thread = True
	s.close()
	print("Close Server")


#MAIN
list_user = []
readFile()
check = 0
add_info = []

#Server Window
root = Tk()
root.title("Server")

style = ttk.Style()
style.configure('TButton', font =
			('calibri', 20, 'bold'))

style.map('W.TButton', foreground = [('active', 'black')],
					background = [('active', '#DC143C')])

style.map('TButton', foreground = [('active','!disabled', 'black')],
					background = [('active', '#9ACD32')])

btn1 = Button(root, text = 'Start Server', command = server_thread)
btn1.grid(ipadx = 30, ipady=30,padx=20,pady=10)

btn2 = Button(root, text = 'Disconnect',style="W.TButton", command = add_and_close)
btn2.grid(ipadx = 30, ipady=30,padx=20,pady=10)

root.mainloop()