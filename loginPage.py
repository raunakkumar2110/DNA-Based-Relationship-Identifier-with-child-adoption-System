#import tkinter as tk
from tkinter import*
from tkinter import messagebox
from PIL import ImageTk,Image  #pip
import mysql.connector;
from tkinter import ttk;
from PIL import Image,ImageTk;
import numpy as np;
import random
import textdistance;
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkhtmlview import HTMLLabel;
from tkcalendar import *;
from datetime import datetime;
from tkinter import font as tkFont

    
def login():
    global Username;
    global Password;
    global root;
    root = Tk()
    root.title("Login Page")
    root.geometry("1000x600+0+0")
    root.resizable(False, False)

    bgRoot="#03045e"
    bgVar="white"
    bgButton="#4ea8de"

    root.configure(background=bgRoot)

    conn = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match"); #connecting to the database
    c = conn.cursor() 
    c.execute("CREATE TABLE IF NOT EXISTS dnamatching(name_var TEXT not null,age_var INTEGER not null,marital_var TEXT not null,email_var TEXT not null,phone_var INTEGER not null,address_var TEXT,city_var TEXT not null,state_var TEXT not null,pin_var INTEGER not null,securityquestion_var TEXT not null,username_var TEXT not null primary key,password_var TEXT not null)")
    #login frame
    Frame_login = Frame(root)
    bg1=Label(Frame_login,bg=bgVar).place(x=0,y=0, relwidth=1, relheight=1)
    Frame_login.place(x=260, y=50,width=500,height=500)
    login_label = Label(Frame_login, text="Login", font=("times new roman", 20, "bold"), bg=bgVar, fg="black").place(x=0, y=20, relwidth=1, relheight=0.1)

    #Username
    lbl_use = Label(Frame_login, text="Username", font=("Goudy old style", 15, "bold"), fg="black", bg=bgVar).place(x=90,y=100)
    Username= Entry(Frame_login, font=("Goudy old style", 15,), bg="#E7E6E6")
    Username.place(x=90,y=130,width=320, height=35)

    #Password
    lbl_Password = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="black", bg=bgVar).place(x=90, y=170)
    Password = Entry(Frame_login, show='*',font=("Goudy old style", 15,), bg="#E7E6E6")
    Password.place(x=90, y=200, width=320, height=35)

    #forgot password
    forget_button= Button(Frame_login,  text="Forget password?", bd=0,cursor="hand2",font=("Goudy old style", 12), fg="red", bg=bgVar).place(x=90, y=240)

    #button
    submit_button = Button(Frame_login, cursor="hand2", text="Back", bd=0, font=("Goudy old style", 15), bg=bgButton,fg="white").place(x=80, y=300,width=100,height=40)
    login_button = Button(Frame_login,  cursor="hand2", text="login", bd=0, font=("Goudy old style", 15), bg=bgButton,fg="white",command=login_check).place(x=200, y=300,width=100,height=40)
    exit_button = Button(Frame_login, cursor="hand2", text="EXIT", bd=0, font=("Goudy old style", 15), bg=bgButton,fg="white").place(x=320, y=300,width=100,height=40)

    # #REGISTER
    Register = Button(Frame_login, cursor="hand2", text="Register", bd=0, font=("Goudy old style", 15,"bold"), bg=bgButton,fg="white").place(x=180, y=390,width=130,height=40)
    
    root.mainloop()
def login_check():
    global uname;
    global pwd;
    global d;
    #getting form data
    uname=Username.get()
    pwd=Password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        messagebox.showinfo("Error","Please fill all the fields")
    else:
        #open database
        conn = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        c=conn.cursor()
        #select query
        sql = ("SELECT * from dnamatching where username_var=%s and password_var=%s");
        val = (uname,pwd);
        c.execute(sql, val);
        result = c.fetchall()
        #fetch data 
        if result:
            mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
            mycur=mydb.cursor();
            mycur.execute("select name_var from dnamatching where  username_var ='" +uname+ "'");
            result = mycur.fetchone();
            b = list(result);
            d  = b[0]; #get user name for main dashboard;
            messagebox.showinfo("Success","Login Successful")
            dnaMatch();
        else:
            messagebox.showinfo("Error","Invalid Username or Password")
        #clear fields
        #Username.delete(0,END)
        #Password.delete(0,END)
        
        
        
def dna_check_database():
    com1 = Combo1.get()
    mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
    mycur=mydb.cursor();
    mycur.execute("select dnaSequence_var from dnamatching where  username_var ='" +uname+ "'");
    result = mycur.fetchone();
    v = list(result);
    n  = v[0];  #user_dna_sequence
    text1 = n;
    if com1 == "Persons are Twins":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching where  username_var != '" +uname+ "'");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            print(float(cal))
            if float(cal) ==100.0:
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text1+"' and username_var != '"+uname+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                tb1.delete("1.0","end")
                for x in range(len(nf)):
                    tb1.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb1.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb1.insert('3.0',"Relationship Status :- '"+com1+"'\n");
                    print("")
                break;
            else:
                tb1.delete("1.0","end")
                tb1.insert('1.0',"No Match Found In Database :- \n");
                
    elif com1 == "Parent and Child Relation":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching where  username_var != '" +uname+ "'");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal1 = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            print(float(cal1))
            if float(cal1) >= 50.0 and float(cal1) < 100.0:
                
                mydb1 = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor1 = mydb.cursor();
                mycursor1.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' and username_var != '"+uname+"'");
                result1 = mycursor1.fetchall();   #fetch in the form of list
                a1 = np.array(result1);
                namearr1 = a1.flatten();
                nf1 = list(namearr1)
                print(nf1)
                x1 =0
                tb1.delete("1.0","end")
                for x in range(len(nf1)):
                    tb1.insert('1.0',"Matched With :- '"+nf1[x]+"'\n");
                    tb1.insert('2.0',"Matched Percentage :- '"+str(cal1)+"'\n");
                    tb1.insert('3.0',"Relationship Status :- '"+com1+"'\n");
                break
            
            else:
                tb1.delete("1.0","end")
                tb1.insert('1.0',"No Match Found In Database :- \n");
                
    elif com1 == "Grandparent and Grandchild Relation":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching where  username_var != '" +uname+ "'");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;\
            print(float(cal))
            if(float(cal) >= 25.0 and float(cal) < 50.0):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' and username_var != '"+uname+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                tb1.delete("1.0","end")
                for x in range(len(nf)):
                    tb1.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb1.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb1.insert('3.0',"Relationship Status :- '"+com1+"'\n");
                break;
            else:
                tb1.delete("1.0","end")
                tb1.insert('1.0',"No Match Found In Database :- \n");
        
    elif com1 == "Uncle/Aunt and Niece/Nephew Relation":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching where  username_var != '" +uname+ "'");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            print(float(cal))
            if(float(cal) >= 12.5 and float(cal) < 25.0):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' and username_var != '"+uname+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                tb1.delete("1.0","end")
                for x in range(len(nf)):
                    tb1.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb1.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb1.insert('3.0',"Relationship Status :- '"+com1+"'\n");
                break;
            else:
                tb1.delete("1.0","end")
                tb1.insert('1.0',"No Match Found In Database :- \n");
    elif com1 == "Persons Are First Cousins":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching where  username_var != '" +uname+ "'");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            print(float(cal))
            if(float(cal) >= 6.25 and float(cal) < 12.5):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' and username_var != '"+uname+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                tb1.delete("1.0","end")
                for x in range(len(nf)):
                    tb1.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb1.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb1.insert('3.0',"Relationship Status :- '"+com1+"'\n");
                break;
            else:
                tb1.delete("1.0","end")
                tb1.insert('1.0',"No Match Found In Database :- \n");
    else:
        tb1.delete("1.0","end")
        tb1.insert('1.0',"No Match Found In Database :- \n");
        

    
            
def dnaMatch():
    global dnaDash;
    global Combo1;
    global tb1
    dnaDash = Tk();
    dnaDash.geometry("1000x600");
    dnaDash.title("Dashboard");
    Label(dnaDash,text = "Welcome To DNA Matching DashBoard",justify = "center",font = ("Times new roman",30,"bold"),fg = "Red",bg = "Black",width = 300).pack();
    bg = Image.open("dback.png").resize((1000,900));
    img = ImageTk.PhotoImage(bg,master = dnaDash);
    lbl = Label(dnaDash,image = img).pack(pady = 0.5 );
    m = Menu(dnaDash);
    m1 = Menu(m,tearoff = 0);
    m.add_cascade(label = "File",menu = m1);
    m1.add_command(label = "DNA Matching (ADV)",command = dna_match_dash1);
    dnaDash.config(menu = m);
    """marlb = HTMLLabel(dnaMatch,html = "<marquee>Welcome User</marquee>");
    marlb.place(x = 60,y = 650);""" #not working with html tags
    wu = Label(dnaDash,text = "Welcome User '"+d+"'",font = ("Times new roman",12,"bold"),bg = "Black",fg = "red").place(x = 10,y =570);
    optlist1 = ["Persons are Twins","Parent and Child Relation","Grandparent and Grandchild Relation","Uncle/Aunt and Niece/Nephew Relation","Persons Are First Cousins"];
    Combo1 = ttk.Combobox(dnaDash,values = optlist1,width = 48,font = ("Times New Roman",12,"bold"));
    Combo1.set("Select Relationship - ");
    Combo1.place(x = 150,y = 90);
    label1 = Label(dnaDash,text = "Click On The Button to Check Paternity Status\n\n⬇",font = ("Times new roman",18,"bold"),bg = "black",fg = "Green").place(x = 110,y =130);
    tb1 = Text(dnaDash, height = 10,width = 60,bg = "light cyan")
    tb1.insert('1.0',"Matched With :- \n");
    tb1.insert('2.0',"Matched Percentage :- \n");
    tb1.insert('3.0',"Relationship Status :- ");
    tb1.place(x = 110,y = 300);
    matchButt = Button(dnaDash,text = "Start Checking",font = ("Times new roman",15,"bold"),fg = "red",bg = "black",width = 20,command = dna_check_database).place(x =230,y = 225);
    clearButt = Button(dnaDash,text = "Clear",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 10).place(x = 75 ,y = 500);
    exitButt =  Button(dnaDash, text = "Exit",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",command = dnaDash.destroy,width = 10).place(x =225,y = 500);
    casButt =  Button(dnaDash, text = "Child Adoption System",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",command =  ch_ad_sys,width = 20).place(x =375,y = 500);
    dnaDash.mainloop();


def ch_ad_sys():
    global cas;
    global Combo2;
    bgVar="black"
    cas = Tk();
    cas.geometry("1200x600");
    cas.title("CAS")
    Label(cas,text = "Welcome To Child Adoption System",justify = "center",font = ("Times new roman",30,"bold"),fg = "Red",bg = "Black",width = 300).pack();
    bg = Image.open("cas1.png").resize((1200,600));
    img = ImageTk.PhotoImage(bg,master = cas);
    lbl = Label(cas,image = img).pack(pady = 0.5 );
    shbt = Button(cas,text = "Show Childrens",font = ("Times new roman",15,"bold"),fg = "red",bg = "Black",width = 20,command =sh_children).place(x =233,y = 475);
    clrButt = Button(cas,text = "Clear",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 15).place(x = 542 ,y = 475);
    eButt =  Button(cas, text = "Exit",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",command = cas.destroy,width = 15).place(x = 794,y = 475);
    adopt= Button(cas,  text="Want to Adopt Any Children ?", bd=0,cursor="hand2",font=("Goudy old style", 15), fg="red", bg=bgVar,command = want_to_a_ch).place(x=480, y=390)
    ol = ["orgA_Punjab","orgB_Delhi"];
    Combo2 = ttk.Combobox(cas,values = ol,width = 48,font = ("Times New Roman",12,"bold"));
    Combo2.set("Select Organization - ");
    Combo2.place(x = 385,y = 90);
    
    
    
    
    
    
    
    cas.mainloop();



def want_to_a_ch():
    global Combo3;
    global Combo4;
    global wtac;
    wtac = Tk();
    global e1;
    global e2;
    wtac.geometry("700x400");
    wtac.title("Eligibility Form");
    Label(wtac,text = "Eligibility Check",justify = "center",font = ("Times new roman",23,"bold"),fg = "Red",bg = "Black",width = 300).pack();
    bg = Image.open("cas1.png").resize((1000,400));
    img = ImageTk.PhotoImage(bg,master = wtac);
    lbl = Label(wtac,image = img).pack(pady = 0.5 );
    oplist = ["orgA_Punjab","orgB_Delhi"];
    Combo3 = ttk.Combobox(wtac,values = oplist,width = 59,font = ("Times New Roman",12,"bold"));
    Combo3.set("Select Organization - ");
    Combo3.place(x = 42,y = 70);
    enlb = Label(wtac,text = "Enter Child ID - ",font = ("arial",16,"bold"),bg = "Black",fg = "red").place(x = 40,y =130);
    e1 = Entry(wtac,width = 35,borderwidth = 1,font = ("Times New Roman",12),highlightthickness=2);
    e1.config(highlightbackground = "green", highlightcolor= "green");
    e1.place(x = 250,y = 130);
    enlb1 = Label(wtac,text = "Adopt Child as - ",font = ("arial",16,"bold"),bg = "Black",fg = "red").place(x = 40,y =180);
    olist = ["Prospective adoptive parents (couple)","Single prospective adoptive parent"];
    Combo4 = ttk.Combobox(wtac,values = olist,width = 33,font = ("Times New Roman",12,"bold"));
    Combo4.set("Choose Category - ");
    Combo4.place(x = 250,y = 180);
    enlb2 = Label(wtac,text = "Enter Age - ",font = ("arial",16,"bold"),bg = "Black",fg = "red").place(x = 40,y =230);
    e2 = Entry(wtac,width = 35,borderwidth = 1,font = ("Times New Roman",12),highlightthickness=2);
    e2.config(highlightbackground = "green", highlightcolor= "green");
    e2.place(x = 250,y = 230);
    cheButt = Button(wtac,text = "Check",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 10,command = check_elig).place(x = 20,y = 340);
    cButt = Button(wtac,text = "Clear",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 10).place(x = 170 ,y = 340);
    backButt = Button(wtac,text = "Back",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 10,command = ch_ad_sys).place(x = 320 ,y = 340);
    exiButt =  Button(wtac, text = "Exit",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",command = wtac.destroy,width = 10).place(x = 465,y = 340);
    
    
    
    wtac.mainloop();

def check_elig():
    global c3;
    c3 = Combo3.get();
    c4 = Combo4.get();
    ent1 = e1.get();
    ent2 = e2.get();
    if c3 == "orgA_Punjab":
        c3 = "orgA_Punjab";
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select Age from  orgA_Punjab where  Child_UID = '"+str(ent1)+"' ");
        res = mycur.fetchall();
        val = list(res);
        fval  = val[0];
        s = sum(fval)
        if 4 == "Prospective adoptive parents (couple)" and int(ent2) <= 90:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 4 and s <= 8 and c4 == "Prospective adoptive parents (couple)" and int(ent2) <= 100:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 8 and s <= 18 and c4 == "Prospective adoptive parents (couple)" and int(ent2) <= 110:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 0 and s <= 4 and c4 == "Single prospective adoptive parent" and int(ent2) <= 45:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 4 and s <= 8 and c4 == "Single prospective adoptive parent" and int(ent2) <= 50:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 8 and s <= 18 and c4 == "Single prospective adoptive parent" and int(ent2) <= 55:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        else:
            messagebox.showinfo("","Sorry !! You are not eligible");
    elif c3 == "orgB_Delhi":
        c3 = "orgB_Delhi";
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select Age from  orgB_Delhi where  Child_UID = '"+str(ent1)+"' ");
        res = mycur.fetchall();
        val = list(res);
        fval  = val[0];
        s = sum(fval)
        if s > 0 and s <= 4 and c4 == "Prospective adoptive parents (couple)" and int(ent2) <= 90:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 4 and s <= 8 and c4 == "Prospective adoptive parents (couple)" and int(ent2) <= 100:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 8 and s <= 18 and c4 == "Prospective adoptive parents (couple)" and int(ent2) <= 110:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 0 and s <= 4 and c4 == "Single prospective adoptive parent" and int(ent2) <= 45:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 4 and s <= 8 and c4 == "Single prospective adoptive parent" and int(ent2) <= 50:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        elif s > 8 and s <= 18 and c4 == "Single prospective adoptive parent" and int(ent2) <= 55:
            messagebox.showinfo("","Congratulations!! You are eligible");
            MsgBox = messagebox.askquestion ('Confirmation','Do u want to Book the Slot to visit The organisation for further investigation')
            if MsgBox == 'yes':
                wtac.destroy()
                calendar();
        else:
            messagebox.showinfo("","Sorry !! You are not eligible");
    else:
        messagebox.showinfo("Kindly choose the Options correctly!!");
    
def bookslot():
    et = enty1.get()
    mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "sih_dna_match");
    mycur = mydb.cursor();
    mycur.execute("CREATE TABLE IF NOT EXISTS Booked_Slot(Name varchar(40),Date date,Organization varchar(30))");
    val= [(d,et,c3)];
    sql="INSERT INTO Booked_slot(Name,Date,Organization)VALUES (%s,%s,%s)";
    mycur.executemany(sql,val);
    mydb.commit();
    messagebox.showinfo("","You have successfully booked the slot Kindly Visit accordingly and keeping Covid regulations in mind , Thank you ");
    

def calendar():
    global calen;
    global mlb;
    global enty1;
    bgVar = "black"
    global str_dt;
    calen = Tk();
    calen.title("Slot Booking");
    calen.geometry("320x300")
    bg = Image.open("cas1.png").resize((320,300));
    img = ImageTk.PhotoImage(bg,master = calen);
    lbl = Label(calen,image = img).pack(pady = 0.5 );
    cal = Calendar(calen,selectmode = "day",year = 2020,month = 5,day = 22);
    cal.place(x = 20,y = 10)
    #dt=cal.get_date()
    #str_dt=dt.strftime("%Y-%m-%d");
    bslotbtn= Button(calen,  text="Book Slot", bd=0,cursor="hand2",font=("Goudy old style", 12), fg="red", bg=bgVar,command = bookslot).place(x = 100,y =250)
    enty1 = Entry(calen,width = 30,borderwidth = 1,font = ("Times New Roman",12),highlightthickness=2);
    enty1.config(highlightbackground = "green", highlightcolor= "green");
    enty1.insert(0,"(YYYY-MM-DD)");
    enty1.place(x = 22,y = 220);
    
    
    
    
    
    
    calen.mainloop();
    













def sh_children():
    c2 = Combo2.get();
    if c2 == "orgA_Punjab":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_MATCH");
        mycur = mydb.cursor();
        mycur.execute("SELECT * FROM orgA_Punjab ");
        tree = ttk.Treeview(cas);
        tree["show"] = "headings";
        s = ttk.Style(cas);
        s.configure(".",font = ("Helvetica",9));
        s.configure("Treeview.Heading",foreground = "Red",font = ("Helvetica",9,"bold"));
        tree["columns"] = ("Child_UID" ,"Name" ,"Age" ,"Facial_Complextion" ,"Address" ,"Height" ,"Weight","Language","DOB","Edu_Qual");
        tree.column("Child_UID",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("Name",width = 80,minwidth = 50,anchor = CENTER);
        tree.column("Age",width = 50,minwidth = 50,anchor = CENTER);
        tree.column("Facial_Complextion",width = 130,minwidth = 50,anchor = CENTER);
        tree.column("Address",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("Height",width = 40,minwidth = 50,anchor = CENTER);
        tree.column("Weight",width = 40,minwidth = 50,anchor = CENTER);
        tree.column("Language",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("DOB",width = 100,minwidth = 50,anchor = CENTER);
        tree.column("Edu_Qual",width = 100,minwidth = 50,anchor = CENTER);
    
        tree.heading("Child_UID",text = "Child_UID",anchor = CENTER);
        tree.heading("Name",text = "Name",anchor = CENTER);
        tree.heading("Age",text = "Age",anchor = CENTER);
        tree.heading("Facial_Complextion",text = "Facial_Complextion",anchor = CENTER);
        tree.heading("Address",text = "Address",anchor = CENTER);
        tree.heading("Height",text = "Height",anchor = CENTER);
        tree.heading("Weight",text = "Weight",anchor = CENTER);
        tree.heading("Language",text = "Language",anchor = CENTER);
        tree.heading("DOB",text = "DOB",anchor = CENTER);
        tree.heading("Edu_Qual",text = "Edu_Qual",anchor = CENTER);
        i = 0;
        for row in mycur:
            tree.insert("", i, text="Hii",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags=("even",));
            i = i+1;
        
        tree.place(x = 230,y =150);
    elif c2 == "orgB_Delhi":
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_MATCH");
        mycur = mydb.cursor();
        mycur.execute("SELECT * FROM orgB_Delhi ");
        tree = ttk.Treeview(cas);
        tree["show"] = "headings";
        s = ttk.Style(cas);
        s.configure(".",font = ("Helvetica",9));
        s.configure("Treeview.Heading",foreground = "Red",font = ("Helvetica",9,"bold"));
        tree["columns"] = ("Child_UID" ,"Name" ,"Age" ,"Facial_Complextion" ,"Address" ,"Height" ,"Weight","Language","DOB","Edu_Qual");
        tree.column("Child_UID",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("Name",width = 80,minwidth = 50,anchor = CENTER);
        tree.column("Age",width = 50,minwidth = 50,anchor = CENTER);
        tree.column("Facial_Complextion",width = 130,minwidth = 50,anchor = CENTER);
        tree.column("Address",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("Height",width = 40,minwidth = 50,anchor = CENTER);
        tree.column("Weight",width = 40,minwidth = 50,anchor = CENTER);
        tree.column("Language",width = 70,minwidth = 50,anchor = CENTER);
        tree.column("DOB",width = 100,minwidth = 50,anchor = CENTER);
        tree.column("Edu_Qual",width = 100,minwidth = 50,anchor = CENTER);
    
        tree.heading("Child_UID",text = "Child_UID",anchor = CENTER);
        tree.heading("Name",text = "Name",anchor = CENTER);
        tree.heading("Age",text = "Age",anchor = CENTER);
        tree.heading("Facial_Complextion",text = "Facial_Complextion",anchor = CENTER);
        tree.heading("Address",text = "Address",anchor = CENTER);
        tree.heading("Height",text = "Height",anchor = CENTER);
        tree.heading("Weight",text = "Weight",anchor = CENTER);
        tree.heading("Language",text = "Language",anchor = CENTER);
        tree.heading("DOB",text = "DOB",anchor = CENTER);
        tree.heading("Edu_Qual",text = "Edu_Qual",anchor = CENTER);
        i = 0;
        for row in mycur:
            tree.insert("", i, text="Hii",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags=("even",));
            i = i+1;
        
        tree.place(x = 230,y =150);
    else:
        messagebox.showinfo("","Details Not Found !! Please Select Appropiate Option");


def dna_match_dash1():
    global dnaDash1;
    global entry_1;
    global tb2;
    dnaDash1 = Tk();
    dnaDash1.geometry("1000x600");
    dnaDash1.title("DNA Dashboard");
    Label(dnaDash1,text = "DNA Matching DashBoard",justify = "center",font = ("Times new roman",30,"bold"),fg = "Red",bg = "Black",width = 300).pack();
    bg = Image.open("dback.png").resize((1000,900));
    img = ImageTk.PhotoImage(bg,master = dnaDash1);
    lbl = Label(dnaDash1,image = img).pack(pady = 0.5 );
    label1 = Label(dnaDash1,text = "Click On The Button to Check Paternity Status\n\n⬇",font = ("Times new roman",18,"bold"),bg = "Black",fg = "Green").place(x = 110,y =130);
    tb2 = Text(dnaDash1, height = 10,width = 60,bg = "light cyan")
    tb2.insert('1.0',"Matched With :- \n");
    tb2.insert('2.0',"Matched Percentage :- \n");
    tb2.insert('3.0',"Relationship Status :- ");
    tb2.place(x = 110,y = 300);
    label2 = Label(dnaDash1,text = "Enter DNA Sequence - ",font = ("Times new roman",16,"bold"),bg = "Black",fg = "Green").place(x = 110,y = 80);
    entry_1 = Entry(dnaDash1,width = 30,borderwidth = 1,font = ("Times New Roman",12),highlightthickness=2);
    entry_1.config(highlightbackground = "green", highlightcolor= "green");
    entry_1.place(x =344,y = 80)
    matchButt = Button(dnaDash1,text = "Start Checking",font = ("Times new roman",15,"bold"),fg = "Green",bg = "Black",width = 20,command = dna_check1).place(x =230,y = 225);
    clearButt = Button(dnaDash1,text = "Clear",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",width = 10).place(x = 188 ,y = 500);
    exitButt =  Button(dnaDash1, text = "Exit",font = ("Times new roman",15,"bold"),fg = "Red",bg = "Black",command = dnaDash1.destroy,width = 10).place(x = 385,y = 500);
    dnaDash1.mainloop();


def dna_check1():
    etr = entry_1.get();
    text1 = etr;
    if(etr != ""):
        mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match");
        mycur=mydb.cursor();
        mycur.execute("select dnaSequence_var from dnamatching ");
        result = mycur.fetchall();
        a = np.array(result);           #2d array
        ds = a.flatten();
        #print(ds)
        i=0;
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            #print(float(cal))
            if float(cal) ==100.0:
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text1+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                tb2.delete("1.0","end")
                for x in range(len(nf)):
                    tb2.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb2.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb2.insert('3.0',"Relationship Status :- Persons are Twins\n");
                    
                break;
            
        i = 0
        for i in range(len(ds)):
            text2 = ds[i];
            cal1 = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            #print(float(cal1))
            if float(cal1) >= 50.0 and float(cal1) < 100.0:
                mydb1 = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor1 = mydb.cursor();
                mycursor1.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"'");
                result1 = mycursor1.fetchall();   #fetch in the form of list
                a1 = np.array(result1);
                namearr1 = a1.flatten();
                nf = list(namearr1)
                print(nf)
                x =0
                for x in range(len(nf)):
                    tb2.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb2.insert('2.0',"Matched Percentage :- '"+str(cal1)+"'\n");
                    tb2.insert('3.0',"Relationship Status :- Parent and Child Relation\n");
                break
            
           
        i = 0
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;\
            #print(float(cal))
            if(float(cal) >= 25.0 and float(cal) < 50.0):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' ");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                
                for x in range(len(nf)):
                    tb2.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb2.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb2.insert('3.0',"Relationship Status :- Grandparent and Grandchild Relation\n");
                break;
           
        i = 0
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
           # print(float(cal))
            if(float(cal) >= 12.5 and float(cal) < 25.0):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"'");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                
                for x in range(len(nf)):
                    tb2.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb2.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb2.insert('3.0',"Relationship Status :- Uncle/Aunt and Niece/Nephew Relation\n");
                break;
           
        i = 0
        for i in range(len(ds)):
            text2 = ds[i];
            cal = textdistance.levenshtein.normalized_similarity(text1,text2)*100;
            #print(float(cal))
            if(float(cal) >= 6.25 and float(cal) < 12.5):
                mydb = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = "SIH_DNA_Match");
                mycursor = mydb.cursor();
                mycursor.execute("select name_var from dnamatching where dnaSequence_var = '"+text2+"' ");
                result = mycursor.fetchall();   #fetch in the form of list
                a = np.array(result);
                namearr = a.flatten();
                nf = list(namearr)
                print(nf)
                x =0
                
                for x in range(len(nf)):
                    tb2.insert('1.0',"Matched With :- '"+nf[x]+"'\n");
                    tb2.insert('2.0',"Matched Percentage :- '"+str(cal)+"'\n");
                    tb2.insert('3.0',"Relationship Status :-Persons Are First Cousins\n");
                break;
            
    else:
        tb2.delete("1.0","end")
        tb2.insert('1.0',"No Match Found In Database :- \n");              
    
    
    
    
        
            
        
       
            
            
        











#dnaMatch()
login()
#dna_check_database()
#ch_ad_sys()
#want_to_a_ch()
#calendar()
#dna_match_dash1()
