#Sarah Ewing
#Python I Final Test
#11/16/2021

import tkinter as tk
import csv
import xml.etree.ElementTree as et
import sqlite3
from contextlib import closing
CSVFILENAME = "employeedata.csv"

class MakeFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill = tk.BOTH, expand=True, padx= 50, pady=20)

        self.errorMessage = tk.StringVar()
        self.idText = tk.StringVar()
        self.firstNameText = tk.StringVar()
        self.lastNameText = tk.StringVar()
        self.payrateText = tk.StringVar()
        self.errorMessage.set("")

        self.initComponents()

    def initComponents(self):
                
        tk.idLabel = tk.Label(self, text="Employee ID").grid(column=0, row=0, sticky=tk.E)
        tk.idEntry = tk.Entry(self, width=25, textvariable=self.idText).grid(column=1, row=0, columnspan=2)
        tk.firstNameLabel = tk.Label(self, text="First Name").grid(column=0, row=1, sticky=tk.E)
        tk.idEntry = tk.Entry(self, width=25, textvariable=self.firstNameText).grid(column=1, row=1, columnspan=2)
        tk.lastNameLabel = tk.Label(self, text="Last Name").grid(column=0, row=2, sticky=tk.E)
        tk.idEntry = tk.Entry(self, width=25, textvariable=self.lastNameText).grid(column=1, row=2, columnspan=2)
        tk.payrateLabel = tk.Label(self, text="Payrate").grid(column=0, row=3, sticky=tk.E)
        tk.idEntry = tk.Entry(self, width=25, textvariable=self.payrateText).grid(column=1, row=3, columnspan=2)
        tk.dbButton = tk.Button(self, text="Clear all fields", command=self.clearAllFields).grid(column=0, row=4, columnspan=3)
        tk.payrateLabel = tk.Label(self, textvariable=self.errorMessage).grid(column=0, row=5, columnspan=3)
        tk.csvButton = tk.Button(self, text="CSV", bg="lightyellow", command=self.addToCsv).grid(column=0, row=6)
        tk.xmlButton = tk.Button(self, text="XML", bg="lightgreen", command=self.addToXml).grid(column=1, row=6)
        tk.dbButton = tk.Button(self, text="DB", bg="lightblue", command=self.addToDb).grid(column=2, row=6)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def appendToList(self):
        entry = []
        entry.append(self.idText.get())
        entry.append(self.firstNameText.get())
        entry.append(self.lastNameText.get())
        entry.append(self.payrateText.get())
        return entry
        

    def addToCsv(self):
        self.validationCheck()
        
        if self.errorMessage.get() == "":    
            entries = []
            with open(CSVFILENAME, newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    entries.append(row)

            entry = self.appendToList()

            lst = []
            for item in entries:
                lst.append(item[0])

            if entry[0] in lst:
                self.errorMessage.set("ID already exists, please try again")
            else:
                entries.append(entry)
                
                with open(CSVFILENAME, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(entries)
                self.errorMessage.set("Entry was saved to employeedata.csv")

    def addToXml(self):
        self.validationCheck()
        
        if self.errorMessage.get() == "":    
            tree = et.parse('employeedata.xml')
            root = tree.getroot()
            lst = []
            for child in root.findall('EMPLOYEE'):
                lst.append(child.find('ID').text)               

            entry = self.appendToList()

            if entry[0] in lst:
                self.errorMessage.set("ID already exists, please try again")
            else:
                employee = et.SubElement(root, 'EMPLOYEE')

                number = et.SubElement(employee, 'ID')
                number.text = self.idText.get()
                firstName = et.SubElement(employee, 'FIRSTNAME')
                firstName.text = self.firstNameText.get()
                lastName = et.SubElement(employee, 'LASTNAME')
                lastName.text = self.lastNameText.get()
                payrate = et.SubElement(employee, 'PAYRATE')
                payrate.text = self.payrateText.get()                
                                
                et.indent(tree)
                tree.write('employeedata.xml')
                self.errorMessage.set("Entry was saved to employeedata.xml")

    def addToDb(self):
        self.validationCheck()
        
        if self.errorMessage.get() == "":    
            entries = []
            conn = sqlite3.connect('employeedata.db')

            try:
                with closing(conn.cursor()) as c:
                    sql = """INSERT INTO EMPLOYEES (ID, FIRSTNAME, LASTNAME, PAYRATE) VALUES (?,?,?,?)"""
                    c.execute(sql, (self.idText.get(), self.firstNameText.get(), self.lastNameText.get(), self.payrateText.get()))
                    conn.commit()
                self.errorMessage.set("Entry was saved to employeedata.db")
            except:
                self.errorMessage.set("ID already exists, please try again")
            

    def validationCheck(self):
        try:
            int(self.idText.get())
            self.errorMessage.set("")
            try:
                float(self.payrateText.get())
                self.errorMessage.set("")
            except:
                self.errorMessage.set("Payrate number invalid, entry not saved")                
        except:
            self.errorMessage.set("ID number invalid, entry not saved")

    def clearAllFields(self):
        self.idText.set("")
        self.firstNameText.set("")
        self.lastNameText.set("")
        self.payrateText.set("")
        self.errorMessage.set("")

if __name__ == "__main__":
    mainWindow = tk.Tk()
    mainWindow.title("Employee Data Entry")
    mainWindow.geometry("365x275")
    MakeFrame(mainWindow)
    mainWindow.mainloop()
