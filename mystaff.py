import ldap
import ldap.modlist as modlist
import sys
from  Tkinter import *
import ttk
import tkMessageBox

class Guiform:
    def __init__(self,master):
         self.master = master
         master.title("Login Form")


         self.password = StringVar()
         self.username =  StringVar()
         self.portokali = "Portokali"
         self.frame = Frame(self.master)
         self.result_set = []
         self.real_value = tuple(self.result_set)
         self.frame.pack()


         self.UsernameBox = Label (self.frame, text = "user name")
         self.Text_UsernameBox = Entry( self.frame, textvariable = self.username)

         self.PasswordBox = Label (self.frame, text = "password")
         self.Text_PasswordBox = Entry( self.frame, textvariable = self.password, show = "*")
         self.Submit = Button(self.frame, text = "Submit", command = self.identity_check)
         self.Close = Button(self.frame, text=" Close", command = master.quit)

         self.UsernameBox.grid(row=0,sticky=W)
         self.Text_UsernameBox.grid(row = 0, column=2,sticky=E )
         self.PasswordBox.grid(row=1,sticky=W)
         self.Text_PasswordBox.grid(row = 1, column=2,sticky=E )
         self.Submit.grid(row=2, column =1)
         self.Close.grid(row=2,column=2)

    # def show(self):
    #      u = self.username.get()
    #      p = self.password.get()
    #      print "username is %s" % u
    #      print  " password is %s " % p

    def new_window(self):
        # self.newWindow = Toplevel(self.master)
        # self.my_gui = Mainwindows(self.newWindow)
        #root.withdraw()
        self.frame.destroy()
        Mainwindows(parent=root)



    def identity_check(self):
        user =  "uid=%s,ou=People,dc=itcurious,dc=com" % self.username.get()
        passw = self.password.get()
        l = ldap.initialize('ldap://40.69.81.8')
        try:
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s(user, passw)
        except ldap.INVALID_CREDENTIALS:
            print "Your username or password are incorrect"
            sys.exit(0)
        try:
            base_dn = "ou=People,dc=itcurious,dc=com"
            attr = ['uid']
            filter = '(uid= %s)' % self.username.get()
                # print filter
                # valid = True
                # print "Till now is ok"
            result = l.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attr)

            if result == []:
                print "Ypu are not authorized. Please ask for permissions! "
            else:
                self.new_window()

                #print "Welcome. Please continue !"
                    # valid = True
            # print "Till now is ok"
        except Exception, error:
            print error


class Mainwindows:
    def __init__(self,parent):
        self.parent = parent
        #Guiform.__init__(self)
        #Toplevel.__init__(self)
        self.frame = Frame(parent)
        # self.frame.geometry("670x600+50+50")



        self.menubar = Frame(parent, relief=RAISED, borderwidth=1)
        self.menubar.grid(row=0,column=0)
        mb_users = Menubutton(self.menubar, text='Users')
        mb_users.grid(row = 0, column = 0)
        mb_users.menu = Menu(mb_users)
        mb_users.menu.add_command(label='Create New User', command = self.add_new_user)
        mb_users.menu.add_command(label='Delete Existing User')

        mb_groups = Menubutton(self.menubar, text='Groups')
        mb_groups.grid(row=0, column=2)
        mb_groups.menu = Menu(mb_groups)
        mb_groups.menu.add_command(label='Create New Group' )
        mb_groups.menu.add_command(label='Modify Existing Group')
        mb_groups.menu.add_command(label='Delete Existing Group')

        # mb_help = Menubutton(menubar, text='help')
        # mb_help.pack(padx=25, side=RIGHT)

        mb_users['menu'] = mb_users.menu
        mb_groups['menu'] = mb_groups.menu

    def add_new_user(self):
        AddUser()

class ldapi:
    import re
    def __init__(self):
        self.real_value = None
        self.ldap_server = ldap.initialize('ldap://40.69.81.8')
        self.bind_username = "uid=john,ou=People,dc=itcurious,dc=com"
        self.bind_password = "johnldap"
        self.ldap_server.simple_bind_s(self.bind_username, self.bind_password)
        #self.pattern = "(["'])(\\?.)*?\1"

        usname = "john"

        l = ldap.initialize('ldap://40.69.81.8')


        try:
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s(self.bind_username,self.bind_password)
        # except ldap.INVALID_CREDENTIALS:
        #     print "Invalid Username or password"
        except ldap.INVALID_CREDENTIALS:
            print "Your username or password are incorrect"
            sys.exit(0)
        try:
            base_dn = "dc=itcurious,dc=com"
            attr = ['ou']
            filter = "(objectClass=organizationalUnit)"
            #print filter
            #valid = True
            #print "Till now is ok"
            result= l.search_s(base_dn,ldap.SCOPE_SUBTREE,filter,attr)
            result_set = []

            if result == [] :
                print "Ypu are not authorized. Please ask for permissions! "
            else:
                    for x in range(0, len(result)):
                        #print result[x][1]['ou']
                        reg_var= ''.join(result[x][1]['ou'])
                        #result_set.append(result[x][1]['ou'])
                        result_set.append(reg_var)
                    print result_set

                    self.real_value= tuple(result_set)
            print self.real_value


        except Exception, error:
            print error



class AddUser(ldapi,Mainwindows):
    def __init__(self):
        ldapi.__init__(self)
        Mainwindows.__init__(self,parent=None)
        self.frame= Frame(self.parent)
        self.frame.grid(row=2)


        #self.master = master
        print "Runva se"
        self.newuser = StringVar()
        self.newuserpassword = StringVar()
        self.firstname= StringVar()
        self.lastname = StringVar()

        self.DeptName_value = StringVar()
        self.DeptName = ttk.Combobox(self.frame, textvariable=self.DeptName_value)
        self.DeptName.bind("<<ComboboxSelected>>",self.selection)
        self.DeptName['values'] = self.real_value
        self.DeptName.current(0)
        self.DeptName.grid(column=1, row=0)
        self.DeptName_Label = Label(self.frame, text = "Select Department")
        self.DeptName_Label.grid(row=0,column= 0)
        self.UserEntry = Entry( self.frame, textvariable = self.newuser)
        self.UserEntry_Label =Label( self.frame, text = "New User")
        self.UserEntry_Label.grid(row=2,column=0)
        self.UserEntry.grid(row=2,column=1)
        self.PasswordEntry = Entry(self.frame, textvariable=self.newuserpassword)
        self.PasswordEntry_Label = Label(self.frame, text="Password")
        self.PasswordEntry_Label.grid(row=4, column=0)
        self.PasswordEntry.grid(row=4, column=1)

        self.FName = Entry(self.frame, textvariable=self.firstname)
        self.FName_Label = Label(self.frame, text="First Name")
        self.LName = Entry(self.frame, textvariable=self.lastname)
        self.LName_Label = Label(self.frame, text="New User")
        self.FName.grid(row=6, column=1)
        self.FName_Label.grid(row=6, column=0)
        self.LName.grid(row=8, column=1)
        self.LName_Label.grid(row=8, column=0)



        self.OKButton = Button(self.frame, text="Create", command = self.user_creation)
        self.CancelButton = Button(self.frame, text="Cancel")
        self.OKButton.grid(row=10, column=2)
        self.CancelButton.grid(row=10, column=3)


    def selection(self,parent):
        self.value_of_dept = self.DeptName.get()
        print self.value_of_dept

    def user_creation(self):
        name = self.newuser.get()
        userpass = self.newuserpassword.get()
        givenName= self.firstname.get()
        sn = self.lastname.get()
        cn = givenName + ' ' + sn
        homedir = "/home/%s" % name
        print cn

        attrs = {}
        attrs['objectclass'] = ['person','organizationalperson','inetorgperson']
        attrs['uid'] = name
        attrs['cn'] = cn
        attrs['sn'] = sn
        attrs['givenName'] = givenName
        attrs['userPassword'] = userpass
        #attrs['loginShell'] =['/bin/bash']
        #attrs['homeDirectory'] = homedir

        dn = "uid=%s,ou=%s,dc=itcurious,dc=com" % (name, self.value_of_dept)
        print dn

        ldif = modlist.addModlist(attrs)

        try:
            self.ldap_server.add_s(dn,ldif)

        except ldap.LDAPError, error:
            print error

            tkMessageBox.showerror("Something went wrong",error.message['desc'])

        self.Message()



    def Message(self):
        messagebox = tkMessageBox.askyesno("LDAP APPLICATION", "Would you like to continue?")
        print messagebox
        if messagebox == True:
            print "Yes"
            self.value_of_dept= None
            self.UserEntry.delete(0,END)
            self.PasswordEntry.delete(0,END)
            self.FName.delete(0,END)
            self.LName.delete(0,END)
            self.DeptName_value = None
        elif messagebox == False:
            root.quit()



class DeleteUser(ldapi,Mainwindows):
    def __init__(self):
        ldapi.__init__(self)
        Mainwindows.__init__(self,parent=None)


        self.DeptName_value = StringVar()
        self.DeptName = ttk.Combobox(self.frame, textvariable=self.DeptName_value)
        self.DeptName.bind("<<ComboboxSelected>>", self.dept_selection)
        self.DeptName['values'] = self.real_value
        self.DeptName.current(0)
        self.DeptName.grid(column=1, row=0)
        self.DeptName_Label = Label(self.frame, text="Select Department")
        self.frame = Frame(self.parent)
        self.frame.grid(row=2)

        self.UserName_value = StringVar()
        self.UserName = ttk.Combobox(self.frame, textvariable=self.DeptName_value)
        self.UserName.bind("<<ComboboxSelected>>", self.user_selection)
        self.UserName['values'] = self.real_value
        self.UserName.current(0)
        self.UserName.grid(column=1, row=0)
        self.UserName_Label = Label(self.frame, text="Select User Account")


    def dept_selection(self,parent):
        self.value_of_dept = self.DeptName.get()
        print self.value_of_dept



    def user_selection(self,parent):
        self.value_of_user = self.UserName.get()
        print self.value_of_user





if __name__ == "__main__":
    root = Tk()
    my_gui = Guiform(root)
    root.mainloop()

