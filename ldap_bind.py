import ldap
import ldap.modlist as modlist
import sys
from  Tkinter import *
import ttk
import tkMessageBox
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
                # try:
                #     result_type , result_data = l.result(result,0)
                # except ldap.NO_SUCH_OBJECT:
                #
                #     if result_type == ldap.RES_SEARCH_ENTRY:
                #         dn = result_data[0][1]
                #         data = result_data [0][1]
                #
                #         print dn
                #         print data
                        # result_set.append(name)

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








class GuiForm(ldapi):
    def __init__(self,master):
        ldapi.__init__(self)
        self.master = master
        self.newuser = StringVar()
        self.newuserpassword = StringVar()
        self.firstname= StringVar()
        self.lastname = StringVar()

        self.DeptName_value = StringVar()
        self.DeptName = ttk.Combobox(master, textvariable=self.DeptName_value)
        self.DeptName.bind("<<ComboboxSelected>>",self.selection)
        self.DeptName['values'] = self.real_value
        self.DeptName.current(0)
        self.DeptName.grid(column=1, row=0)
        self.DeptName_Label = Label(master, text = "Select Department")
        self.DeptName_Label.grid(row=0,column= 0)
        self.UserEntry = Entry( master, textvariable = self.newuser)
        self.UserEntry_Label =Label( master, text = "New User")
        self.UserEntry_Label.grid(row=2,column=0)
        self.UserEntry.grid(row=2,column=1)
        self.PasswordEntry = Entry(master, textvariable=self.newuserpassword)
        self.PasswordEntry_Label = Label(master, text="Password")
        self.PasswordEntry_Label.grid(row=4, column=0)
        self.PasswordEntry.grid(row=4, column=1)

        self.FName = Entry(master, textvariable=self.firstname)
        self.FName_Label = Label(master, text="First Name")
        self.LName = Entry(master, textvariable=self.lastname)
        self.LName_Label = Label(master, text="New User")
        self.FName.grid(row=6, column=1)
        self.FName_Label.grid(row=6, column=0)
        self.LName.grid(row=8, column=1)
        self.LName_Label.grid(row=8, column=0)



        self.OKButton = Button(master, text="Create", command = self.user_creation)
        self.CancelButton = Button(master, text="Cancel")
        self.OKButton.grid(row=10, column=2)
        self.CancelButton.grid(row=10, column=3)



        # self.notebook= ttk.Notebook(master)
        # tab1 = ttk.Frame( self.notebook)
        # tab2 = ttk.Frame(self.notebook)
        # tab3 = ttk.Frame(self.notebook)
        # self.notebook.add(tab1, text="Create New User", compound=TOP)
        # self.notebook.add(tab2, text="Tab Two")
        # self.notebook.add(tab3, text="Tab Three")
        # self.notebook.pack()
        # self.notebook.bind("<<NotebookTabChanged>>", self.check_tab)

    def selection(self, master):
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
            self.UserEntry.delete(0,END)
            self.PasswordEntry.delete(0,END)
            self.FName.delete(0,END)
            self.LName.delete(0,END)
            self.DeptName_value = None
        elif messagebox == False:
            root.quit()
















root = Tk()
app = GuiForm(root)
root.mainloop()
