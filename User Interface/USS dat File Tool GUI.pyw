import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import *
import sys, os, re, time
from datetime import datetime
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
from collections import deque

# Regular expression patterns
record_pattern = re.compile('[a-z][0-9]*\s*')
empty_pattern = re.compile('[^\S\n\t]+')
empty2_pattern = re.compile('[^\S\r\n]{2,}')
lat_long_pattern = re.compile('-?[0-9]{2}\.\d{1,13}$')

missing_meter_filename = 'MissingMeters ' + str(datetime.today().strftime('%Y-%m-%d_%H-%M')) + '.txt'
download_filename = 'download.dat'

# Initial window setup
window = tk.Tk()
s = ttk.Style()
s.theme_use('clam')
window.title("USS dat File Tool v0.9")
window.resizable(False, False)
window.geometry('700x370')

dirp = os.path.dirname(__file__)
photo = PhotoImage(file="assets\\Favicon.png")
window.iconphoto(False, photo)



# Program functions

def singleRecordScan():
    answer = simpledialog.askstring("Enter Record", "Enter the record type to search:",
                                parent=window)
    if answer == None:
        return
    answer = answer.upper()
    counter = 0
    try:
        with open(download_filename, 'r') as openfile:
            for line in openfile:
                if line.startswith(answer):
                    counter+=1
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")

    textBox.delete(1.0, "end")
    textBox.insert("end", f"{counter:,d} " + answer + " records found")
    textBox.insert("end", "\n")


def printSingleRecord():
    record_type = simpledialog.askstring("Enter Record", "Enter the record type to search:",
                                parent=window)
    if record_type == None:
        return
    record_type = record_type.upper()
    counter = 1.0
    try:
        with open(download_filename, 'r') as openfile:
            textBox.delete(1.0, "end")
            for line in openfile:
                if line.startswith(record_type):
                    textBox.insert(counter, line + "\n")
                    counter+=1
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")


def printAllRecords():
    try:
        with open(download_filename, 'r') as openfile:
            counter = 1
            for line in openfile:
                textBox.insert(float(counter), line)
                counter+=1
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")

        
def fixOfficeRegionZoneFields():
    counter = 1.0
    try:
        with open(download_filename, 'r') as openfile:
            for line in openfile:
                if line.startswith('RHD'):
                    office = line[71:73]
                    if office == "  ":
                        office = "BLANK"
                    region = line[73:75]
                    if region == "  ":
                        region = "BLANK"
                    zone = line[75:77]
                    if zone == "  ":
                        zone = "BLANK"
                    textBox.delete(1.0, "end")
                    textBox.insert(1.0, "Office . . . . : \t" + str(office))
                    textBox.insert(2.0, "\n")
                    textBox.insert(2.0, "Region . . . . : \t" + str(region))
                    textBox.insert(3.0, "\n")
                    textBox.insert(3.0, "Zone . . . . . : \t" + str(zone))
                    break
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")

        
def scanAllRecordsVerbose():
    all_records = {}
    counter = 1.0
    try:
        with open(download_filename, 'r') as openfile:
            for line in openfile:
                x = line[0:3]
                if x not in all_records:
                    all_records[x] = 1
                else:
                    all_records[x]+=1
            textBox.delete(counter, "end")
            textBox.insert(counter, "File scan successful")
            counter+=1
            textBox.insert(counter, "\n")
            textBox.insert(counter, "--------------------")
            counter+=1
            textBox.insert(counter, "\n")
            for record in all_records:
                textBox.insert(counter, str(record) + ". . . :\t" + f"{all_records[record]:,d}")
                counter+=1
                textBox.insert(counter, "\n")
            textBox.insert(counter, "--------------------")
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")


def exportMissingMeters():
    counter=0
    try:
        with open(download_filename, 'r') as openfile:
            try:
                with open(missing_meter_filename, 'x') as builtfile:
                    previous_line = ''
                    textBox.delete(1.0, "end")
                    textBox.insert(1.0, "Attempting to export missing meters...")
                    textBox.insert("end", "\n")
                    for line in openfile:
                        if line.startswith('MTR'):
                            meter_record = line[45:57]
                            if empty_pattern.match(meter_record):
                                builtfile.write(previous_line)
                                counter+=1
                        previous_line=line
                    if counter == 0:
                        builtfile.close()
                        os.remove(missing_meter_filename)
                        textBox.insert("end", "\n")
                        textBox.insert("end", "No missing meters found.")
                        return
            except FileExistsError:
                textBox.insert("end", "ERROR: FILE ALREADY EXISTS")
                return
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")
        return
    textBox.delete(1.0, "end")
    textBox.insert(1.0, "The operation was successful.")
    textBox.insert(2.0, "\n")

def missingMeters():
    counter = 0
    empty_pattern = re.compile('[^\S\n\t]+')
    try:
        with open(download_filename, 'r') as openfile:
            previous_line = ''
            textBox.delete(1.0, "end")
            textBox.insert(1.0, "Attempting to find missing meters...")
            textBox.insert(2.0, "\n")
            for line in openfile:
                        if line.startswith('MTR'):
                            meter_record = line[45:57]
                            if empty_pattern.match(meter_record):
                                #builtfile.write(previous_line)
                                textBox.insert("end", previous_line)
                                textBox.insert("end", "\n")
                                counter+=1
                        previous_line=line
            if counter == 0:
                textBox.insert("end", "\n")
                textBox.insert("end", "No missing meters found.")
                return
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")
        return
##    textBox.delete(1.0, "end")
##    textBox.insert(1.0, "The operation was successful.")
##    textBox.insert(2.0, "\n")

def printMeterType():
    user_meter_code = simpledialog.askstring("Enter Record", "Enter the record type to search:", parent=window)
    if user_meter_code == None:
        return
    user_meter_code = user_meter_code.upper()
    counter = 0
    current_record = deque(maxlen=getCustomerRecordLength()+1)
    try:
        with open(download_filename, 'r') as openfile:
            textBox.delete(1.0, "end")
            for line in openfile:
                if line.startswith('RDG'):
                    meter_code = line[76:78] #range 77-78
                    if int(meter_code) == int(user_meter_code):
                        for record in current_record:
                            if record.startswith('CUS'):
                                textBox.insert("end", "{0} {1}".format(counter, record))
                                counter+=1
                current_record.append(line)
            if counter == 0:
                textBox.insert("end", "No meters of that type found.")
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")
        return


def checkMalformedLatLong():
    malformed_data = False
    counter=1
    try:
        with open(download_filename, 'r') as openfile:
            for line in openfile:
                if line.startswith('MTX'):
                    lat_data = line[23:40].rstrip()
                    long_data = line[40:57].rstrip()
                    if not lat_long_pattern.match(lat_data):
                        malformed_data = True 
                        print("Malformed lat data at line:", counter, "Value:", lat_data)
                    elif not lat_long_pattern.match(long_data):
                        malformed_data = True
                        print("Malformed long data at line:", counter, "Value:", long_data)
                counter+=1
            if malformed_data == True:
                print("The above data is malformed in some way.")
            else:
                if checkLatLongSigns(float(lat_data), float(long_data)) == False:
                    print("The data is not malformed.")
                else:
                    print("The data has malformed sign values.")
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND.")

def checkLatLongSigns(lat_data, long_data):
    if lat_data < 0 or long_data > 0:
        return True
    else:
        return False


def getCustomerRecordLength():
    try:
        with open(download_filename, 'r') as openfile:
            counter = start_line = end_line = 0
            for line in openfile:
                counter+=1
                if line.startswith('CUS'):
                    start_line = counter
                if line.startswith('RFF'):
                    end_line = counter
                    length = (end_line-start_line)+1
                    return length
    except FileNotFoundError:
        textBox.insert("end", "ERROR: FILE NOT FOUND")        

def drawCanvas():
    canvas.create_rectangle(20, 140, 120, 180, fill="red")
    canvas.create_text(70, 130, text="Projects--20%")
    canvas.create_rectangle(140, 160, 240, 180, fill="blue")
    canvas.create_text(190, 150, text="Quizzes--10%")
    canvas.create_rectangle(260, 120, 360, 180, fill="green")
    canvas.create_text(310, 110, text="Midterm--30%")
    canvas.create_line(0, 180, 500, 180)

def clearText():
    textBox.delete(1.0, "end")

def save():
    export_filename = "Export " + str(datetime.today().strftime('%Y-%m-%d_%H-%M')) + ".txt"
    with open(export_filename, 'w') as openfile:
        text = textBox.get('1.0', 'end')
        openfile.write(text)

def openFile():
    filename = tk.filedialog.askopenfilename(title="Import File")
    global download_filename
    download_filename = filename
       

def aboutDialog():
    dialog = """Version: 0.9 \n Commit: fa35902dcd98d85f7400ac297a9f61a7200c5803 \n Date: 2020-07-09:12:00:00 \n Python: 3.9.1 \n OS: Windows_NT x64 10.0.10363
            """
    messagebox.showinfo("About", dialog)

################################################

#Create Tab Control
TAB_CONTROL = ttk.Notebook(window)

# Tab 1
##############
TAB1 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB1, text=' Basic Operations Center ')

# Tab 1 Widgets
b01 = ttk.Button(TAB1, text="1.", width=1.5)
b01.place(x=20, y=20)
b1 = ttk.Button(TAB1, text="Single Record Scan", command=lambda:singleRecordScan(), width=20)
b1.place(x=50, y=20)

b02 = ttk.Button(TAB1, text="2.", width=1.5)
b02.place(x=20, y=60)
b2 = ttk.Button(TAB1, text="Full Record Scan", command=lambda:scanAllRecordsVerbose(), width=20)
b2.place(x=50, y=60)

b03 = ttk.Button(TAB1, text="3.", width=1.5)
b03.place(x=20, y=100)
b3 = ttk.Button(TAB1, text="Display Record Type", command=lambda:printSingleRecord(), width=20)
b3.place(x=50, y=100)

b04 = ttk.Button(TAB1, text="4.", width=1.5)
b04.place(x=20, y=140)
b4 = ttk.Button(TAB1, text="Office-Region-Zone", command=lambda:fixOfficeRegionZoneFields(), width=20)
b4.place(x=50, y=140)

b05 = ttk.Button(TAB1, text="5.", width=1.5)
b05.place(x=20, y=180)
b5 = ttk.Button(TAB1, text="Missing Meters", command=lambda:missingMeters(), width=20)
b5.place(x=50, y=180)

b06 = ttk.Button(TAB1, text="6.", width=1.5)
b06.place(x=20, y=220)
b6 = ttk.Button(TAB1, text="Display Meter Type", command=lambda:printMeterType(), width=20)
b6.place(x=50, y=220)

b07 = ttk.Button(TAB1, text="7.", width=1.5)
b07.place(x=20, y=260)
b7 = ttk.Button(TAB1, text="Malformed Lat/Long", command=lambda:checkMalformedLatLong(), width=20)
b7.place(x=50, y=260)


consolelabel = ttk.Label(TAB1, text="Console:")
consolelabel.place(x=220, y=17)
consoleclearbutton = ttk.Button(TAB1, text="clear", width=4.5, command=lambda:clearText())
consoleclearbutton.place(x=622, y=6)

textBox = tk.Text(TAB1, height=16, width=55, background='black', foreground='lawn green')
textBox.place(x=220, y=40)
textBox.insert(1.0, "United Systems dat File Tool")
textBox.insert(2.0, "\n")
textBox.insert(2.0, "(c) 2020 United Systems and Software, Inc.")
textBox.insert(3.0, "\n")

##scrollbar = tk.Scrollbar(window)
###scrollbar = tk.Scrollbar(textBox)
##scrollbar.pack(side=RIGHT, fill=Y)
##textBox.config(yscrollcommand=scrollbar.set)
##scrollbar.config(command=textBox.yview)

# Tab 2
##############
##TAB2 = ttk.Frame(TAB_CONTROL)
##TAB_CONTROL.add(TAB2, text=' Visualizations ')
##TAB_CONTROL.pack(expand=1, fill="both")
##
###Tab 2 Widgets
##tab2label = ttk.Label(TAB2, text="Data Visualization")
##tab2label.place(x=20, y=20)
##tab2label2 = ttk.Label(TAB2, text="Select Data to Display:")
##tab2label2.place(x=20, y=50)
##
##tab2check1 = ttk.Checkbutton(TAB2, text="Customer")
##tab2check1.place(x=30, y=80)
##tab2check2 = ttk.Checkbutton(TAB2, text="Route")
##tab2check2.place(x=30, y=100)
##tab2check3 = ttk.Checkbutton(TAB2, text="Meter")
##tab2check3.place(x=30, y=120)
##tab2check4 = ttk.Checkbutton(TAB2, text="Radio Reads")
##tab2check4.place(x=30, y=140)
##tab2check4 = ttk.Checkbutton(TAB2, text="Placeholder")
##tab2check4.place(x=30, y=160)
##tab2check4 = ttk.Checkbutton(TAB2, text="Placeholder2")
##tab2check4.place(x=30, y=180)
##tab2check4 = ttk.Checkbutton(TAB2, text="Placeholder3")
##tab2check4.place(x=30, y=200)
##
##redrawbutton = ttk.Button(TAB2, text="Render", command=lambda:drawCanvas())
##redrawbutton.place(x=30, y=230)
##
##canvas = tk.Canvas(TAB2, width=440, height=250)
##canvas.place(x= 210, y=30)

# Tab 3
##############
TAB3 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB3, text=" Import/Export ")
TAB_CONTROL.pack(expand=1, fill="both")

#Tab 3 Widgets
tab3label = ttk.Label(TAB3, text="Import data from download file:")
tab3label.place(x=20, y=40)
tab3label2 = ttk.Label(TAB3, text="Export current console data:")
tab3label2.place(x=20, y=115)

tab3importinput = tk.Text(TAB3, width=60, height=1)
tab3importinput.place(x=20, y=65)
tab3importinput.insert(1.0, "C:\\Users\\Alex\\Desktop\\download.dat")
tab3importbutton = ttk.Button(TAB3, text="Import...", command=lambda:openFile())
tab3importbutton.place(x=515, y=60)

tab3exportinput= tk.Text(TAB3, width=60, height=1)
tab3exportinput.place(x=20, y=140)
tab3exportinput.insert(1.0, os.getcwd())
tab3exportbutton = ttk.Button(TAB3, text="Export... ", command=lambda:save())
tab3exportbutton.place(x=515, y=135)

tab3enforcebutton = ttk.Checkbutton(TAB3, text="Enforce referential integrity")
tab3enforcebutton.place(x=20, y=280)
#tab3cleardatabutton = ttk.Checkbutton(TAB3, text="Clear data")
#tab3cleardatabutton.place(x=20, y=170)


# menu
menubar = tk.Menu(window)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", underline=1, command=lambda:openFile())
filemenu.add_command(label="Save", underline=0, command=lambda:save())
filemenu.add_separator()
filemenu.add_command(label="Exit", underline=0, command=lambda:window.destroy())
menubar.add_cascade(label="File", menu=filemenu, underline=0)

# create more pulldown menus
editmenu = tk.Menu(menubar, tearoff=0)
#editmenu.add_command(label="Cut")
editmenu.add_command(label="Clear", underline=1, command=lambda:clearText())
#editmenu.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=editmenu, underline=0)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", underline=0, command=lambda:aboutDialog())
menubar.add_cascade(label="Help", menu=helpmenu, underline=0)

# display the menu
window.config(menu=menubar)
#Calling Main()
window.mainloop()



