from logging import root
from textwrap import fill
import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import font as tkFont
import mysql.connector;
from PIL import ImageTk, Image


root = tk.Tk()
root.title("Registration Form")
root.geometry("1000x600+0+0")
root.resizable(False, False)

root.configure(background='lightblue')
# root.call('wm', 'attributes', '.', '-topmost', True)


conn = mysql.connector.connect(host = "localhost",user = "root",password = "admin",database = " SIH_DNA_Match"); #connecting to the database
c = conn.cursor() 

c.execute("CREATE TABLE IF NOT EXISTS dnamatching(name_var TEXT not null,dnaSequence_var TEXT not null,gender_var TEXT not null,age_var INTEGER not null,marital_var TEXT not null,email_var TEXT not null,phone_var INTEGER not null,address_var TEXT,city_var TEXT not null,state_var TEXT not null,pin_var INTEGER not null,securityquestion_var TEXT not null,username_var TEXT not null,password_var TEXT not null)")

def register():

    name = name_var.get()
    dnaSequence = dnaSequence_var.get()
    gender = gender_var.get()
    age = age_var.get()
    marital = maritelStatusVar.get()
    email = email_var.get()
    phone = phone_var.get()
    address = address_var.get()
    city = city_var.get()
    state = state_var.get()
    pin = pinCode_var.get()
    securityquestion= securityQuestion_var.get()
    username = username_var.get()
    password = password_var.get()
    confirm_password= confirm_password_var.get()

    if name != '' and gender_var != '' and age != '' and marital != '' and phone != '' and address != '' and city != '' and state != '' and pin != '' and securityquestion != '' and username != '' and password != '' and confirm_password != '':
        if password == confirm_password:
            val= [(name,dnaSequence,gender,age,marital,email,phone,address,city,state,pin,securityquestion,username,password)];
            sql="INSERT INTO dnamatching(name_var,dnaSequence_var,gender_var,age_var,marital_var,email_var,phone_var,address_var,city_var,state_var,pin_var,securityquestion_var,username_var,password_var)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            c.executemany(sql,val);
            conn.commit();
            messagebox.showinfo("Registration Successful","You have successfully registered");
            root.destroy();
        else:
            messagebox.showinfo("Error","Password and Confirm Password not matched")
            
    else:
        messagebox.showinfo("Error","All fields are required")

def login():
    root.destroy()
    import loginPage

def uploadProfile():
    f_types = [('Jpg Files', '*.jpg'),
    ('PNG Files','*.png')]   # type of files to select 
    filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
    col=1 # start from column 1
    row=7 # start from row 3 
    for f in filename:
        img=Image.open(f) # read the image file
        img=img.resize((100,100)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =tk.Label(root)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
        if(col==3): # start new line after third column
            row=row+1# start wtih next row
            col=1    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column 


text_var = tk.StringVar()
user_id = tk.StringVar()
name_var = tk.StringVar()
dnaSequence_var = tk.StringVar()
gender_var = tk.StringVar()
age_var = tk.StringVar()
maritelStatusVar = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
address_var = tk.StringVar()
city_var = tk.StringVar()
state_var = tk.StringVar()
pinCode_var = tk.StringVar()
securityQuestion_var = tk.StringVar()
username_var = tk.StringVar()
password_var = tk.StringVar()
confirm_password_var = tk.StringVar()
profileImage_var = tk.StringVar()

input1 = tk.Label(root, text="Registration Form", font=("times new roman", 30, "bold"), background="lightblue", foreground="black",)
input1.grid(row=0, column=1, columnspan=9, padx=20)

name_label = tk.Label(root, text="Name", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
name_label.grid(row=1, column=0, padx=(150,10), pady=10,sticky='w')

name_var = tk.Entry(root, textvariable=name_var, width=30)
name_var.grid(row=1, column=1, padx=(5,5), pady=20,sticky='w')

email_label = tk.Label(root, text="Email", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
email_label.grid(row=1, column=2, padx=10, pady=10,sticky='w')

email_var = tk.Entry(root, textvariable=email_var, width=30)
email_var.grid(row=1, column=3, padx=20, pady=20,sticky='w')

phone_label = tk.Label(root, text="Phone", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
phone_label.grid(row=2, column=0, padx=(150,10), pady=10,sticky='w')

phone_var = tk.Entry(root, textvariable=phone_var, width=30)
phone_var.grid(row=2, column=1, padx=(5,5), pady=20,sticky='w')

maritelStatus_label = tk.Label(root, text="Marital Status", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
maritelStatus_label.grid(row=2, column=2, padx=10, pady=10,sticky='w')

maritelStatusVar = ttk.Combobox(root, textvariable=maritelStatusVar, width=20)
maritelStatusVar['values'] = ("Single", "Married", "Divorced", "Widowed")
maritelStatusVar.grid(row=2, column=3, padx=20, pady=20,sticky='w')

Address_label = tk.Label(root, text="Address", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
Address_label.grid(row=3, column=0, padx=(150,10), pady=10,sticky='w')

address_var = tk.Entry(root, textvariable=address_var, width=30)
address_var.grid(row=3, column=1, padx=(5,5), pady=20,sticky='w')

city_label = tk.Label(root, text="City", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
city_label.grid(row=3, column=2, padx=10, pady=10,sticky='w')

city_var = tk.Entry(root, textvariable=city_var, width=30)
city_var.grid(row=3, column=3, padx=20, pady=20,sticky='w')

state_label = tk.Label(root, text="State", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
state_label.grid(row=4, column=0, padx=(150,10), pady=10,sticky='w')

state_var = ttk.Combobox(root, textvariable=state_var, width=20)
state_var['values'] = ("Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal")
state_var.grid(row=4, column=1, padx=(5,5), pady=20,sticky='w')

pinCode_label = tk.Label(root, text="Pin Code", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
pinCode_label.grid(row=4, column=2, padx=10, pady=10,sticky='w')

pinCode_var = tk.Entry(root, textvariable=pinCode_var, width=20)
pinCode_var.grid(row=4, column=3, padx=20, pady=20,sticky='w')

username_label = tk.Label(root, text="Username", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
username_label.grid(row=5, column=0, padx=(150,10), pady=10,sticky='w')

username_var = tk.Entry(root, textvariable=username_var, width=30)
username_var.grid(row=5, column=1, padx=(5,5), pady=20,sticky='w')

securityQuestion_label = tk.Label(root, text="Security Question", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
securityQuestion_label.grid(row=5, column=2, padx=10, pady=10,sticky='w')

securityQuestion_var = tk.Entry(root, textvariable=securityQuestion_var, width=30)
securityQuestion_var.grid(row=5, column=3, padx=20, pady=20,sticky='w')

password_label = tk.Label(root, text="Password", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
password_label.grid(row=6, column=0, padx=(150,10), pady=10,sticky='w')

pinCode_var = tk.Entry(root, textvariable=password_var,show="*", width=30)
pinCode_var.grid(row=6, column=1, padx=(5,5), pady=20,sticky='w')

confirm_password_label = tk.Label(root, text="Confirm Password", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
confirm_password_label.grid(row=6, column=2, padx=10, pady=10,sticky='w')

confirm_password_var = tk.Entry(root, textvariable=confirm_password_var,show="*", width=30)
confirm_password_var.grid(row=6, column=3, padx=20, pady=20,sticky='w')

age_label = tk.Label(root, text="Age", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
age_label.grid(row=7, column=0, padx=(150,10), pady=10,sticky='w')

age_var = tk.Entry(root, textvariable=age_var, width=10)
age_var.grid(row=7, column=1, padx=(5,5), pady=20,sticky='w')

dnaSequence_label = tk.Label(root, text="DNA Sequence", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
dnaSequence_label.grid(row=7, column=2, padx=10, pady=10,sticky='w')

dnaSequence_var = tk.Entry(root, textvariable=dnaSequence_var, width=30)
dnaSequence_var.grid(row=7, column=3, padx=20, pady=20,sticky='w')

gender_label = tk.Label(root, text="Gender", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
gender_label.grid(row=8, column=0, padx=(150,10), pady=10,sticky='w')

gender_var = ttk.Combobox(root, textvariable=age_var, width=20)
gender_var['values'] = ("Male", "Female", "Transgender")
gender_var.grid(row=8, column=1, padx=(5,5), pady=20,sticky='w')


profileImage_label = tk.Label(root, text="Profile Image", font=("times new roman", 15, "bold"), background="lightblue", foreground="black",)
profileImage_label.grid(row=8, column=2, padx=10, pady=10,sticky='w')

profileImage_button = tk.Button(root, text="Browse", command=lambda:uploadProfile(), width=10)
profileImage_button.grid(row=8, column=3,padx=20, pady=20,sticky='w')

helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)

register_button = tk.Button(root, text="Register",width="10", font=helv36,bg="black",foreground="white", command=register)
register_button.grid(row=9, column=2, padx=(5,5), pady=5,columnspan=2,sticky='w')

# cancel_button = tk.Button(root, text="Cancel",font=helv36,command=root.destroy)
# cancel_button.grid(row=9, column=3, padx=20, pady=5,sticky='w')

login_button = tk.Button(root, text="Login",font=helv36,bg="black",foreground="white", command=login)
login_button.grid(row=9, column=3, padx=20, pady=5,sticky='w')


root.mainloop()