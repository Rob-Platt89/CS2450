import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tempfile import NamedTemporaryFile
from PIL import ImageTk,Image #pip install Pillow
import re      
import pdb
import csv
import os
import platform
import shutil
import datetime
import Pmw #pip3 install Pmw-py3

dir_path = os.path.dirname(os.path.realpath(__file__))

if platform.system() == 'Windows':
    slash_direction = '\\'
else:
    slash_direction = '/'
TIMECARD_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'timecard.png'
RUN_PAY_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'run_pay.png'
RECEIPT_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'receipt.png'
ADD_EMP_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'add_emp.png'
EDIT_EMP_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'edit_emp.png'
EMPLOYEE_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'emp_dir.png'
EDIT_PAYROLL_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'edit_payroll.png'
EDIT_PERSONAL_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'edit_personal.png'
LOGIN_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'login.png'
PROFILE_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'profile.png'
PAYROLL_IMG = dir_path + slash_direction + 'user_manual_pics' + slash_direction + 'payroll.png'
PASSWORD_CSV = dir_path + slash_direction + 'passwords.csv'
EMPLOYEE_CSV = dir_path + slash_direction + 'employees_test.csv'
EMPLOYEES_HEADER = ['ID', 'FirstName', 'LastName', 'Address', 'City', 'State', 'Zip', 'Classification', 'PayMethod', 'Salary', 'Hourly', 'Commission', 'Route', 'Account', 'OfficePhone', 'DOB', 'SSN', 'StartDate', 'PermissionLevel', 'JobTitle', 'Dpt', 'Email', 'EarningToDate', 'Archived', 'AboutMe']
RECEIPTS_CSV = dir_path + slash_direction + 'receipts_test.csv'
TIMECARDS_CSV = dir_path + slash_direction + 'timecards_test.csv'
DEFAULT_PASSWORD = 'Hello World'
CURRENT_PATH = dir_path + slash_direction
CURRENT_YEAR = 2021
STATES = ['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN',
        'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
        'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
        'WI', 'WY']

CLASSES = ['', '1', '2', '3']
PAY_TYPES = ['', '1', '2']
PERMISSION = ['', '1', '2']

class APP(tk.Tk):
    def __init__(self):
        global EMPLOYEES_HEADER
        super().__init__()
        print('Creating Application Class')
        self.balloon = Pmw.Balloon(self)
        self.title('EMS')
        self.geometry('900x750')
        self.resizable(True, True)
        self.configure(bg='#e4faff')
        self.user_info = [''] * len(EMPLOYEES_HEADER)
        self.employee_info = []
        self.user_permission_level = 2
        controller = tk.Frame(self)
        controller.grid(column=0, row=0)
        controller.grid_rowconfigure(0, weight=1)
        controller.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LOGIN_FRAME, PROFILE_INFO_FRAME, EDIT_PERSONAL_INFO, 
        PAYROLL_INFO_FRAME, EDIT_PAYMENT_INFO, EMPLOYEE_SEARCH_FRAME):
            page_name = F.__name__
            frame = F(parent=controller, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='NSEW')

        self.show_frame('PROFILE_INFO_FRAME')
        
    def get_user_info(self, empid):
        global EMPLOYEE_CSV
        with open(EMPLOYEE_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                if row[0] == 'ID':
                    continue
                elif row[0] == empid:
                    index = 0
                    for entry in row:
                        if entry == '':
                            index += 1
                            continue
                        self.user_info[index] = str(entry)
                        index += 1
                    break
        if self.user_info[18] != '':
            self.user_permission_level = self.user_info[18]
    
    def get_employee_info(self, filter='', includeArchived=False):
        filter = filter.lower()
        filter.split(' ')
        if filter == '':
            filter = '1234567890'
        if filter == '*':
            filter = ''
        global EMPLOYEE_CSV
        global EMPLOYEES_HEADER
        self.employee_info.clear()
        with open(EMPLOYEE_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                if row[0] == 'ID':
                    continue
                elif row[0] == self.user_info[0]:
                    continue
                elif not row[0].lower().startswith(filter) and not row[1].lower().startswith(filter) and not row[2].lower().startswith(filter):
                    continue
                else:
                    employee = ['']*len(EMPLOYEES_HEADER)
                    index = 0
                    for entry in row:
                        if entry == '':
                            index += 1
                            continue
                        employee[index] = str(entry)
                        index += 1
                    # If we are not including archived employees, and the employee is archived
                    # then we continue past them.
                    if not includeArchived:
                        if employee[23] == 'True':
                            continue
                    self.employee_info.append(employee)
    
    def update_employee_info(self, employee):
        global EMPLOYEES_HEADER
        global EMPLOYEE_CSV
        # Read from current Employees file, write to temp file
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

        with open(EMPLOYEE_CSV, 'r') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            writer.writerow(EMPLOYEES_HEADER)
            for row in reader:
                if row[0] == 'ID':
                    continue
                elif row[0] != employee[0]:
                    writer.writerow(row)
                else:
                    temp_list = []
                    for entry in employee:
                        if entry == '':
                            temp_list.append('')
                        else:
                            temp_list.append(entry)
                    writer.writerow(temp_list)
        shutil.move(tempfile.name, EMPLOYEE_CSV)

    def add_new_employee(self, new_employee):
        with open(EMPLOYEE_CSV, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(new_employee)

    def add_password(self, emp_id):
        global PASSWORD_CSV
        global DEFAULT_PASSWORD

        with open(PASSWORD_CSV, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            entry = [emp_id, DEFAULT_PASSWORD]
            writer.writerow(entry)
    
    def show_frame(self, frame_name):
        '''if self.frames['EMPLOYEE_SEARCH_FRAME'].scrollbar_active:
            self.frames['EMPLOYEE_SEARCH_FRAME'].scrollbar_active = False
            self.frames['EMPLOYEE_SEARCH_FRAME'].scrollbar.destroy()
            self.frames['EMPLOYEE_SEARCH_FRAME'].list.destroy()'''
        frame = self.frames[frame_name]
        frame.update_frame()
        navbar_options = {'pady':(0, 10), 'padx':5}
        style = ttk.Style()
        style.configure('Theme.TButton', font=('TkDefaultFont', 12, 'bold', 'underline'), background='black')
        if(frame_name == 'LOGIN_FRAME'):
            self.geometry('300x175')

        #Navigation Bar
        if(frame_name == 'PROFILE_INFO_FRAME'):
            frame.payroll_info_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Payroll Info')
            frame.payroll_info_button.grid(column=0, row=0, **navbar_options)
            frame.payroll_info_button.grid_rowconfigure(0, weight=1)
            frame.payroll_info_button.configure(command=lambda: self.show_frame('PAYROLL_INFO_FRAME'))
            frame.profile_page_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Profile Page')
            frame.profile_page_button.grid(column=1, row=0, **navbar_options)
            frame.profile_page_button.grid_rowconfigure(0, weight=1)
            frame.profile_page_button.configure(command=lambda: self.show_frame('PROFILE_INFO_FRAME'))
            frame.employee_directory_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Employee Directory')
            frame.employee_directory_button.grid(column=2, row=0, **navbar_options)
            frame.employee_directory_button.grid_rowconfigure(0, weight=1)
            frame.employee_directory_button.configure(command=lambda: self.show_frame('EMPLOYEE_SEARCH_FRAME'))
            self.geometry('940x500')
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
        if(frame_name == 'PAYROLL_INFO_FRAME'):
            frame.payroll_info_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Payroll Info')
            frame.payroll_info_button.grid(column=0, row=0, **navbar_options)
            frame.payroll_info_button.grid_rowconfigure(0, weight=1)
            frame.payroll_info_button.configure(command=lambda: self.show_frame('PAYROLL_INFO_FRAME'))
            frame.profile_page_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Profile Page')
            frame.profile_page_button.grid(column=1, row=0, **navbar_options)
            frame.profile_page_button.grid_rowconfigure(0, weight=1)
            frame.profile_page_button.configure(command=lambda: self.show_frame('PROFILE_INFO_FRAME'))
            frame.employee_directory_button = ttk.Button(frame, style='Theme.TButton', width=60, text='Employee Directory')
            frame.employee_directory_button.grid(column=2, row=0, **navbar_options)
            frame.employee_directory_button.grid_rowconfigure(0, weight=1)
            frame.employee_directory_button.configure(command=lambda: self.show_frame('EMPLOYEE_SEARCH_FRAME'))
            self.geometry('940x500')
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
        if(frame_name == 'EMPLOYEE_SEARCH_FRAME'):
            frame.payroll_info_button = ttk.Button(frame, style='Theme.TButton', width=20, text='Payroll Info')
            frame.payroll_info_button.grid(column=0, row=0, **navbar_options)
            frame.payroll_info_button.grid_rowconfigure(0, weight=1)
            frame.payroll_info_button.configure(command=lambda: self.show_frame('PAYROLL_INFO_FRAME'))
            frame.profile_page_button = ttk.Button(frame, style='Theme.TButton', width=20, text='Profile Page')
            frame.profile_page_button.grid(column=1, row=0, **navbar_options)
            frame.profile_page_button.grid_rowconfigure(0, weight=1)
            frame.profile_page_button.configure(command=lambda: self.show_frame('PROFILE_INFO_FRAME'))
            frame.employee_directory_button = ttk.Button(frame, style='Theme.TButton', width=20, text='Employee Directory')
            frame.employee_directory_button.grid(column=2, row=0, **navbar_options)
            frame.employee_directory_button.grid_rowconfigure(0, weight=1)
            frame.employee_directory_button.configure(command=lambda: self.show_frame('EMPLOYEE_SEARCH_FRAME'))
            self.geometry('800x500')
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid_columnconfigure(3, weight=1)
        
        if(frame_name == 'EDIT_PERSONAL_INFO'):
            self.geometry('350x400')

        if(frame_name == 'EDIT_PAYMENT_INFO'):
            self.geometry('350x280')

        frame.tkraise()

class EMPLOYEE_SEARCH_FRAME(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.scrollbar_active = False
        
        options = {'padx': 5, 'pady': 5}

        #Search Box Entry   
        self.name_label = ttk.Label(self, text='Search Employee:')
        self.name_label.grid(column=0, row=1, sticky='W', **options)
        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.bind("<KeyRelease>", self.search)
        self.name_entry.grid(column=1, row=1, sticky='W', **options)
        self.name_entry.focus()

        #Clear Search Button
        self.clear_search_button = ttk.Button(self, text='Clear Search')
        self.clear_search_button.grid(column=2, row=1, sticky='W', **options)
        self.clear_search_button.configure(command=self.clear_search)

        #Include Archived Checkbox
        self.archived = tk.BooleanVar()
        self.archived_checkbox = tk.Checkbutton(self, text='Include Archived?', variable=self.archived, onvalue=True, offvalue=False, command=self.search)
        self.archived_checkbox.grid(column=3, row=1, sticky='W', **options)
        
        #Logout Button
        self.logout_button = ttk.Button(self, text='Logout')
        self.logout_button.grid(column=3, row=10, sticky='SE')
        self.logout_button.configure(command=self.logout)
        self.grid(column=0, row=1, **options)

        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=0, row=10, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)
    
    def help(self):
        self.profile_img = Image.open(EMPLOYEE_IMG)
        self.profile_img.show()

    def logout(self):
        app.show_frame('LOGIN_FRAME')

    def error(self):
        self.new_window = tk.Toplevel(app)
        self.new_window.title('Error')
        self.new_window.geometry('100x100')
        self.error_label = ttk.Label(self.new_window, text='Not yet available')
        self.error_label.grid(column=0, row=0)

    def update_frame(self):
        '''Update frame function for Employee Directory Page
        Adds the Add Employee Button if user is an admin.
        Iterates through employee database and adds employees
        to the list for viewing.
        Adds a View Employee Button for the user to get more info
        about the selected employee.'''
        self.scrollbar_active = True
        self.controller.title('Employee Directory')

        # Include Add Employee button if the user is an admin
        if self.controller.user_permission_level == '1':
            self.add_employee_button = ttk.Button(self, text='Add New Employee')
            self.add_employee_button.grid(column=0, row=2)
            self.add_employee_button.configure(command=self.add_employee)

        # View Employee Button - Changes based on permission level
        if self.controller.user_permission_level == '1':
            self.view_emp_button = ttk.Button(self, text='View/Edit Selected Employee')
            self.view_emp_button.grid(column=1, row=2)
            self.view_emp_button.configure(command=lambda: self.view_employee_admin(self.get_selected()))
        else:
            self.view_emp_button = ttk.Button(self, text='View Selected Employee')
            self.view_emp_button.grid(column=1, row=2)
            self.view_emp_button.configure(command=lambda: self.view_employee_base(self.get_selected()))

        #Submit Receipt and Timecard Buttons for Admin's Only
        if self.controller.user_permission_level == '1':
            self.receipt_button = ttk.Button(self, text='Submit\nReceipt')
            self.receipt_button.grid(column=3, row=4, sticky='NW')
            self.receipt_button.configure(command=lambda: self.add_receipt(self.get_selected()))
            self.timecard_button = ttk.Button(self, text='Submit\nTimecard')
            self.timecard_button.grid(column=3, row=5, sticky='NW')
            self.timecard_button.configure(command=lambda: self.add_timecard(self.get_selected()))

        #Run Payroll, Archive, and Unarchive Buttons for Admin's Only
        if self.controller.user_permission_level == '1':
            self.archive_button = ttk.Button(self, text='Archive Selected')
            self.archive_button.grid(column=2, row=2, sticky='NE', pady=30)
            self.archive_button.configure(command=lambda: self.archive_employee(self.get_selected()))
            self.run_payroll_button = ttk.Button(self, text='Run Payroll')
            self.run_payroll_button.grid(column=3, row=3, sticky='NW', pady=30)
            self.run_payroll_button.configure(command=self.run_payroll)
            self.unarchive_button = ttk.Button(self, text='Unarchive Selected')
            self.unarchive_button.grid(column=3, row=2)
            self.unarchive_button.configure(command=lambda: self.unarchive_employee(self.get_selected()))

        #Employee List - Headers and List Reference
        self.list = ttk.Treeview(self, columns=('Last Name', 'Employee ID'))
        #self.scrollbar = ttk.Scrollbar(orient='vertical', command=self.list.yview)
        #self.scrollbar.place(x=630, y=123, height=210)
        #self.list.configure(yscrollcommand=self.scrollbar.set)
        self.list.grid(padx=30, pady=25, column=0, columnspan=3, row=3, rowspan=3, sticky='W')
        self.list.heading('#0', text='First Name')
        self.list.heading('#1', text='Last Name')
        self.list.heading('#2', text='Employee ID')
        # Iteratively add employee info into the list
        self.controller.get_employee_info(filter = self.name_entry.get(), includeArchived=self.archived.get())
        self.controller.employee_info.sort(key=lambda x : x[2])
        for employee in self.controller.employee_info:
            if employee[23] == 'True':
                self.list.insert("", 'end', text=employee[1], values=(employee[2], employee[0]), tags=('archived'))
            elif '' in employee:
                self.list.insert("", 'end', text=employee[1], values=(employee[2], employee[0]), tags=('missingInfo'))
            else:
                self.list.insert("", 'end', text=employee[1], values=(employee[2], employee[0]))
        self.list.tag_configure('archived', background='#ffabae')
        self.list.tag_configure('missingInfo', background='#fffd7d')

    def get_selected(self):
        '''Helper function for getting the employee list of the selected item in the GUI list'''
        selected = self.list.focus()
        empId = str(self.list.item(selected)['values'][1])
        for emp in self.controller.employee_info:
            if empId == emp[0]:
                return emp
        return None

    def run_payroll(self):
        if tk.messagebox.askokcancel(title='Confirm Payroll', 
                                    message=f'Are you sure you want to run payroll?', 
                                    icon='warning', default='ok'):
            # Create new directory for storing new payroll files - dir name based on current date
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            new_dir = date + '_payroll'
            path = os.path.join(CURRENT_PATH, new_dir)
            os.mkdir(path)

            # Get list of all non-archived employees (including user)
            self.controller.get_employee_info(filter='*')
            employees = self.controller.employee_info + [self.controller.user_info]

            # Read in timecard and receipt data
                # While doing so, write copies of this data to new files
            timecards = []
            receipts = []
            timecards_copy = path + slash_direction + date + '_timecards.csv'
            receipts_copy = path + slash_direction + date + '_receipts.csv'
            with open(TIMECARDS_CSV, 'r') as csvFile, open(timecards_copy, 'w') as copy:
                reader = csv.reader(csvFile, delimiter=',')
                writer = csv.writer(copy, delimiter=',')
                for row in reader:
                    timecards.append(row)
                    writer.writerow(row)
            
            with open(RECEIPTS_CSV, 'r') as csvFile, open(receipts_copy, 'w') as copy:
                reader = csv.reader(csvFile, delimiter=',')
                writer = csv.writer(copy, delimiter=',')
                for row in reader:
                    receipts.append(row)
                    writer.writerow(row)

            # Create Payroll File to write to
            payroll_file = path + slash_direction + date + '_payroll.txt'
            # Iterate through employees, calculate each payroll, write to file, update year-to-date
            with open(payroll_file, 'w') as payroll:
                for emp in employees:
                    total_pay = 0
                    if emp[7] == '': # If missing classification info then skip
                        continue
                    if emp[7] == '1': # Calculation for hourly employees
                        total_pay = 0
                        for timecard in timecards: # Traverse timecards to find employee's
                            if timecard[0] == emp[0]:
                                for entry in timecard[1:]: # Calculate total pay using timecard entries
                                    total_pay += float(entry) * float(emp[10])
                    elif emp[7] == '2': # Calculation for salaried employees
                        total_pay = float(emp[9]) / 24
                    else: # Calculation for commissioned employees
                        total_pay = float(emp[9]) / 24 # Pay starts at 1/24th of salary
                        for receipt in receipts: # Find this employees receipts
                            if receipt[0] == emp[0]:
                                for entry in receipt[1:]: # Calculate total using receipts
                                    total_pay += float(entry) * (float(emp[11])/100)
                    if emp[8] == '1': # Output string for mailed employees
                        output = f'Mailing {total_pay:.2f} to {emp[1]} {emp[2]} at {emp[3]} {emp[4]}, {emp[5]} {emp[6]}\n'
                    else: # Output string for ACH employees
                        output = f'Transferred {total_pay:.2f} for {emp[1]} {emp[2]} to {emp[13]} at {emp[12]}\n'
                    # Write to file
                    payroll.write(output)
                    # Update year-to-date
                    if emp[22] == '':
                        emp[22] = '0.00'
                    year_to_date = float(emp[22])
                    year_to_date += total_pay
                    emp[22] = f'{year_to_date:.2f}'
                    self.controller.update_employee_info(emp)

            # Clear old receipt/timecard files
            '''
            f = open(RECEIPTS_CSV, 'w')
            f.close()
            f = open(TIMECARDS_CSV, 'w')
            f.close()
            '''
            tk.messagebox.showinfo(title='Payroll Complete', message=f'Payroll Complete. Find Info at {payroll_file}')
        else:
            tk.messagebox.showinfo(title='Payroll Canceled', message='Payroll was not run.')

    def payment_submission_validation(self, input):
        singleDigit = '^\d+$'
        digitWithDecimal = '^\d+\.\d+$'
        if re.search(singleDigit, input) or re.search(digitWithDecimal, input):
            return True
        else:
            return False

    def confirm_receipts(self, receipts, empid):

        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

        with open(RECEIPTS_CSV, 'r') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            for row in reader:
                if row[0] == empid:
                    entry = [empid] + receipts
                    writer.writerow(entry)
                else:
                    writer.writerow(row)
        
        shutil.move(tempfile.name, RECEIPTS_CSV)
        self.receipt_window.destroy()

    def render_receipt_list(self, receipts):
        self.receipt_list = ttk.Treeview(self.receipt_window, columns=('#1'))
        self.receipt_list.grid(padx=25, pady=25, column=0, row=1, rowspan=2)
        self.receipt_list.heading('#0', text='Entry Number')
        self.receipt_list.heading('#1', text='Receipt Amount (Hours)')
        count = 1
        for entry in receipts:
            self.receipt_list.insert("", 'end', text=count, values=(entry))
            count += 1

    def submit_receipt(self, amount, receipts):
        if self.payment_submission_validation(amount):
            receipts.append(amount)
            self.entered_amount.set('0.00')
            self.render_receipt_list(receipts)
        else:
            tk.messagebox.showinfo(title='Error', message='Please enter receipt as a valid dollar amount. Ex: "150.55"')

    def get_selected_receipt(self):
        # Returns the index of the selected receipt in the receipt treeview
        selected = self.receipt_list.focus()
        return int(self.receipt_list.item(selected)['text']) - 1

    def delete_receipt(self, index, receipts):
        # Removes item from timecards list using index
        del receipts[index]
        self.render_receipt_list(receipts)

    def add_receipt(self, employee):
        # Confirm that selected employee is a commissioned employee
        if employee[7] != '3':
            tk.messagebox.showinfo(title='Error', message='Selected Employee is not a commission employee.')
            return
        # Confirm that selected employee is not archived.
        if employee[23] == 'True':
            tk.messagebox.showinfo(title='Error', message='Cannot add receipt for archived employee.')
            return
        # Get list of current receipts for the selected employee
        with open(RECEIPTS_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            receipts = []
            # Traverse CSV file finding current timecards for employee
            for row in reader:
                if row[0] == employee[0]:
                    receipts = row[1:] # copy timecards but leave out employee ID
                    break

        # Create Toplevel window
        options = {'padx':5, 'pady':5}
        self.receipt_window = tk.Toplevel(app)
        self.receipt_window.title(f'Receipts for: {employee[1]} {employee[2]}')
        self.receipt_window.geometry('700x400')

        # Make entry box for adding a timecard with button
        self.entered_amount = tk.StringVar(value='0.00')
        self.receipt_entry = ttk.Entry(self.receipt_window, textvariable=self.entered_amount)
        self.receipt_entry.grid(row=0, column=0, **options)
        self.submit_button = ttk.Button(self.receipt_window, text='Submit\nReceipt')
        self.submit_button.grid(row=0, column=1, **options)
        self.submit_button.configure(command=lambda: self.submit_receipt(self.entered_amount.get(), receipts))

        # Make treeview list of current timecards
        self.render_receipt_list(receipts)

        # Delete button for deleting selected item in the list
        self.delete_button = ttk.Button(self.receipt_window, text='Delete\nReceipt')
        self.delete_button.grid(row=1, column=1, **options)
        self.delete_button.configure(command=lambda: self.delete_receipt(self.get_selected_receipt(), receipts))

        # Confirm button for writing list of receipts to database
        self.confirm_button = ttk.Button(self.receipt_window, text='Confirm')
        self.confirm_button.grid(row=3, column=0, **options)
        self.confirm_button.configure(command=lambda: self.confirm_receipts(receipts, employee[0]))

        # Cancel button for closing window and not changing any info in database
        self.cancel_button = ttk.Button(self.receipt_window, text='Cancel')
        self.cancel_button.grid(row=3, column=1, **options)
        self.cancel_button.configure(command=lambda: self.receipt_window.destroy())

        self.help_button = ttk.Button(self.receipt_window, text='Help')
        self.help_button.grid(column=0, row=4, sticky='SW', **options)
        self.help_button.configure(command=self.receipt_help)

    def receipt_help(self):
        self.profile_img = Image.open(LOGIN_IMG)
        self.profile_img.show(RECEIPT_IMG)
        
        self.grid_columnconfigure(0, weight=1)
    def confirm_timecards(self, timecards, empid):

        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

        with open(TIMECARDS_CSV, 'r') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            for row in reader:
                if row[0] == empid:
                    entry = [empid] + timecards
                    writer.writerow(entry)
                else:
                    writer.writerow(row)
        
        shutil.move(tempfile.name, TIMECARDS_CSV)
        self.timecard_window.destroy()

    def render_timecard_list(self, timecards):
        self.timecard_list = ttk.Treeview(self.timecard_window, columns=('#1'))
        self.timecard_list.grid(padx=25, pady=25, column=0, row=1, rowspan=2)
        self.timecard_list.heading('#0', text='Entry Number')
        self.timecard_list.heading('#1', text='Timecard Amount (Hours)')
        count = 1
        for entry in timecards:
            self.timecard_list.insert("", 'end', text=count, values=(entry))
            count += 1
    
    def submit_timecard(self, amount, timecards):
        if self.payment_submission_validation(amount):
            timecards.append(amount)
            self.entered_amount.set('0.0')
            self.render_timecard_list(timecards)
        else:
            tk.messagebox.showinfo(title='Error', message='Please enter timecard amount as a decimal of the hours worked. Ex: "6.5"')

    def get_selected_timecard(self):
        # Returns the index of the selected timecard in the timecard treeview
        selected = self.timecard_list.focus()
        return int(self.timecard_list.item(selected)['text']) - 1

    def delete_timecard(self, index, timecards):
        # Removes item from timecards list using index
        del timecards[index]
        self.render_timecard_list(timecards)

    def add_timecard(self, employee):
        # Confirm that selected employee is an hourly employee
        if employee[7] != '1':
            tk.messagebox.showinfo(title='Error', message='Selected Employee is not an hourly employee.')
            return
        # Confirm that selected employee is not archived.
        if employee[23] == 'True':
            tk.messagebox.showinfo(title='Error', message='Cannot add timecard for archived employee.')
            return
        # Get list of current timecards for the selected employee
        with open(TIMECARDS_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            timecards = []
            # Traverse CSV file finding current timecards for employee
            for row in reader:
                if row[0] == employee[0]:
                    timecards = row[1:] # copy timecards but leave out employee ID
                    break

        # Create Toplevel window
        options = {'padx':5, 'pady':5}
        self.timecard_window = tk.Toplevel(app)
        self.timecard_window.title(f'Timecards for: {employee[1]} {employee[2]}')
        self.timecard_window.geometry('700x400')

        # Make entry box for adding a timecard with button
        self.entered_amount = tk.StringVar(value='0.0')
        self.timecard_entry = ttk.Entry(self.timecard_window, textvariable=self.entered_amount)
        self.timecard_entry.grid(row=0, column=0, **options)
        self.submit_button = ttk.Button(self.timecard_window, text='Submit\nTimecard')
        self.submit_button.grid(row=0, column=1, **options)
        self.submit_button.configure(command=lambda: self.submit_timecard(self.entered_amount.get(), timecards))

        # Make treeview list of current timecards
        self.render_timecard_list(timecards)

        # Delete button for deleting selected item in the list
        self.delete_button = ttk.Button(self.timecard_window, text='Delete\nTimecard')
        self.delete_button.grid(row=1, column=1, **options)
        self.delete_button.configure(command=lambda: self.delete_timecard(self.get_selected_timecard(), timecards))

        # Confirm button for writing list of timecards to database
        self.confirm_button = ttk.Button(self.timecard_window, text='Confirm')
        self.confirm_button.grid(row=3, column=0, **options)
        self.confirm_button.configure(command=lambda: self.confirm_timecards(timecards, employee[0]))

        # Cancel button for closing window and not changing any info in database
        self.cancel_button = ttk.Button(self.timecard_window, text='Cancel')
        self.cancel_button.grid(row=3, column=1, **options)
        self.cancel_button.configure(command=lambda: self.timecard_window.destroy())
        
        self.help_button = ttk.Button(self.timecard_window, text='Help')
        self.help_button.grid(column=0, row=4, sticky='SW', **options)
        self.help_button.configure(command=self.timecard_help)

    def timecard_help(self):
        self.profile_img = Image.open(TIMECARD_IMG)
        self.profile_img.show()

    def search(self, key=None):
        '''Reloads the page with new list of employees that meet the filter requirements'''
        self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')

    def clear_search(self):
        '''Clears search entry box and reloads page'''
        self.name.set('')
        self.archived.set(False)
        self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')

    def view_employee_base(self, employee):

        options = {'padx':5, 'pady':5}
        self.new_window = tk.Toplevel(app)
        self.new_window.title(f'Viewing: {employee[1]} {employee[2]}')
        self.new_window.geometry('500x400')

        self.id_label = ttk.Label(self.new_window, text=f'ID: {employee[0]}')
        self.id_label.grid(column=0, row=0, sticky='WE', **options)
        self.name_label = ttk.Label(self.new_window, text=f'Name: {employee[1]} {employee[2]}')
        self.name_label.grid(column=1, row=0, sticky='WE', **options)
        self.job_label = ttk.Label(self.new_window, text=f'Job: {employee[19]} - {employee[20]}')
        self.job_label.grid(column=2, row=0, sticky='WE', **options)
        phone = employee[14]
        if phone == '':
            phone = 'XXXXXXXXXX'
        self.phone_label = ttk.Label(self.new_window, text=f'Phone: {phone[0:3]}-{phone[3:6]}-{phone[6:]}')
        self.phone_label.grid(column=0, row=1, sticky='WE', **options)
        self.email_label = ttk.Label(self.new_window, text=f'Email: {employee[21]}')
        self.email_label.grid(column=2, row=1, sticky='WE', **options)
        about_me = employee[24].lstrip('"').rstrip('"')
        self.about_me_label = ttk.Label(self.new_window, text=f'About Me: {about_me}')
        self.about_me_label.grid(column=0, columnspan=3, row=2, sticky='WE', **options)

        self.exit_button = ttk.Button(self.new_window, text='Exit')
        self.exit_button.grid(column=2,row=3, sticky='SE', **options)
        self.exit_button.configure(command=lambda: self.new_window.destroy())

        self.help_button = ttk.Button(self.new_window, text='Help')
        self.help_button.grid(column=0, row=3, sticky='SW', **options)
        self.help_button.configure(command=self.base_view_help)

    def base_view_help(self):
        options = {'padx':5, 'pady':5}

        self.new_window = tk.Toplevel(app)
        self.new_window.title('Help Page')
        self.new_window.geometry('260x200')

        self.header = ttk.Label(self.new_window, text='Help Menu', font=('default', 18, 'bold', 'underline'), foreground='blue', anchor='center')
        self.header.grid(column=0, row=0, padx='5', pady='15')
    
        self.personal_button = ttk.Button(self.new_window, text='Selected Employee Info')
        self.personal_button.grid(column=0, row=1, **options)
        self.personal_button.configure(width=40)
        
        self.grid_columnconfigure(0, weight=1)
        
    def view_employee_admin(self, employee):
        # Passed argument is list for that employee
        # Creates Toplevel window labels and entry boxes
        # Entry boxes are prepopulated with that employees info, empty if None
        # Same layout as add_employee window
        options = {'padx':5, 'pady':5}
        self.new_window = tk.Toplevel(app)
        self.new_window.title(f'Viewing {employee[1]} {employee[2]}')
        self.new_window.geometry('1100x640')
        self.string_vars = {}
        for index in range(len(employee)):
            if employee[index] == '':
                fill_string = ''
            else:
                fill_string = str(employee[index])
                if fill_string.startswith('"'):
                    fill_string = fill_string.lstrip('"')
                if fill_string.endswith('"'):
                    fill_string = fill_string.rstrip('"')
            self.string_vars[index] = tk.StringVar()
            self.string_vars[index].set(fill_string)
        #Employee Id Number
        self.id_label = ttk.Label(self.new_window, text='ID:')
        self.id_label.grid(column=0, row=0, sticky='EW', **options)
        self.id_entry = ttk.Label(self.new_window, text=self.string_vars[0].get())
        self.id_entry.grid(column=1, row=0, **options)
        self.id_entry.focus()
        #First Name
        self.first_name_label = ttk.Label(self.new_window, text='First Name:')
        self.first_name_label.grid(column=0, row=1, sticky='EW', **options)
        self.first_name_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[1])
        self.first_name_entry.grid(column=1, row=1, sticky='W', **options)
        #Last Name
        self.last_name_label = ttk.Label(self.new_window, text='Last Name:')
        self.last_name_label.grid(column=2, row=1, sticky='EW', **options)
        self.last_name_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[2])
        self.last_name_entry.grid(column=3, row=1, sticky='W', **options)
        self.name_warning = ttk.Label(self.new_window, text='')
        self.name_warning.grid(row=1, column=4, columnspan=2, sticky='EW', **options)
        #Address
        self.address_label = ttk.Label(self.new_window, text='Address:')
        self.address_label.grid(column=0, row=2, sticky='EW', **options)
        self.address_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[3])
        self.address_entry.grid(column=1, row=2, sticky='W', **options)
        #City
        self.city_label = ttk.Label(self.new_window, text='City:')
        self.city_label.grid(column=2, row=2, sticky='EW', **options)
        self.city_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[4])
        self.city_entry.grid(column=3, row=2, sticky='W', **options)
        self.address_warning = ttk.Label(self.new_window, text='')
        self.address_warning.grid(column=4, row=2, columnspan=2, sticky='EW', **options)
        #State Dropdown
        self.state_label = ttk.Label(self.new_window, text='State:')
        self.state_label.grid(column=0, row=3, sticky='EW', **options)
        self.state_entry = tk.OptionMenu(self.new_window, self.string_vars[5], *STATES)
        self.state_entry.grid(column=1, row=3, sticky='W', **options)
        #ZIP Code
        self.zip_label = ttk.Label(self.new_window, text='Zip:')
        self.zip_label.grid(column=2, row=3, sticky='EW', **options)
        self.zip_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[6])
        self.zip_entry.grid(column=3, row=3, sticky='W', **options)
        self.zip_warning = ttk.Label(self.new_window, text='')
        self.zip_warning.grid(row=3, column=4, columnspan=2, sticky='EW', **options)
        #Classification Dropdown
        self.classification_label = ttk.Label(self.new_window, text='Classification(1-Hourly, 2-Commissioned, 3-Salary):')
        self.classification_label.grid(column=0, row=4, columnspan=3, sticky='EW', **options)
        self.classification_entry = tk.OptionMenu(self.new_window, self.string_vars[7], *CLASSES)
        self.classification_entry.grid(column=3, row=4, sticky='W', **options)
        #Payment Method
        self.pay_method_label = ttk.Label(self.new_window, text='Pay Method(1-Mailed, 2-ACH):')
        self.pay_method_label.grid(column=0, row=5, columnspan=3, sticky='EW', **options)
        self.pay_method_entry = tk.OptionMenu(self.new_window, self.string_vars[8], *PAY_TYPES)
        self.pay_method_entry.grid(column=3, row=5, sticky='W', **options)
        #Salary
        self.salary_label = ttk.Label(self.new_window, text='Salary:')
        self.salary_label.grid(column=0, row=6, sticky='EW', **options)
        self.salary_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[9])
        self.salary_entry.grid(column=1, row=6, sticky='W', **options)
        self.salary_warning = ttk.Label(self.new_window, text='')
        self.salary_warning.grid(column=0, row=7, columnspan=2, sticky='EW', **options)
        #Hourly Rate
        self.hourly_label = ttk.Label(self.new_window, text='Hourly Rate:')
        self.hourly_label.grid(column=2, row=6, sticky='EW', **options)
        self.hourly_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[10])
        self.hourly_entry.grid(column=3, row=6, sticky='W', **options)
        self.hourly_warning = ttk.Label(self.new_window, text='')
        self.hourly_warning.grid(column=2, row=7, columnspan=2, sticky='EW', **options)
        #Commission
        self.commission_label = ttk.Label(self.new_window, text='Commission:')
        self.commission_label.grid(column=4, row=6, sticky='EW', **options)
        self.commission_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[11])
        self.commission_entry.grid(column=5, row=6, sticky='W', **options)
        self.commission_warning = ttk.Label(self.new_window, text='')
        self.commission_warning.grid(column=4, row=7, columnspan=2, sticky='EW', **options)
        #Routing Number
        self.route_label = ttk.Label(self.new_window, text='Routing Number:')
        self.route_label.grid(column=0, row=8, sticky='EW', **options)
        self.route_entry = ttk.Entry(self.new_window, width=40, textvariable=self.string_vars[12])
        self.route_entry.grid(column=1, row=8, columnspan=2, sticky='W', **options)
        #Bank Account Number
        self.account_label = ttk.Label(self.new_window, text='Account Number:')
        self.account_label.grid(column=0, row=9, sticky='EW', **options)
        self.account_entry = ttk.Entry(self.new_window, width=40, textvariable=self.string_vars[13])
        self.account_entry.grid(column=1, row=9, columnspan=2, sticky='W', **options)
        #Phone Number
        self.phone_label = ttk.Label(self.new_window, text='Phone Number:')
        self.phone_label.grid(column=0, row=10, sticky='EW', **options)
        self.phone_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[14])
        self.phone_entry.grid(column=1, row=10, sticky='W', **options)
        self.phone_warning = ttk.Label(self.new_window, text='')
        self.phone_warning.grid(column=0, row=11, columnspan=2, sticky='EW', **options)
        #Date of Birth
        self.dob_label = ttk.Label(self.new_window, text='Date of Birth (mm/dd/yyyy):')
        self.dob_label.grid(column=2, row=10, sticky='EW', **options)
        self.dob_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[15])
        self.dob_entry.grid(column=3, row=10, sticky='W', **options)
        self.dob_warning = ttk.Label(self.new_window, text='')
        self.dob_warning.grid(column=2, row=11, columnspan=2, sticky='EW', **options)
        #Social Security Number
        self.ssn_label = ttk.Label(self.new_window, text='Social Security Number:')
        self.ssn_label.grid(column=4, row=10, sticky='EW', **options)
        self.ssn_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[16])
        self.ssn_entry.grid(column=5, row=10, sticky='W', **options)
        self.ssn_warning = ttk.Label(self.new_window, text='')
        self.ssn_warning.grid(column=4, row=11, columnspan=2, sticky='EW', **options)
        #Start Date
        self.start_date_label = ttk.Label(self.new_window, text='Start Date (mm/dd/yyyy):')
        self.start_date_label.grid(column=0, row=12, sticky='EW', **options)
        self.start_date_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[17])
        self.start_date_entry.grid(column=1, row=12, sticky='W', **options)
        self.start_date_warning = ttk.Label(self.new_window, text='')
        self.start_date_warning.grid(column=0, row=13, columnspan=2, sticky='EW', **options)
        #Permission Level
        self.permission_label = ttk.Label(self.new_window, text='Permission Level(1-Admin, 2-Regular):')
        self.permission_label.grid(column=2, row=12, columnspan=2, sticky='EW', **options)
        self.permission_entry = tk.OptionMenu(self.new_window, self.string_vars[18], *PERMISSION)
        self.permission_entry.grid(column=4, row=12, sticky='W', **options)
        #Job Title
        self.job_title_label = ttk.Label(self.new_window, text='Job Title:')
        self.job_title_label.grid(column=0, row=14, sticky='EW', **options)
        self.job_title_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[19])
        self.job_title_entry.grid(column=1, row=14, sticky='W', **options)
        #Department
        self.department_label = ttk.Label(self.new_window, text='Department:')
        self.department_label.grid(column=2, row=14, sticky='EW', **options)
        self.department_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[20])
        self.department_entry.grid(column=3, row=14, sticky='W', **options)
        #Email
        self.email_label = ttk.Label(self.new_window, text='Work Email:')
        self.email_label.grid(column=4, row=14, sticky='EW', **options)
        self.email_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[21])
        self.email_entry.grid(column=5, row=14, sticky='W', **options)
        #Earnings
        self.earnings_label = ttk.Label(self.new_window, text='Earning to Date:')
        self.earnings_label.grid(column=0, row=15, sticky='EW', **options)
        self.earnings_value = ttk.Label(self.new_window, text=employee[22])
        self.earnings_value.grid(column=1, row=15, sticky='W', **options)
        #About me
        self.about_me_label = ttk.Label(self.new_window, text=f'About Me:')
        self.about_me_label.grid(column=0, row=16, sticky='WE', **options)
        self.about_me_entry = ttk.Entry(self.new_window, textvariable=self.string_vars[24])
        self.about_me_entry.grid(column=1, columnspan=3, row=16, sticky='W', **options)
        #Submit and Cancel Buttons
        self.submit_button = ttk.Button(self.new_window, text='Submit')
        self.submit_button.grid(column=0, row=17, sticky='S', **options)
        self.submit_button.configure(command=lambda: self.submit_edit(employee))
        self.cancel_button = ttk.Button(self.new_window, text='Cancel')
        self.cancel_button.grid(column=1, row=17, sticky='S', **options)
        self.cancel_button.configure(command=lambda: self.new_window.destroy())
        #Help Button
        self.help_button = ttk.Button(self.new_window, text='Help')
        self.help_button.grid(column=0, row=18, sticky='SW', **options)
        self.help_button.configure(command=self.view_help)
        
        self.grid(column=0, row=0, padx=5, pady=5, sticky='NSEW')

    def view_help(self):
        self.profile_img = Image.open(EDIT_EMP_IMG)
        self.profile_img.show()
       
    def submit_edit(self, employee):
        if self.validate_employee_form(self.string_vars):
            for index in range(len(employee)):
                value = self.string_vars[index].get().strip()
                if value == '':
                    value = ''
                    employee[index] = value
                    continue
                if index == 24:
                    value = f'"{value}"'
                    employee[index] = value
                elif value !=  employee[index]:
                    employee[index] = value
            self.controller.update_employee_info(employee)
            self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')
            self.new_window.destroy()

    def add_employee(self):

        options = {'padx':5, 'pady':5}
        self.new_window = tk.Toplevel(app)
        self.new_window.title('Add Employee')
        self.new_window.geometry('1100x600')

        self.stringVars = []
        self.id = tk.StringVar()
        self.stringVars.append(self.id)
        self.first_name = tk.StringVar()
        self.stringVars.append(self.first_name)
        self.last_name = tk.StringVar()
        self.stringVars.append(self.last_name)
        self.address = tk.StringVar()
        self.stringVars.append(self.address)
        self.city = tk.StringVar()
        self.stringVars.append(self.city)
        self.state = tk.StringVar()
        self.stringVars.append(self.state)
        self.zip = tk.StringVar()
        self.stringVars.append(self.zip)
        self.classification = tk.StringVar()
        self.stringVars.append(self.classification)
        self.pay_method = tk.StringVar()
        self.stringVars.append(self.pay_method)
        self.salary = tk.StringVar()
        self.stringVars.append(self.salary)
        self.hourly = tk.StringVar()
        self.stringVars.append(self.hourly)
        self.commission = tk.StringVar()
        self.stringVars.append(self.commission)
        self.route = tk.StringVar()
        self.stringVars.append(self.route)
        self.account = tk.StringVar()
        self.stringVars.append(self.account)
        self.phone = tk.StringVar()
        self.stringVars.append(self.phone)
        self.dob = tk.StringVar()
        self.stringVars.append(self.dob)
        self.ssn = tk.StringVar()
        self.stringVars.append(self.ssn)
        self.start_date = tk.StringVar()
        self.stringVars.append(self.start_date)
        self.permission_level = tk.StringVar(value = PERMISSION[2])
        self.stringVars.append(self.permission_level)
        self.job_title = tk.StringVar()
        self.stringVars.append(self.job_title)
        self.department = tk.StringVar()
        self.stringVars.append(self.department)
        self.email = tk.StringVar()
        self.stringVars.append(self.email)
        
        self.id_label = ttk.Label(self.new_window, text='ID:')
        self.id_label.grid(column=0, row=0, sticky='EW', **options)
        self.id_entry = ttk.Entry(self.new_window, textvariable=self.id)
        self.id_entry.grid(column=1, row=0, **options)
        self.id_warning = ttk.Label(self.new_window, text='')
        self.id_warning.grid(row=0, column=2, columnspan=2, sticky='EW', **options)
        self.id_entry.focus()
        
        self.first_name_label = ttk.Label(self.new_window, text='First Name:')
        self.first_name_label.grid(column=0, row=1, sticky='EW', **options)
        self.first_name_entry = ttk.Entry(self.new_window, textvariable=self.first_name)
        self.first_name_entry.grid(column=1, row=1, sticky='W', **options)

        self.last_name_label = ttk.Label(self.new_window, text='Last Name:')
        self.last_name_label.grid(column=2, row=1, sticky='EW', **options)
        self.last_name_entry = ttk.Entry(self.new_window, textvariable=self.last_name)
        self.last_name_entry.grid(column=3, row=1, sticky='W', **options)
        self.name_warning = ttk.Label(self.new_window, text='', background='white')
        self.name_warning.grid(row=1, column=4, columnspan=2, sticky='EW', **options)

        self.address_label = ttk.Label(self.new_window, text='Address:')
        self.address_label.grid(column=0, row=2, sticky='EW', **options)
        self.address_entry = ttk.Entry(self.new_window, textvariable=self.address)
        self.address_entry.grid(column=1, row=2, sticky='W', **options)

        self.city_label = ttk.Label(self.new_window, text='City:')
        self.city_label.grid(column=2, row=2, sticky='EW', **options)
        self.city_entry = ttk.Entry(self.new_window, textvariable=self.city)
        self.city_entry.grid(column=3, row=2, sticky='W', **options)
        self.address_warning = ttk.Label(self.new_window, text='')
        self.address_warning.grid(column=4, row=2, columnspan=2, sticky='EW', **options)

        self.state_label = ttk.Label(self.new_window, text='State:')
        self.state_label.grid(column=0, row=3, sticky='EW', **options)
        self.state_entry = tk.OptionMenu(self.new_window, self.state, *STATES)
        self.state_entry.grid(column=1, row=3, sticky='W', **options)

        self.zip_label = ttk.Label(self.new_window, text='Zip:')
        self.zip_label.grid(column=2, row=3, sticky='EW', **options)
        self.zip_entry = ttk.Entry(self.new_window, textvariable=self.zip)
        self.zip_entry.grid(column=3, row=3, sticky='W', **options)
        self.zip_warning = ttk.Label(self.new_window, text='', background='white')
        self.zip_warning.grid(row=3, column=4, columnspan=2, sticky='EW', **options)

        self.classification_label = ttk.Label(self.new_window, text='Classification(1-Hourly, 2-Commissioned, 3-Salary):')
        self.classification_label.grid(column=0, row=4, columnspan=3, sticky='EW', **options)
        self.classification_entry = tk.OptionMenu(self.new_window, self.classification, *CLASSES)
        self.classification_entry.grid(column=3, row=4, sticky='W', **options)

        self.pay_method_label = ttk.Label(self.new_window, text='Pay Method(1-Mailed, 2-ACH):')
        self.pay_method_label.grid(column=0, row=5, columnspan=3, sticky='EW', **options)
        self.pay_method_entry = tk.OptionMenu(self.new_window, self.pay_method, *PAY_TYPES)
        self.pay_method_entry.grid(column=3, row=5, sticky='W', **options)

        self.salary_label = ttk.Label(self.new_window, text='Salary:')
        self.salary_label.grid(column=0, row=6, sticky='EW', **options)
        self.salary_entry = ttk.Entry(self.new_window, textvariable=self.salary)
        self.salary_entry.grid(column=1, row=6, sticky='W', **options)
        self.salary_warning = ttk.Label(self.new_window, text='')
        self.salary_warning.grid(column=0, row=7, columnspan=2, sticky='EW', **options)

        self.hourly_label = ttk.Label(self.new_window, text='Hourly Rate:')
        self.hourly_label.grid(column=2, row=6, sticky='EW', **options)
        self.hourly_entry = ttk.Entry(self.new_window, textvariable=self.hourly)
        self.hourly_entry.grid(column=3, row=6, sticky='W', **options)
        self.hourly_warning = ttk.Label(self.new_window, text='')
        self.hourly_warning.grid(column=2, row=7, columnspan=2, sticky='EW', **options)

        self.commission_label = ttk.Label(self.new_window, text='Commission:')
        self.commission_label.grid(column=4, row=6, sticky='EW', **options)
        self.commission_entry = ttk.Entry(self.new_window, textvariable=self.commission)
        self.commission_entry.grid(column=5, row=6, sticky='W', **options)
        self.commission_warning = ttk.Label(self.new_window, text='')
        self.commission_warning.grid(column=4, row=7, columnspan=2, sticky='EW', **options)

        self.route_label = ttk.Label(self.new_window, text='Routing Number:')
        self.route_label.grid(column=0, row=8, sticky='EW', **options)
        self.route_entry = ttk.Entry(self.new_window, width=40, textvariable=self.route)
        self.route_entry.grid(column=1, row=8, columnspan=2, sticky='W', **options)
        self.route_warning = ttk.Label(self.new_window, text='')
        self.route_warning.grid(column=3, row=8, columnspan=2, sticky='EW', **options)

        self.account_label = ttk.Label(self.new_window, text='Account Number:')
        self.account_label.grid(column=0, row=9, sticky='EW', **options)
        self.account_entry = ttk.Entry(self.new_window, width=40, textvariable=self.account)
        self.account_entry.grid(column=1, row=9, columnspan=2, sticky='W', **options)
        self.account_warning = ttk.Label(self.new_window, text='')
        self.account_warning.grid(column=3, row=9, columnspan=2, sticky='EW', **options)

        self.phone_label = ttk.Label(self.new_window, text='Phone Number:')
        self.phone_label.grid(column=0, row=10, sticky='EW', **options)
        self.phone_entry = ttk.Entry(self.new_window, textvariable=self.phone)
        self.phone_entry.grid(column=1, row=10, sticky='W', **options)
        self.phone_warning = ttk.Label(self.new_window, text='')
        self.phone_warning.grid(column=0, row=11, columnspan=2, sticky='EW', **options)

        self.dob_label = ttk.Label(self.new_window, text='Date of Birth:')
        self.dob_label.grid(column=2, row=10, sticky='EW', **options)
        self.dob_entry = ttk.Entry(self.new_window, textvariable=self.dob)
        self.dob_entry.grid(column=3, row=10, sticky='W', **options)
        self.dob_warning = ttk.Label(self.new_window, text='')
        self.dob_warning.grid(column=2, row=11, columnspan=2, sticky='EW', **options)

        self.ssn_label = ttk.Label(self.new_window, text='Social Security Number:')
        self.ssn_label.grid(column=4, row=10, sticky='EW', **options)
        self.ssn_entry = ttk.Entry(self.new_window, textvariable=self.ssn)
        self.ssn_entry.grid(column=5, row=10, sticky='W', **options)
        self.ssn_warning = ttk.Label(self.new_window, text='')
        self.ssn_warning.grid(column=4, row=11, columnspan=2, sticky='EW', **options)

        self.start_date_label = ttk.Label(self.new_window, text='Start Date:')
        self.start_date_label.grid(column=0, row=12, sticky='EW', **options)
        self.start_date_entry = ttk.Entry(self.new_window, textvariable=self.start_date)
        self.start_date_entry.grid(column=1, row=12, sticky='W', **options)
        self.start_date_warning = ttk.Label(self.new_window, text='')
        self.start_date_warning.grid(column=0, row=13, columnspan=2, sticky='EW', **options)

        self.permission_label = ttk.Label(self.new_window, text='Permission Level(1-Admin, 2-Regular):')
        self.permission_label.grid(column=2, row=12, columnspan=2, sticky='EW', **options)
        self.permission_entry = tk.OptionMenu(self.new_window, self.permission_level, *PERMISSION)
        self.permission_entry.grid(column=4, row=12, sticky='W', **options)

        self.job_title_label = ttk.Label(self.new_window, text='Job Title:')
        self.job_title_label.grid(column=0, row=14, sticky='EW', **options)
        self.job_title_entry = ttk.Entry(self.new_window, textvariable=self.job_title)
        self.job_title_entry.grid(column=1, row=14, sticky='W', **options)

        self.department_label = ttk.Label(self.new_window, text='Department:')
        self.department_label.grid(column=2, row=14, sticky='EW', **options)
        self.department_entry = ttk.Entry(self.new_window, textvariable=self.department)
        self.department_entry.grid(column=3, row=14, sticky='W', **options)

        self.email_label = ttk.Label(self.new_window, text='Work Email:')
        self.email_label.grid(column=4, row=14, sticky='EW', **options)
        self.email_entry = ttk.Entry(self.new_window, textvariable=self.email)
        self.email_entry.grid(column=5, row=14, sticky='W', **options)

        self.submit_button = ttk.Button(self.new_window, text='Submit')
        self.submit_button.grid(column=0, row=15, sticky='S', **options)
        self.submit_button.configure(command=self.submit_add)
        self.cancel_button = ttk.Button(self.new_window, text='Cancel')
        self.cancel_button.grid(column=1, row=15, sticky='S', **options)
        self.cancel_button.configure(command=lambda: self.new_window.destroy())
        self.grid(column=0, row=0, padx=5, pady=5, sticky='NSEW')

        self.help_button = ttk.Button(self.new_window, text='Help')
        self.help_button.grid(column=0, row=18, sticky='SW', **options)
        self.help_button.configure(command=self.add_help)

    def add_help(self):
        self.profile_img = Image.open(ADD_EMP_IMG)
        self.profile_img.show()
    def submit_add(self):
        if self.validate_employee_form(self.stringVars):
            if self.check_duplicate_id(self.id):
                new_emp = []
                for vars in self.stringVars:
                    var = vars.get()
                    if var == '':
                        var = ''
                    new_emp.append(var)
                new_emp.append('0.00') # Add earnings to date
                new_emp.append('False') # Add Archived Status
                new_emp.append('') # Add "About Me" value of ''
                self.controller.add_new_employee(new_emp)
                self.controller.add_password(new_emp[0])
                self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')
                self.new_window.destroy()

    def check_duplicate_id(self, empid_var):
        empid = empid_var.get()
        self.controller.get_employee_info('*', True)
        employees = self.controller.employee_info + [self.controller.user_info]
        for emp in employees:
            if empid == emp[0]:
                self.id_warning['text'] = 'Entered ID already belongs to another employee'
                return False
        return True

    def validate_employee_form(self, entries):
        indices = range(len(EMPLOYEES_HEADER)-3)
        self.id_warning['text'] = ''
        valid = True
        for index in indices:
            value = entries[index].get().strip()
            if index == 0: # Validate ID
                if value == '':
                    valid = False
                    self.id_label.configure(foreground='red')
                    self.id_warning['text'] = 'ID is Required'
                    continue
                idValidation = "^\d{6}$" # 6 digit ID number
                if re.search(idValidation, value):
                    self.id_label.configure(foreground='black')
                    self.id_warning['text'] = ''
                    continue
                else:
                    valid = False
                    self.id_label.configure(foreground='red')
                    self.id_warning['text'] = 'ID should be a 6 digit number. Ex: "652347"'
                    continue
            # Validate first and last name fields - Required Fields
            elif index == 1 or index == 2:
                if value == '':
                    valid = False
                    self.name_warning['text'] = 'First and Last name are required.'
                    if index == 1:
                        self.first_name_label.configure(foreground='red')
                        continue
                    else:
                        self.last_name_label.configure(foreground='red')
                        continue
                else:
                    self.name_warning['text'] = ''
                    if index == 1:
                        self.first_name_label.configure(foreground='black')
                        continue
                    else:
                        self.last_name_label.configure(foreground='black')
                        continue
            # Validate Zip Code
            elif index == 6:
                if value == '':
                    self.zip_label.configure(foreground='black')
                    self.zip_warning['text'] = ''
                    continue
                zipValidation = "^\d{5}$"
                if re.search(zipValidation, value):
                    self.zip_label.configure(foreground='black')
                    self.zip_warning['text'] = ''
                    continue
                else:
                    valid = False
                    self.zip_warning['text'] = 'Zip code must be a 5 digit number. Ex: "54047"'
                    self.zip_label.configure(foreground='red')
                    continue
            # Validate Salary Entry and Hourly Rate entry
            elif index == 9 or index == 10:
                if value == '':
                    continue
                moneyValidationDecimal = "^\d+\.\d{2}$" # Validates a floating point with 2 decimal places
                moneyValidationNoDecimal = "^\d+$"
                if re.search(moneyValidationDecimal, value):
                    if index == 9:
                        self.salary_label.configure(foreground='black')
                        self.salary_warning['text'] = ''
                    else:
                        self.hourly_label.configure(foreground='black')
                        self.hourly_warning['text'] = ''
                    continue
                elif re.search(moneyValidationNoDecimal, value):
                    entries[index].set(value + '.00')
                    if index == 9:
                        self.salary_label.configure(foreground='black')
                        self.salary_warning['text'] = ''
                    else:
                        self.hourly_label.configure(foreground='black')
                        self.hourly_warning['text'] = ''
                    continue
                else:
                    valid = False
                    if index == 9:
                        self.salary_warning['text'] = 'Must be a dollar amount with no commas. Ex: "65000.00"'
                        self.salary_label.configure(foreground='red')
                    else:
                        self.hourly_warning['text'] = 'Must be a dollar amount. Ex: "25.50"'
                        self.hourly_label.configure(foreground='red')
                    continue
            # Validate Commission Entry
            elif index == 11:
                if value == '':
                    self.commission_warning['text'] = ''
                    self.commission_label.configure(foreground='black')
                    continue
                integerValidation = "^\d+$"
                if re.search(integerValidation, value) and int(value) in range(1, 100):
                    self.commission_label.configure(foreground='black')
                    self.commission_warning['text'] = ''
                    continue
                else:
                    valid = False
                    self.commission_warning['text'] = 'Must be an integer amount. Ex: "25" or "30"'
                    self.commission_label.configure(foreground='red')
                    continue
            # Validate Routing number
            elif index == 12:
                if value == '':
                    self.route_label.configure(foreground='black')
                    self.route_warning['text'] = ''
                    continue
                routeValidation = "^\d{8}-?\w$"
                if re.search(routeValidation, value):
                    self.route_warning['text'] = ''
                    self.route_label.configure(foreground='black')
                    continue
                else:
                    valid = False
                    self.route_warning['text'] = 'Must be 8 digits followed by 1 alphanumeric character. Ex: "12345678-A" or "12345678A"'
                    self.route_label.configure(foreground='red')
                    continue
            # Validate Account number
            elif index == 13:
                if value == '':
                    self.account_warning['text'] = ''
                    self.account_label.configure(foreground='black')
                    continue
                accountValidation = "^\d{6}-?\d{4}$"
                if re.search(accountValidation, value):
                    self.account_warning['text'] = ''
                    self.account_label.configure(foreground='black')
                    continue
                else:
                    valid = False
                    self.account_warning['text'] = 'Must be 10 digit number. Ex: "123456-7890" or "1234567890"'
                    self.account_label.configure(foreground='red')
                    continue
            # Validate phone number
            elif index == 14:
                if value == '':
                    self.phone_label.configure(foreground='black')
                    self.phone_warning['text'] = ''
                    continue
                phoneValidation = "^\d{3}-?\d{3}-?\d{4}$"
                if re.search(phoneValidation, value):
                    value = value.replace('-', '')
                    entries[index].set(value)
                    self.phone_warning['text'] = ''
                    self.phone_label.configure(foreground='black')
                    continue
                else:
                    valid = False
                    self.phone_warning['text'] = 'Must be 10 digits. Ex: 555-555-5555 or 9876543210'
                    self.phone_label.configure(foreground='red')
                    continue
            # Validate SSN
            elif index == 16:
                if value == '':
                    self.ssn_warning['text'] = ''
                    self.ssn_label.configure(foreground='black')
                    continue
                ssnValidation = "^\d{3}-?\d{2}-?\d{4}$"
                if re.search(ssnValidation, value):
                    value = value.replace('-', '')
                    entries[index].set(value)
                    self.ssn_warning['text'] = ''
                    self.ssn_label.configure(foreground='black')
                    continue
                else:
                    valid = False
                    self.ssn_warning['text'] = 'Must be 9 digits. Ex: 555-55-5555 or 123456789'
                    self.ssn_label.configure(foreground='red')
                    continue
            # Validate dates (DOB and start date)
            elif index == 15 or index == 16:
                if value == '':
                    continue
                dateValidation = "^(\d{2})/(\d{2})/(\d{4})$"
                result = re.search(dateValidation, value)
                if result:
                    month = int(result.group(1))
                    date = int(result.group(2))
                    year = int(result.group(3))
                    if year < CURRENT_YEAR:
                        if month in [1, 3, 5, 7, 8, 10, 12]:
                            if date in range(1, 32):
                                if index == 15:
                                    self.dob_warning['text'] = ''
                                    self.dob_label.configure(foreground='black')
                                else:
                                    self.start_date_warning['text'] = ''
                                    self.start_date_label.configure(foreground='black')
                                continue
                            else: # Not valid day for those months
                                valid = False
                                if index == 15:
                                    self.dob_warning['text'] = 'Not a valid date'
                                    self.dob_label.configure(foreground='red')
                                else:
                                    self.start_date_warning['text'] = 'Not a valid date'
                                    self.start_date_label.configure(foreground='red')
                        elif month == 2:
                            if date in range(1, 30):
                                if index == 15:
                                    self.dob_warning['text'] = ''
                                    self.dob_label.configure(foreground='black')
                                else:
                                    self.start_date_warning['text'] = ''
                                    self.start_date_label.configure(foreground='black')
                                continue
                            else: # Not a valid day for February
                                valid = False
                                if index == 15:
                                    self.dob_warning['text'] = 'Not a valid date'
                                    self.dob_label.configure(foreground='red')
                                else:
                                    self.start_date_warning['text'] = 'Not a valid date'
                                    self.start_date_label.configure(foreground='red')
                        elif month in [4, 6, 9, 11]:
                            if date in range(1, 31):
                                if index == 15:
                                    self.dob_warning['text'] = ''
                                    self.dob_label.configure(foreground='black')
                                else:
                                    self.start_date_warning['text'] = ''
                                    self.start_date_label.configure(foreground='black')
                                continue
                            else: # Not a valid day for those months
                                valid = False
                                if index == 15:
                                    self.dob_warning['text'] = 'Not a valid date'
                                    self.dob_label.configure(foreground='red')
                                else:
                                    self.start_date_warning['text'] = 'Not a valid date'
                                    self.start_date_label.configure(foreground='red')
                        else: # Not a valid month
                            valid = False
                            if index == 15:
                                self.dob_warning['text'] = 'Not a valid date'
                                self.dob_label.configure(foreground='red')
                            else:
                                self.start_date_warning['text'] = 'Not a valid date'
                                self.start_date_label.configure(foreground='red')
                    else: # Not a valid year
                        valid = False
                        if index == 15:
                            self.dob_warning['text'] = 'Not a valid date'
                            self.dob_label.configure(foreground='red')
                        else:
                            self.start_date_warning['text'] = 'Not a valid date'
                            self.start_date_label.configure(foreground='red')
                else: # Didn't pass Regex
                    valid = False
                    if index == 15:
                        self.dob_warning['text'] == 'Must be in mm/dd/yyyy format'
                        self.dob_label.configure(foreground='red')
                    else:
                        self.start_date_warning['text'] = 'Must be in mm/dd/yyyy format'
                        self.start_date_label.configure(foreground='red')

        # If classification is 1 then must have hourly amount
        if entries[7].get() == '1':
            if entries[10].get() == '':
                valid = False
                self.hourly_label.configure(foreground='red')
                self.hourly_warning['text'] = 'HOURLY RATE REQUIRED FOR HOURLY EMPLOYEE'
        # If classification is 2 then must have a salary
        elif entries[7].get() == '2':
            if entries[9].get() == '':
                valid = False
                self.salary_label.configure(foreground='red')
                self.salary_warning['text'] = 'SALARY REQUIRED FOR SALARY EMPLOYEE'
        # If classification is 3 then must have a salary and commission
        elif entries[7].get() == '3':
            if entries[9].get() == '':
                valid = False
                self.salary_label.configure(foreground='red')
                self.salary_warning['text'] = 'SALARY REQUIRED FOR SALARY EMPLOYEE'
            if entries[11].get() == '':
                valid = False
                self.commission_label.configure(foreground='red')
                self.commission_warning['text'] = 'COMMISSION RATE REQUIRED FOR SALARY EMPLOYEE'
        
        # If paymethod is 1 then must have address info
        if entries[8].get() == '1':
            if entries[3].get() == '' or entries[4].get() == '' or entries[5].get() == '' or entries[6].get() == '':
                self.address_label.configure(foreground='red')
                valid = False
                self.address_warning['text'] = 'ADDRESS REQUIRED FOR MAILED PAY'
        # If paymethod is 2 then must have routing and account numbers
        elif entries[8].get() == '2':
            if entries[12].get() == '':
                self.route_label.configure(foreground='red')
                valid = False
                self.route_warning['text'] = 'ROUTING NUMBER REQUIRED FOR ACH PAY'
            if entries[13].get() == '':
                valid = False
                self.account_label.configure(foreground='red')
                self.account_warning['text'] = 'ACCOUNT NUMBER REQUIRED FOR ACH PAY'
        
        return valid

    def archive_employee(self, employee):
        if employee[23] == 'True':
            tk.messagebox.showinfo(title='Error', message='Selected Employee is already archived.')
            return
        if tk.messagebox.askokcancel(title='Confirm Archive', 
                                    message=f'Are you sure you wish to archive {employee[1]} {employee[2]}?', 
                                    icon='warning', default='ok'):
            employee[23] = 'True'
            self.controller.update_employee_info(employee)
            self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')
        else:
            self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')
    
    def unarchive_employee(self, employee):
        if employee[23] != 'True':
            tk.messagebox.showinfo(title='Error', message='Selected Employee is not archived.')
            return
        if tk.messagebox.askokcancel(title='Confirm Unarchive', 
                                    message=f'Are you sure you wish to unarchive {employee[1]} {employee[2]}?', 
                                    icon='warning', default='ok'):
            employee[23] = 'False'
            self.controller.update_employee_info(employee)
            self.controller.show_frame('EMPLOYEE_SEARCH_FRAME')

class LOGIN_FRAME(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = tk.StringVar()
        self.password = tk.StringVar()
        
        options = {'padx': 5, 'pady': 5}
        self.id_label = ttk.Label(self, text='ID:')
        self.id_label.grid(column=1, row=1, sticky='W', **options)
        #ID Entry
        self.id_entry = ttk.Entry(self, textvariable=self.id)
        self.id_entry.grid(column=2, row=1, sticky='W', **options)
        self.id_entry.focus()
        #Password Entry
        self.password_label = ttk.Label(self, text='Password:')
        self.password_label.grid(column=1, row=2, sticky='W', **options)
        self.password_entry = ttk.Entry(self, show='*', textvariable=self.password)
        self.password_entry.grid(column=2, row=2, **options)
        #Login Button
        self.login_button = ttk.Button(self, text='Login')
        self.login_button.grid(column=1, row=3, sticky='W', **options)
        self.login_button.configure(command=lambda: self.verify(self.id_entry.get(), self.password_entry.get()))
        self.grid(padx=5, pady=5, sticky='NSEW')
        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=1, row=4, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)

        self.id_entry.bind("<KeyRelease-Return>", self.moveToPassword)

        self.password_entry.bind("<KeyRelease-Return>", self.enterPress)

    def help(self):
        self.profile_img = Image.open(LOGIN_IMG)
        self.profile_img.show()

    def moveToPassword(self, key):
        self.password_entry.focus()

    def enterPress(self, key):
        self.verify(self.id_entry.get(), self.password_entry.get())

    def verify(self, empid, password):
        global PASSWORD_CSV
        with open(PASSWORD_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                if row[0] == 'ID':
                    continue
                elif row[0] == empid:
                    if row[1] == password:
                        if self.verify_not_archived(empid):
                            return self.successful_login(empid)
                        else:
                            return
                    else:
                        break
        self.failed_login('Incorrect Employee ID or Password')

    def verify_not_archived(self, empid):
        '''Function used to verify that the employee trying to login is not archived.'''
        with open(EMPLOYEE_CSV, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                if row[0] == empid:
                    if row[23] == 'True':
                        self.failed_login('You have been archived from the system, cannot login.')
                        return False
                    else:
                        return True


    def successful_login(self, empid):
        '''Function called when the login is successful.
        Gets the employee info for the user and goes to Profile Page Frame'''
        self.controller.get_user_info(empid)
        self.controller.user_permission_level == self.controller.user_info[18]
        self.controller.get_employee_info()
        self.controller.show_frame('PROFILE_INFO_FRAME')

    def failed_login(self, message):
        '''Function called when the login is unsuccessful.
        Provide an appropriate error message as an argument.'''
        self.error_label = ttk.Label(self, text=message)
        self.error_label.grid(column=0, columnspan=3, row=4, sticky='W')

    def update_frame(self):
        '''Sets title to login title. Reset entry boxes to be blank.
        Reset user and employee info to be empty. Reset permission level to 2.'''
        self.controller.title('Employee Login')
        self.id.set('')
        self.password.set('')
        self.controller.user_info = [''] * len(EMPLOYEES_HEADER)
        self.controller.employee_info = []
        self.controller.user_permission_level = 2

class PROFILE_INFO_FRAME(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.user_id = 'EmployeeID'
        self.user_name = 'User Name'
        self.user_job_title = 'Job Title'
        self.user_address = 'Address'
        self.user_phone = 'Phone'
        self.user_email = 'Email'
        
        
        main_options = {'padx':20, 'pady':20, 'ipadx':10, 'ipady':10}

        style = ttk.Style()
        style.configure('Theme.TLabel', borderwidth=4, relief='raised', anchor='center', width=20)

        #ID Label
        self.id_label = ttk.Label(self, text=' Employee ID: ' + self.user_id, style='Theme.TLabel')
        self.id_label.grid(column=0, row=2, **main_options)
        #Name Label
        self.name_label = ttk.Label(self, text='Missing Name', style='Theme.TLabel')
        self.name_label.grid(column=1, row=2, **main_options)
        #Job Title Label
        self.job_label = ttk.Label(self, text='Missing Job Title', style='Theme.TLabel')
        self.job_label.grid(column=2, row=2, **main_options)
        #Address Label
        self.address_label = ttk.Label(self, text='Missing Address', style='Theme.TLabel')
        self.address_label.grid(column=0, row=3, **main_options)
        #Office Phone Label
        self.phone_label = ttk.Label(self, text='Missing Phone Number', style='Theme.TLabel')
        self.phone_label.grid(column=1, row=3, **main_options)
        #Company Email Label
        self.email_label = ttk.Label(self, text='Missing Email', style='Theme.TLabel')
        self.email_label.grid(column=2, row=3, **main_options)

        #About Me Section
        self.about_me_label = ttk.Label(self, text='About Me:')
        self.about_me_label.grid(column=0, row=4, sticky='W', pady=10)
        self.about_me_entry = tk.Text(self, height=10, width=60)
        self.about_me_entry.grid(column=0, row=5, columnspan=2, rowspan=5, sticky='W')
        self.submit_button = ttk.Button(self, text='Submit About Me Info')
        self.submit_button.grid(column=1, row=10, sticky='W', pady=10)
        self.submit_button.configure(command=self.about_me)
        #Edit Personal Information Button
        self.edit_info_button = ttk.Button(self, text='Edit Info')
        self.edit_info_button.grid(column=2, row=6, sticky='E', pady=15, padx=10)
        self.edit_info_button.configure(command=lambda: self.controller.show_frame('EDIT_PERSONAL_INFO'))
        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=0, row=10, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)
        #Logout Button
        self.logout_button = ttk.Button(self, text='Logout')
        self.logout_button.grid(column=2, row=10, sticky='SE')
        self.logout_button.configure(command=self.logout)

        self.grid(column=0, row=1, padx=5, pady=5)

    def logout(self):
        app.show_frame('LOGIN_FRAME')

    def about_me(self):
        self.controller.user_info[24] = f'"{self.about_me_entry.get("1.0", "end-1c")}"'
        self.controller.update_employee_info(self.controller.user_info)

    def help(self):
        self.profile_img = Image.open(PROFILE_IMG)
        self.profile_img.show()
        
    def update_frame(self):
        self.controller.title(f'{self.controller.user_info[1]} {self.controller.user_info[2]} Profile')

        self.id_label.configure(text=f'Employee ID: {self.controller.user_info[0]}')
        if self.controller.user_info[1] != '':
            self.name_label.configure(text=f'{self.controller.user_info[1]} {self.controller.user_info[2]}')
        if self.controller.user_info[19] != '':
            self.job_label.configure(text=f'{self.controller.user_info[19]} - {self.controller.user_info[20]}')
        if self.controller.user_info[3] != '':
            self.address_label.configure(text=f'{self.controller.user_info[3]} {self.controller.user_info[4]}, {self.controller.user_info[5]} {self.controller.user_info[6]}')
        phone = self.controller.user_info[14]
        if phone != '':
            self.phone_label.configure(text=f'{phone[0:3]}-{phone[3:6]}-{phone[6:]}')
        if self.controller.user_info[21] != '':
            self.email_label.configure(text=f'{self.controller.user_info[21]}')
        if self.controller.user_info[24] != '':
            self.about_me_entry.delete("1.0", "end-1c")
            self.about_me_entry.insert(tk.END, self.controller.user_info[24].rstrip('"').lstrip('"'))

class PAYROLL_INFO_FRAME(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        main_options = {'padx':20, 'pady':20, 'ipadx':10, 'ipady':10}

        style = ttk.Style()
        style.configure('Theme.TLabel', borderwidth=4, relief='raised', anchor='center', width=50)
        #Payment type
        self.payment_type_label = ttk.Label(self, text=' Missing Payment Type ', style='Theme.TLabel')
        self.payment_type_label.grid(column=0, row=1, sticky='S', **main_options)
        #Payment Method
        self.payment_method_label = ttk.Label(self, text=' Missing Payment Method ', style='Theme.TLabel')
        self.payment_method_label.grid(column=1, row=1, sticky='S', **main_options)
        #Salary
        self.salary_label = ttk.Label(self, text=' Missing Pay Rate ', style='Theme.TLabel')
        self.salary_label.grid(column=2, row=1, sticky='S', **main_options)
        #Bank Routing Number
        self.routing_number_label = ttk.Label(self, text=' Missing Routing Number ', style='Theme.TLabel')
        self.routing_number_label.grid(column=0, row=2, sticky='S', **main_options)
        #Bank Account Number
        self.bank_account_label = ttk.Label(self, text=' Missing Bank Account # ', style='Theme.TLabel')
        self.bank_account_label.grid(column=1, row=2, sticky='S', **main_options)
        #Earnings to date
        self.earnings_label = ttk.Label(self, text=' Missing Earnings to Date ', style='Theme.TLabel') 
        self.earnings_label.grid(column=2, row=2, sticky='S', **main_options)
        #Edit Payment Information Button
        self.edit_payment_info_button = ttk.Button(self, text='Edit Payment Info')
        self.edit_payment_info_button.grid(column=2, row=4, sticky='E', pady=15, padx=10)
        self.edit_payment_info_button.configure(command=lambda: self.controller.show_frame('EDIT_PAYMENT_INFO'))
        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=0, row=12, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)
        #Logout Button
        self.logout_button = ttk.Button(self, text='Logout')
        self.logout_button.grid(column=2, row=10, sticky='SE')
        self.logout_button.configure(command=self.logout)

        self.grid(column=0, row=1, padx=5, pady=5)

    def help(self):
        self.profile_img = Image.open(PAYROLL_IMG)
        self.profile_img.show()

    def logout(self):
        app.show_frame('LOGIN_FRAME')

    def update_frame(self):
        self.controller.title('Payroll Info')

        class_types = {'1': 'Hourly', '2': 'Commissioned', '3': 'Salary'}
        classification = self.controller.user_info[7]
        if classification != '':
            self.payment_type_label.configure(text=f'Payment Type: {class_types[classification]}')
        payment_methods = {'1': 'MAIL', '2':'ACH'}
        pay_method = self.controller.user_info[8]
        if pay_method != '':
            self.payment_method_label.configure(text=f'{payment_methods[pay_method]}')
        if classification == '1': # Hourly employee
            pay_info = f'${self.controller.user_info[10]}'
        elif classification == '3': # Commissioned employee
            pay_info = f'Salary: ${self.controller.user_info[9]} Rate: {self.controller.user_info[11]}%'
        elif classification == '2': # Salaried employee
            pay_info = f'${self.controller.user_info[9]}'
        else:
            pay_info = 'No Pay Info'
        self.salary_label.configure(text=f'Pay Info: {pay_info}')
        routing_number = self.controller.user_info[12]
        if routing_number != '':
            self.routing_number_label.configure(text=f'Routing #: {routing_number}')
        bank_account = self.controller.user_info[13]
        if bank_account != '':
            self.bank_account_label.configure(text=f'Account: {bank_account}')
        earning_to_date = self.controller.user_info[22]
        if earning_to_date != '':
            self.earnings_label.configure(text=f'Earning To Date: ${earning_to_date}')

        warning_text = ''
        # If employee has payment type of mail, but is missing address info, display warning
        if self.controller.user_info[8] == '1':
            if self.controller.user_info[3] == '' or self.controller.user_info[4] == '' or self.controller.user_info[5] == '' or self.controller.user_info[6] == '':
                warning_text = '''WARNING: You are not currently eligible for payroll.
You have elected to receive your paycheck by mail, but you are currently missing address information.
Update address info on your Profile Page.'''
        # If employee has payment type of ach, but is missing routing/account info, display warning
        elif self.controller.user_info[8] == '2':
            if self.controller.user_info[12] == '' or self.controller.user_info[13] == '':
                warning_text = '''WARNING: You are not currently eligible for payroll.
You have elected to receive your paycheck by mail, but you are currently missing routing or account information.
Update bank info on your Payroll Page.'''
        self.warning = tk.Text(self, height=4, width=90, state='normal', wrap='word')
        self.warning.delete("1.0", "end-1c")
        self.warning.insert(tk.END, warning_text)
        self.warning.grid(column=0, row=3, columnspan=2, rowspan=2, sticky='W')

class EDIT_PERSONAL_INFO(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        options = {'padx':5, 'pady':5}
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.street = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.zip = tk.StringVar()
        self.phone = tk.StringVar()
        #First Name
        self.edit_first_name_label = ttk.Label(self, text='First Name:')
        self.edit_first_name_label.grid(column=1, row=1, sticky='W', **options)
        self.edit_first_name_entry = ttk.Entry(self, textvariable=self.first_name)
        self.edit_first_name_entry.grid(column=2, row=1, sticky='W', **options)
        self.edit_first_name_entry.focus()
        self.first_name_warning = ttk.Label(self, text='')
        self.first_name_warning.grid(column=3, row=1, columnspan=2, sticky='EW', **options)
        #Last Name
        self.edit_last_name_label = ttk.Label(self, text='Last Name:')
        self.edit_last_name_label.grid(column=1, row=2, sticky='W', **options)
        self.edit_last_name_entry = ttk.Entry(self, textvariable=self.last_name)
        self.edit_last_name_entry.grid(column=2, row=2, **options)
        self.last_name_warning = ttk.Label(self, text='')
        self.last_name_warning.grid(column=3, row=2, columnspan=2, sticky='EW', **options)
        #Street
        self.edit_street_label = ttk.Label(self, text='Street:')
        self.edit_street_label.grid(column=1, row=3, sticky='W', **options)
        self.edit_street_entry = ttk.Entry(self, textvariable=self.street)
        self.edit_street_entry.grid(column=2, row=3, sticky='W', **options)
        #City
        self.edit_city_label = ttk.Label(self, text='City:')
        self.edit_city_label.grid(column=1, row=4, sticky='W', **options)
        self.edit_city_entry = ttk.Entry(self, textvariable=self.city)
        self.edit_city_entry.grid(column=2, row=4, sticky='W', **options)
        #State
        self.edit_state_label = ttk.Label(self, text='State:')
        self.edit_state_label.grid(column=1, row=5, sticky='W', **options)
        self.edit_state_entry = tk.OptionMenu(self, self.state, *STATES)
        self.edit_state_entry.grid(column=2, row=5, sticky='W', **options)
        #ZIP code
        self.edit_zip_label = ttk.Label(self, text='Zip:')
        self.edit_zip_label.grid(column=1, row=6, sticky='W', **options)
        self.edit_zip_entry = ttk.Entry(self, textvariable=self.zip)
        self.edit_zip_entry.grid(column=2, row=6, sticky='W', **options)
        self.zip_warning = ttk.Label(self, text='')
        self.zip_warning.grid(column=3, row=6, columnspan=2, sticky='EW', **options)
        #Phone
        self.edit_phone_label = ttk.Label(self, text='Phone:')
        self.edit_phone_label.grid(column=1, row=7, sticky='W', **options)
        self.edit_phone_entry = ttk.Entry(self, textvariable=self.phone)
        self.edit_phone_entry.grid(column=2, row=7, stick='W', **options)
        self.phone_warning = ttk.Label(self, text='')
        self.phone_warning.grid(column=3, row=7, columnspan=2, sticky='EW', **options)

        #Okay and Cancel Buttons
        self.okay_button = ttk.Button(self, text='Okay')
        self.okay_button.grid(column=1, row=8, sticky='SE', pady=15)
        self.okay_button.configure(command=lambda: self.submit_changes())
        self.cancel_button = ttk.Button(self, text='Cancel')
        self.cancel_button.grid(column=2, row=8, sticky='SW', pady=15)
        self.cancel_button.configure(command=lambda: self.controller.show_frame('PROFILE_INFO_FRAME'))
        self.grid(padx=5, pady=5, sticky='NSEW')

        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=1, row=9, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)

    def help(self):
        self.profile_img = Image.open(EDIT_PERSONAL_IMG)
        self.profile_img.show()

    def submit_changes(self):
        # Update user_info list with input values
        if self.validate_changes():
            self.controller.user_info[1] = str(self.first_name.get())
            self.controller.user_info[2] = str(self.last_name.get())
            self.controller.user_info[3] = str(self.street.get())
            self.controller.user_info[4] = str(self.city.get())
            self.controller.user_info[5] = str(self.state.get())
            self.controller.user_info[6] = str(self.zip.get())
            self.controller.user_info[14] = str(self.phone.get()).replace('-', '')

            self.controller.update_employee_info(self.controller.user_info)

            self.controller.show_frame('PROFILE_INFO_FRAME')

    def validate_changes(self):
        valid = True
        # Don't allow empty name fields
        if self.first_name.get() == '':
            valid = False
            self.first_name_warning['text'] = 'First Name Required'
            self.edit_first_name_label.configure(foreground='red')
        else:
            self.first_name_warning['text'] = ''
            self.edit_first_name_label.configure(foreground='black')
        if self.last_name.get() == '':
            valid = False
            self.last_name_warning['text'] = 'Last Name Required'
            self.edit_last_name_label.configure(foreground='red')
        else:
            self.last_name_warning['text'] = ''
            self.edit_last_name_label.configure(foreground='black')
        # Validate Phone Number Input
        phoneValidation = "^\d{3}-?\d{3}-?\d{4}$"
        if re.search(phoneValidation, self.phone.get()):
            self.phone_warning['text'] = ''
            self.edit_phone_label.configure(foreground='black')
        else:
            valid = False
            self.phone_warning['text'] = 'Must be 10 digits. Ex: 555-555-5555 or 9876543210'
            self.edit_phone_label.configure(foreground='red')
        # Validate zip code input
        zipValidation = "^\d{5}$"
        if re.search(zipValidation, self.zip.get()) or self.zip.get() == '':
            self.edit_zip_label.configure(foreground='black')
            self.zip_warning['text'] = ''
        else:
            valid = False
            self.zip_warning['text'] = 'Must be 5 digits. Ex: "57014"'
            self.edit_zip_label.configure(foreground='red')
        return valid

    def update_frame(self):
        self.controller.title('Edit Personal Info')

        self.first_name.set(self.controller.user_info[1])
        self.last_name.set(self.controller.user_info[2])
        self.street.set(self.controller.user_info[3])
        self.city.set(self.controller.user_info[4])
        self.state.set(self.controller.user_info[5])
        self.zip.set(self.controller.user_info[6])
        self.phone.set(self.controller.user_info[14])

class EDIT_PAYMENT_INFO(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        options = {'padx':5, 'pady':5}
        
        METHODS = ['ACH', 'MAIL']

        self.routing_number = tk.StringVar()
        self.account_number = tk.StringVar()
        self.payment_method = tk.StringVar()

        #Routing Number
        self.edit_routing_number_label = ttk.Label(self, text='Bank Routing Number:')
        self.edit_routing_number_label.grid(column=1, row=1, sticky='W', **options)
        self.edit_routing_number_entry = ttk.Entry(self, textvariable=self.routing_number)
        self.edit_routing_number_entry.grid(column=2, row=1, sticky='W', **options)
        self.routing_warning = ttk.Label(self, text='')
        self.routing_warning.grid(column=3, row=1, columnspan=2, sticky='EW', **options)
        #Bank Account Number
        self.edit_account_number_label = ttk.Label(self, text='Bank Account Number:')
        self.edit_account_number_label.grid(column=1, row=2, sticky='W', **options)
        self.edit_account_number_entry = ttk.Entry(self, textvariable=self.account_number)
        self.edit_account_number_entry.grid(column=2, row=2, sticky='W', **options)
        self.account_warning = ttk.Label(self, text='')
        self.account_warning.grid(column=3, row=2, columnspan=2, sticky='EW', **options)
        #Payment Method
        self.edit_payment_method_label = ttk.Label(self, text='Payment Method (ACH or MAIL):')
        self.edit_payment_method_label.grid(column=1, row=3, sticky='W', padx=5, pady=20)
        self.edit_payment_method_entry = tk.OptionMenu(self, self.payment_method, *METHODS)
        self.edit_payment_method_entry.grid(column=2, row=3, sticky='W', padx=5, pady=20)
        
        #Okay and Cancel buttons
        self.okay_button = ttk.Button(self, text='Okay')
        self.okay_button.grid(column=1, row=4, sticky='SE', pady=15)
        self.okay_button.configure(command=self.submit_changes)
        self.cancel_button = ttk.Button(self, text='Cancel')
        self.cancel_button.grid(column=2, row=4, sticky='SW', pady=15)
        self.cancel_button.configure(command=lambda: self.controller.show_frame('PAYROLL_INFO_FRAME'))

        #Help Button
        self.help_button = ttk.Button(self, text='Help')
        self.help_button.grid(column=1, row=5, padx='5', pady='5', sticky='SW')
        self.help_button.configure(command=self.help)
        self.grid(sticky='NSEW', **options)
    
    def help(self):
        self.profile_img = Image.open(EDIT_PAYROLL_IMG)
        self.profile_img.show()

    def submit_changes(self):
        valid = True
        if self.validate_changes('Routing', self.routing_number.get()):
            self.edit_routing_number_label.configure(foreground='black')
            self.routing_warning['text'] = ''
        else:
            self.edit_routing_number_label.configure(foreground='red')
            valid = False
            self.routing_warning['text'] = 'Must be 8 digits followed by 1 alphanumeric. Ex: 12345678-A'
        if self.validate_changes('Account', self.account_number.get()):
            self.edit_account_number_label.configure(foreground='black')
            self.account_warning['text'] = ''
        else:
            self.edit_account_number_label.configure(foreground='red')
            self.account_warning['text'] = 'Must be 10 digits. Ex: 123456-7890 or 1234567890'
            valid = False
        if valid:
            self.controller.user_info[12] = str(self.routing_number.get())
            self.controller.user_info[13] = str(self.account_number.get())
            if self.payment_method.get() == 'ACH':
                self.controller.user_info[8] = '2'
            else:
                self.controller.user_info[8] = '1'
            
            self.controller.update_employee_info(self.controller.user_info)

            self.controller.show_frame('PAYROLL_INFO_FRAME')

    def validate_changes(self, ty, entry):
        if entry.strip() == '':
            return True
        routingReg = r"^\d{8}-?\d|\w$"
        accountReg = r"^\d{6}-?\d{4}$"
        if ty == "Routing":
            return len(re.findall(routingReg, entry)) > 0
        elif ty == "Account":
            return len(re.findall(accountReg, entry)) > 0
        return False

    def update_frame(self):
        self.controller.title('Edit Payroll Info')

        self.routing_number.set(self.controller.user_info[12])
        self.account_number.set(self.controller.user_info[13])
        if self.controller.user_info[8] == '1':
            self.payment_method.set('MAIL')
        else:
            self.payment_method.set('ACH')

if __name__ == '__main__':
    app = APP()
    Pmw.initialise(app)
    app.mainloop()
    