from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import socket
import os,sys

window = Tk()
window.title('Client')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

link = resource_path("show.png")
link2 = resource_path("hide.png")
show = PhotoImage(file = link)
hide = PhotoImage(file = link2)

style = ttk.Style()
style.theme_use("clam")
txt_cl = "#F5DEB3"

frame1 = Frame(window)
frame1.grid()

def EnterIP():
    def entry_clear_IP(e):
        if ip_entry.get() == "Enter IP":
            ip_entry.delete(0,END)
    global can
    can = Canvas(frame1, width = 1024, height = 640)
    can.grid(row=0,column=0)
    can.create_text(520,230,text="Connect to Server", font=("Comic Sans MS",24,'bold'),fill="#400000")

    ip_entry = Entry(frame1, font=("Courier New", 11),fg="black", bd=0)
    ip_entry.place(x=412, y=300,width=220,height=25)
    ip_entry.insert(0,"Enter IP")

    def checkIP():
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        HOST = str(ip_addr)
        PORT = 1239

        if ip_entry.get() != HOST:
            messagebox.showinfo("Status", "Wrong IP")
            return

        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.connect((HOST, PORT))
            messagebox.showinfo("Status", "Connect to Server successfully")
            main()
        except:
            messagebox.showinfo("Connection Lost", "Server has disconnected")
            return

    ip_btn = Button(frame1, text="Connect",font=("Fira", 16,'bold'), width=16,fg="#336d92",bd=5,command=checkIP)
    ip_btn.place(x=411,y=340)

def main():
    can.destroy()
    x=430
    y=240

    def entry_clear_un(e):
        if un_entry.get() == "Enter username":
            un_entry.delete(0,END)
    def entry_clear_pw(e):
        if pw_entry.get() == "Enter password":
            pw_entry.delete(0,END)
            pw_entry.configure(show="●")    
    
    def showPW():
        global hide_show
        hide_show.destroy()
        hide_show = Button(my_canvas, image=hide,bd=0,command=hidePW)
        hide_show.place(x=x+176,y=y+50,width=25,height=25)
        pw_entry.config(show="")
    def hidePW():
        global hide_show
        hide_show.destroy()
        hide_show = Button(my_canvas, image=show,bd=0,command=showPW)
        hide_show.place(x=x+176,y=y+50,width=25,height=25,)
        pw_entry.config(show="●")

    def after_login():
        username = un_entry.get()
        password = pw_entry.get()

        if username == "Enter username" or username == "":
            messagebox.showinfo("Status", "Please enter username")
            return
        for i in username:
            if i == " ":
                messagebox.showinfo("Status", "Username must contain no space character")
                return
        
        if password == "Enter password" or password == "":
            messagebox.showinfo("Status", "Please enter password")
            return
        for i in password:
            if i == " ":
                messagebox.showinfo("Status", "Password must contain no space character")
                return
        
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        HOST = str(ip_addr)
        PORT = 1239

        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            cli.connect((HOST, PORT))
        except:
            messagebox.showinfo("Connection Lost", "Server has disconnected")
            return

        print("Connected to ('" + HOST + "', " + str(PORT) + ")")

        cli.sendall("Client".encode("utf8"))
        cli.recv(1024)

        req = "Log in"    
        cli.sendall(req.encode("utf8"))
        cli.recv(1024)

        cli.sendall(username.encode("utf8"))
        cli.recv(1024)

        cli.sendall(password.encode("utf8"))

        feedback = cli.recv(1024).decode("utf8")
        cli.sendall("Received Feedback".encode("utf8"))
        messagebox.showinfo("Status", feedback)

        status = cli.recv(1024).decode("utf8")
        if status == "Disconnect":
            return
            cli.close()
        elif status == "Connect":
            def main2():
                my_canvas.destroy() 
                can_show = Canvas(frame1, width = 810, height = 360)
                can_show.pack(fill = "both", expand = True)

                def log_out():
                    cli.close()
                    can_show.destroy()
                    main()

                def out():
                    cli.close()
                    window.destroy()

                

                def addNote():
                    can_show.destroy()
                    cli.sendall("Add Note".encode("utf8"))
                    cli.recv(1024)
                    can_Note = Canvas(frame1, width = 810, height = 360)
                    can_Note.pack(fill = "both", expand = True)        

                    def textNote():
                        can_Note.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360)
                        can_addTypeNote.pack(fill = "both", expand = True)
                        def textSubmit():
                            cli.sendall("Text".encode("utf8"))
                            cli.recv(1024)

                            tittle = tittleBox.get()
                            cli.sendall(tittle.encode("utf8"))
                            cli.recv(1024)

                            text_content = text_box.get("1.0", END)
  
                            cli.sendall(text_content.encode("utf8"))
                            message = cli.recv(1024).decode("utf8")
                            messagebox.showinfo(message)
                            can_addTypeNote.destroy()
                            text_box.destroy()
                            main2()

                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 11),fg="black", bd=0)
                        tittleBox.place(x=105, y=10,width=600,height=100)

                        text_box = Text()
                        text_box.place(x=105, y=40,width=600,height=200)
                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=("Candara",11),borderwidth=4, command=textSubmit) 
                        SubmitBtn.place(x=343, y=310, height=27, width=124)
                    
                    def imgNote():
                        can_Note.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360)
                        can_addTypeNote.pack(fill = "both", expand = True)
                        def textSubmit():
                            cli.sendall("Image".encode("utf8"))
                            cli.recv(1024)

                            tittle = tittleBox.get()
                            cli.sendall(tittle.encode("utf8"))
                            cli.recv(1024)

                            filename = (pathEntry.get())
                            filesize =os.path.getsize(filename)
                            cli.sendall(filename.encode("utf8"))
                            cli.recv(1024)
                            
                            cli.sendall(str(filesize).encode("utf8"))
                            cli.recv(1024)
                        
                            with open(filename, "rb") as f:
                                # read the bytes from the file
                                bytes_read = f.read(filesize+1024)
                                cli.sendall(bytes_read)

                            message = cli.recv(1024).decode("utf8")
                            messagebox.showinfo(message)
                            can_addTypeNote.destroy()
                            pathEntry.destroy()
                            main2()

                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 11),fg="black", bd=0)
                        tittleBox.place(x=105, y=10,width=600,height=100)

                        pathEntry = Entry(can_addTypeNote, font=("Courier New", 11),fg="black", bd=0)
                        pathEntry.place(x=105, y=150,width=600,height=100)
                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=("Candara",11),borderwidth=4, command=textSubmit) 
                        SubmitBtn.place(x=343, y=310, height=27, width=124)       

                    def fileNote():
                        can_Note.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360)
                        can_addTypeNote.pack(fill = "both", expand = True)
                        def textSubmit():
                            cli.sendall("File".encode("utf8"))
                            cli.recv(1024)

                            tittle = tittleBox.get()
                            cli.sendall(tittle.encode("utf8"))
                            cli.recv(1024)

                            filename = (pathEntry.get())
                            filesize =os.path.getsize(filename)
                            cli.sendall(filename.encode("utf8"))
                            cli.recv(1024)
                            
                            cli.sendall(str(filesize).encode("utf8"))
                            cli.recv(1024)
                        
                            with open(filename, "rb") as f:
                                # read the bytes from the file
                                bytes_read = f.read(filesize+1024)
                                cli.sendall(bytes_read)

                            message = cli.recv(1024).decode("utf8")
                            messagebox.showinfo(message)
                            can_addTypeNote.destroy()
                            pathEntry.destroy()
                            main2()

                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 11),fg="black", bd=0)
                        tittleBox.place(x=105, y=10,width=600,height=100)

                        pathEntry = Entry(can_addTypeNote, font=("Courier New", 11),fg="black", bd=0)
                        pathEntry.place(x=105, y=150,width=600,height=100)
                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=("Candara",11),borderwidth=4, command=textSubmit) 
                        SubmitBtn.place(x=343, y=310, height=27, width=124)  

                    textBtn = Button(can_Note, text="Text",font=("Candara",11),borderwidth=4, command=textNote)
                    textBtn.place(x=156, y=305, height=27, width=124)

                    imgBtn = Button(can_Note, text="Image",font=("Candara",11),borderwidth=4, command=imgNote)
                    imgBtn.place(x=270, y=305, height=27, width=124)

                    fileBtn = Button(can_Note, text="File",font=("Candara",11),borderwidth=4, command=fileNote)
                    fileBtn.place(x=370, y=305, height=27, width=124)

                    can_Note.mainloop()

                def viewNote():
                    can_show.destroy()
                    cli.sendall("View Note".encode("utf8"))
                    topicList = cli.recv(1024)
                    can_Note = Canvas(frame1, width = 810, height = 360)
                    can_Note.pack(fill = "both", expand = True) 
                    global topicListBox
                    topicListBox = Listbox(can_Note, yscrollcommand=True)
                    
                    can_Note.mainloop()
               


                log_out1 = Button(can_show, text="Log out",font=("Candara",11),borderwidth=4,bg="#DB7093", command=log_out)
                log_out1.place(x=31, y=305, height=27, width=122)

                exit_ = Button(can_show, text="Exit",font=("Candara",11),borderwidth=4,bg="#CD5C5C", command=out)
                exit_.place(x=156, y=305, height=27, width=124)   

                addNoteBtn = Button(can_show, text="Add Note",font=("Candara",11),borderwidth=4, command=addNote)
                addNoteBtn.place(x=31, y=105, height=27, width=122)

                viewNoteBtn = Button(can_show, text="View Note",font=("Candara",11),borderwidth=4, command=viewNote)
                viewNoteBtn.place(x=131, y=105, height=27, width=122)
                can_show.mainloop()  
            main2()

    def signup1():
        def entry_clear_unsu(e):
           if un_entry_signup.get() == "Enter username":
                un_entry_signup.delete(0,END)
        def entry_clear_pwsu(e):
            if pw_entry_signup.get() == "Enter password":
                pw_entry_signup.delete(0,END)
                pw_entry_signup.config(show="●")
        def entry_clear_pwa(e):
            if pw_confirm_entry.get() == "Enter password again":
                pw_confirm_entry.delete(0,END)
                pw_confirm_entry.config(show="●")
        def back():
            my_canvas_sign.destroy()
            main()

        def sign_up():
            
            username = un_entry_signup.get()
            password = pw_entry_signup.get()
            confirm  = pw_confirm_entry.get()

            if username == "Enter username" or username == "":
                messagebox.showinfo("Status", "Please enter username")
                return
            for i in username:
                if i == " ":
                    messagebox.showinfo("Status", "Username must contain no space character")
                    return

            if password == "Enter password" or password == "":
                messagebox.showinfo("Status", "Please enter password")
                return
            for i in password:
                if i == " ":
                    messagebox.showinfo("Status", "Password must contain no space character")
                    return

            if confirm == "Enter password again" or confirm == "":
                messagebox.showinfo("Status", "Please confirm password")
                return
            for i in confirm:
                if i == " ":
                    messagebox.showinfo("Status", "Password confirmation must contain no space character")
                    return
            if password != confirm:
                messagebox.showinfo("Status", "Confirmation does not match")
                return

            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            HOST = str(ip_addr)
            PORT = 1239

            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                cli.connect((HOST, PORT))
            except:
                messagebox.showinfo("Connection Lost", "Server has disconnected")
                return

            print("Connected to ('" + HOST + "', " + str(PORT) + ")")

            cli.sendall("Client".encode("utf8"))
            cli.recv(1024)

            req = "Sign up"
            cli.sendall(req.encode("utf8"))
            cli.recv(1024)

            cli.sendall(username.encode("utf8"))
            cli.recv(1024)

            cli.sendall(password.encode("utf8"))

            feedback = cli.recv(1024).decode("utf8")
            cli.sendall("Received Feedback".encode("utf8"))
            messagebox.showinfo("Status", feedback)

            cli.close()

        my_canvas.destroy()
        my_canvas_sign = Canvas(frame1, width = 1024, height = 640)
        my_canvas_sign.pack(fill = "both", expand = True)
        my_canvas_sign.create_text(x+90,y-50,text="Sign up", font=("Comic Sans MS",24,'bold'),fill="#400000")
        my_canvas_sign.create_text(x+25,y-10,text="Username:", font=("Verdana",11,'bold'),fill = txt_cl)
        my_canvas_sign.create_text(x+23,y+40,text="Password:", font=("Verdana",11,'bold'),fill = txt_cl)
        my_canvas_sign.create_text(x+56,y+90,text="Confirm password:", font=("Verdana",11,'bold'),fill = txt_cl)

        un_entry_signup = Entry(my_canvas_sign, font=("Courier New", 11),fg="black", bd=0)
        un_entry_signup.place(x=x-19, y=y,width=220,height=25)
        un_entry_signup.insert(0,"Enter username")

        pw_entry_signup = Entry(my_canvas_sign, font=("Courier New", 11),fg="black", bd=0)
        pw_entry_signup.place(x=x-19, y=y+50,width=195,height=25)
        pw_entry_signup.insert(0,"Enter password")

        pw_confirm_entry = Entry(my_canvas_sign, font=("Courier New", 11),fg="black", bd=0)
        pw_confirm_entry.insert(0,"Enter password again")
        pw_confirm_entry.place(x=x-19, y=y+100,width=195,height=25)

        def showPW_signup():
            global hide_show1
            hide_show1.destroy()
            hide_show1 = Button(my_canvas_sign, image=hide,bd=0,command=hidePW_signup)
            hide_show1.place(x=x+176,y=y+50,width=25,height=25)
            pw_entry_signup.config(show="")
        def hidePW_signup():
            global hide_show1
            hide_show1.destroy()
            hide_show1 = Button(my_canvas_sign, image=show,bd=0,command=showPW_signup)
            hide_show1.place(x=x+176,y=y+50,width=25,height=25,)
            pw_entry_signup.config(show="●")

        global hide_show1
        hide_show1 = Button(my_canvas_sign, image=show,bd=0, command=showPW_signup)
        hide_show1.place(x=x+176,y=y+50,width=25,height=25)

        def showPW_signupCF():
            global hide_show2
            hide_show2.destroy()
            hide_show2 = Button(my_canvas_sign, image=hide,bd=0,command=hidePW_signupCF)
            hide_show2.place(x=x+176,y=y+100,width=25,height=25)
            pw_confirm_entry.config(show="")
        def hidePW_signupCF():
            global hide_show2
            hide_show2.destroy()
            hide_show2 = Button(my_canvas_sign, image=show,bd=0,command=showPW_signupCF)
            hide_show2.place(x=x+176,y=y+100,width=25,height=25,)
            pw_confirm_entry.config(show="●")

        global hide_show2
        hide_show2 = Button(my_canvas_sign, image=show,bd=0, command=showPW_signupCF)
        hide_show2.place(x=x+176,y=y+100,width=25,height=25)
        
        un_entry_signup.bind("<FocusIn>", entry_clear_unsu)
        pw_entry_signup.bind("<FocusIn>", entry_clear_pwsu)
        pw_confirm_entry.bind("<FocusIn>", entry_clear_pwa)

        signup_btn2 = Button(my_canvas_sign, text="Sign up",font=("Fira", 16,'bold'), width=16,fg="#336d92",bd=4, command = sign_up)
        signup_btn2.place(x=x-20, y=y+140)
        back_login = Button(my_canvas_sign, text="Back to login",font=("Fira", 16,'bold'), width=16,fg="#336d92",bd=4, command = back)
        back_login.place(x=x-20, y=y+190)

    my_canvas = Canvas(frame1, width = 1024, height = 640)
    my_canvas.pack(fill = "both", expand = True)

    my_canvas.create_text(520,190,text="Client Login", font=("Comic Sans MS",24,'bold'),fill="#400000")
    my_canvas.create_text(x+25,y-10,text="Username:", font=("Verdana",11,'bold'),fill = txt_cl)
    my_canvas.create_text(x+23,y+40,text="Password:", font=("Verdana",11,'bold'),fill = txt_cl)

    un_entry = Entry(my_canvas, font=("Courier New", 11),fg="black", bd=0)
    un_entry.place(x=x-19, y=y,width=220,height=25)
    un_entry.insert(0,"Enter username")

    pw_entry = Entry(my_canvas, font=("Courier New", 11),fg="black", bd=0)
    pw_entry.place(x=x-19, y=y+50,width=195,height=25)
    pw_entry.insert(0,"Enter password")

    login_btn = Button(my_canvas, text="Login",font=("Fira", 16,'bold'), width=16,fg="#336d92",bd=5, command=after_login)
    login_btn.place(x=x-21, y=y+90)

    signup_btn1 = Button(my_canvas, text="Sign up",font=("Fira", 16,'bold'), width=16,fg="#336d92", bd=5,command=signup1)
    signup_btn1.place(x=x-21, y=y+140)

    global hide_show
    hide_show = Button(my_canvas, image=show,bd=0, command=showPW)
    hide_show.place(x=x+176,y=y+50,width=25,height=25)

    un_entry.bind("<FocusIn>", entry_clear_un)
    pw_entry.bind("<FocusIn>", entry_clear_pw)


EnterIP()
frame1.mainloop()