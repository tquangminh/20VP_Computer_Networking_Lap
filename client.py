import imp
from importlib.resources import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter.filedialog import askopenfile
import socket
import os,sys
import io
import tkinter as tk
from PIL import Image, ImageTk

window = Tk()
window.resizable(False, False) 
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
    
    can = Canvas(frame1, width = 610, height = 400)
    can.configure(background="#d78e8e")
    can.pack(fill = "both", expand = True)

    can.create_text(300,130,text="CONNECT TO SERVER", font=("Inter",30,'bold'),fill="#f8ecec")
    ip_entry = Entry(frame1, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
    ip_entry.place(x=190, y=230,width=250,height=25)
    ip_entry.insert(0,"Enter IP")
    ip_entry.bind("<FocusIn>", entry_clear_IP)
    
    
    
    
    
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

    ip_btn = Button(frame1, text="Connect",font=("Fira", 16,'bold'), width=16,fg="#d78e8e",bd=0,command=checkIP)
    ip_btn.place(x=204,y=300)

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
        hide_show.place(x = 270,y = 200,width=25,height=35)
        pw_entry.config(show="")
    def hidePW():
        global hide_show
        hide_show.destroy()
        hide_show = Button(my_canvas, image=show,bd=0,command=showPW)
        hide_show.place(x=270,y=200,width=25,height=35,)
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
                can_show = Canvas(frame1,
                    bg = "#ffffff",
                    height = 360,
                    width = 810,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge")
                
                background_img = PhotoImage(file = f"background.png")
                background = can_show.create_image(
                    405, 180,
                    image=background_img)


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
                    
                    my_canvas = Canvas(frame1,
                        bg = "#ffffff",
                        height = 360,
                        width = 810,
                        bd = 0,
                        highlightthickness = 0,
                        relief = "ridge")
                    
                    background_img = PhotoImage(file = f"background2.png")
                    background = my_canvas.create_image(
                        405, 180,
                        image=background_img)

                    my_canvas.pack(fill = "both", expand = True)

                    def textNote():
                        my_canvas.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360, bg = "#ffffff", 
                        bd = 0,
                        highlightthickness = 0,
                        relief = "ridge")

                        background = can_addTypeNote.create_image(
                        405, 180,
                        image=background_img)

                        can_addTypeNote.pack(fill = "both", expand = True)
                        def Submit():
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
                        def entry_clear_tittle(e):
                            if tittleBox.get() == "Enter title":
                                tittleBox.delete(0,END)
                        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 13),fg="black", bd=0)
                        tittleBox.insert(0,"Enter title")
                        tittleBox.bind("<FocusIn>", entry_clear_tittle)
                        tittleBox.place(x=105, y=20,width=600,height=50)
                    

                        text_box = Text()
                        text_box.place(x=105, y=130,width=600,height=150)
                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=Fira_Sans, borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=Submit) 
                        SubmitBtn.place(x=310, y=310, height=27, width=124)
                    
                    def imgNote():
                        my_canvas.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360, bg = "#ffffff", 
                        bd = 0,
                        highlightthickness = 0,
                        relief = "ridge")

                        background = can_addTypeNote.create_image(
                        405, 180,
                        image=background_img)

                        can_addTypeNote.pack(fill = "both", expand = True)

                        def Submit():
                            cli.sendall("Image".encode("utf8"))
                            cli.recv(1024)

                            tittle = tittleBox.get()
                            cli.sendall(tittle.encode("utf8"))
                            cli.recv(1024)

                            filename = filename2
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

                        def entry_clear_tittle(e):
                            if tittleBox.get() == "Enter title":
                                tittleBox.delete(0,END)
    
                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 13),fg="black", bd=0)
                        tittleBox.place(x=105, y=20,width=600,height=50)
                        tittleBox.insert(0,"Enter title")
                        tittleBox.bind("<FocusIn>", entry_clear_tittle)
                        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
                        def UploadAction(event=None): 
                            global filename2
                            filename2 = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpeg *.png *.jpg *.gif')])
                            print('Selected:', filename2)
                            pathDisplay = Label(can_addTypeNote,font = Fira_Sans, text = filename2,fg='#63cdda', bg = '#fff8ee')
                            pathDisplay.place(x = 220, y = 260)

                        
                        pathEntry = Button(can_addTypeNote, text='Select Image',font=Fira_Sans, borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=UploadAction)
                    
                        pathEntry.place(x=105, y=150,width=600,height=100)
                        


                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=Fira_Sans, borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=Submit)

                        SubmitBtn.place(x=343, y=310, height=27, width=124)       

                    def fileNote():
                        my_canvas.destroy()
                        can_addTypeNote = Canvas(frame1, width = 810, height = 360, bg = "#ffffff", 
                        bd = 0,
                        highlightthickness = 0,
                        relief = "ridge")

                        background = can_addTypeNote.create_image(
                        405, 180,
                        image=background_img)

                        can_addTypeNote.pack(fill = "both", expand = True)

                       

                        def Submit():
                            cli.sendall("File".encode("utf8"))
                            cli.recv(1024)

                            tittle = tittleBox.get()
                            cli.sendall(tittle.encode("utf8"))
                            cli.recv(1024)

                            filename = filename3
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
                            
                        def entry_clear_tittle(e):
                            if tittleBox.get() == "Enter title":
                                tittleBox.delete(0,END)
                        tittleBox = Entry(can_addTypeNote, font=("Courier New", 13),fg="black", bd=0)
                        tittleBox.place(x=105, y=20,width=600,height=50)
                        tittleBox.insert(0,"Enter title")
                        tittleBox.bind("<FocusIn>", entry_clear_tittle)

                        def UploadAction(event=None): 
                            global filename3
                            filename3 = filedialog.askopenfilename()
                            print('Selected:', filename3)
                            pathDisplay = Label(can_addTypeNote,font = Fira_Sans, text = filename3,fg='#63cdda', bg = '#fff8ee')
                            pathDisplay.place(x = 220, y = 260)



                       

                        pathEntry = Button(can_addTypeNote, text='Select File',font=Fira_Sans, borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=UploadAction)
                        pathEntry.place(x=105, y=150,width=600,height=100)

                       
                        SubmitBtn = Button(can_addTypeNote, text="Submit",font=Fira_Sans, borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=Submit) 
                        SubmitBtn.place(x=343, y=310, height=27, width=124)  
                       

                    def backAddNote():
                        my_canvas.destroy()
                        main2()
                

                    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
                    
                    #192.168.0.190
                   
                    textBtn = Button(my_canvas, text="Text",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=textNote)
                    textBtn.place(x=235, y=40, height=40, width=350)

                    imgBtn = Button(my_canvas, text="Image",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=imgNote)
                    imgBtn.place(x=235, y=120, height=40, width=350)

                    fileBtn = Button(my_canvas, text="File",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF",command=fileNote)
                    fileBtn.place(x=235, y=200, height=40, width=350)
                    
                    backBtn = Button(my_canvas, text="Back",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=backAddNote)
                    backBtn.place(x=235, y=280, height=40, width=350)

                    my_canvas.mainloop()

                def viewNote():
                    def backViewNote():
                        topicListBox.destroy()     
                        my_canvas.destroy()
                        cli.sendall('Back'.encode('utf8'))
                        main2()
                    def view():
                        def save():
                            global filename
                            if type == 'Text':
                                filename = "clientDisk/" + topicSelected + ".txt"
                            else: 
                                filename = "clientDisk/" + os.path.basename(filename)
                            with open(filename, "wb") as f:
                                f.write(content)
                        topicSelected = topicListBox.get(ANCHOR)
                        topicListBox.destroy()
                        my_canvas.destroy()
                        can_viewNote = Canvas(frame1, width = 700, height = 700)
                        can_viewNote.configure(background = "#d78e8e")
                        can_viewNote.pack(fill = "both", expand = False)
                        cli.sendall(topicSelected.encode("utf8"))
                        type = cli.recv(1024).decode("utf8")
                        cli.sendall("Received Type".encode("utf8"))
                        if type == 'Text': 
                            content = cli.recv(4096)
                        else: 
                            global filename
                            filename = cli.recv(1024).decode("utf8")
                            cli.sendall('Received File Name'.encode("utf8"))
                            filesize = cli.recv(1024)
                            filesize = int(filesize)
                            cli.sendall('Received File Size'.encode("utf8"))
                            content = cli.recv(filesize + 1024)

                        if type == 'Text': 
                            can_viewNote.create_text(520,190,text=content, font=("Comic Sans MS",24,'bold'),fill="#400000")
                        elif type == 'Image':
                            image = Image.open(io.BytesIO(content))
                            imageresize = resized = image.resize((500, 500),Image.ANTIALIAS)
                            img = ImageTk.PhotoImage(imageresize)
                            
                            panel = Label(can_viewNote, image = img, relief = GROOVE)
                         
                            panel.place(x = 100, y = 71, height = 500, width = 500)
                        else: 
                            can_viewNote.create_text(520,190,text=filename, font=("Comic Sans MS",24,'bold'),fill="#400000")
                        
                        saveBtn = Button(can_viewNote, text="Save",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=save)
                        saveBtn.place(x=400, y=616, height=40, width=200)
                        can_viewNote.mainloop()


                        
                            


                    can_show.destroy()
                    cli.sendall("View Note".encode("utf8"))
                    csvTopicList = cli.recv(1024).decode("utf8")
                    TopicList = map(str.strip, csvTopicList.split(','))
                    
                    my_canvas = Canvas(frame1,
                    bg = "#ffffff",
                    height = 360,
                    width = 810,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge")
                
                    background_img = PhotoImage(file = f"background2.png")
                    background = my_canvas.create_image(
                    405, 180,
                    image=background_img)
                    my_canvas.pack(fill = "both", expand = True) 

                    scrollbar = Scrollbar()
                    topicListBox = Listbox(yscrollcommand = scrollbar.set)
                    topicListBox.place(x=15, y=37, height=234, width=751)
                    
                    for i in TopicList:
                        topicListBox.insert(END, i)
                    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
                           
                    backBtn = Button(my_canvas, text="Back",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=backViewNote)
                    backBtn.place(x=15, y=297, height=40, width=350)

                    viewBtn = Button(my_canvas, text="View",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=view)
                    viewBtn.place(x=416, y=297, height=40, width=350)
                    my_canvas.mainloop()
                # tkFont.BOLD == 'bold'
                Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
                log_out1 = Button(can_show, text="LOG OUT",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=log_out)
                log_out1.place(x=235, y=200, height=40, width=350)

                exit_ = Button(can_show, text="EXIT",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=out)
                exit_.place(x=235, y=280, height=40, width=350)   

                addNoteBtn = Button(can_show, text="ADD NOTE",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF",command=addNote)
                addNoteBtn.place(x=235, y=40, height=40, width=350)
                #192.168.0.190
                viewNoteBtn = Button(can_show, text="VIEW NOTE",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command=viewNote)
                viewNoteBtn.place(x=235, y=120, height=40, width=350)
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

   
  

  
    
    my_canvas = Canvas(frame1, width = 362, height = 404)
    my_canvas.pack(expand = YES, fill = BOTH)
    my_canvas.configure(background = "#d78e8e")
    my_canvas.create_text(180,80,text="Client Login", font=("Inter",24,'bold'),fill="#303952")
    un_entry = Entry(my_canvas, font=("Montserrat", 13),fg="#303952",bg = "#ebc6c6", bd=0)
    un_entry.place(x=75, y=150,width=220,height=35)
    un_entry.insert(0,"Enter username")

    pw_entry = Entry(my_canvas, font=("Montserrat", 13),fg="#303952",bg = "#ebc6c6", bd=0)
    pw_entry.place(x=75, y=200,width=195,height=35)
    pw_entry.insert(0,"Enter password")

    login_btn = Button(my_canvas, text="Login",font=("Fira", 16,'bold'), width=17, fg="#d78e8e",bd=0, command=after_login)
    login_btn.place(x=70, y=260)
   

    signup_btn1 = Button(my_canvas, text="Sign up",font=("Fira", 16,'bold'), width=17,fg="#d78e8e", bd=0,command=signup1)
    signup_btn1.place(x=70, y=310)

    global hide_show
    hide_show = Button(my_canvas, image=show,bd=0, command=showPW)
    hide_show.place(x=270,y=200,width=25,height=35)

    un_entry.bind("<FocusIn>", entry_clear_un)
    pw_entry.bind("<FocusIn>", entry_clear_pw)
    


EnterIP()

frame1.mainloop()