'''
Runnable code for the entire system.
'''

USER_ID = '999999'
EMPLOYEE_DIR = 'employees.csv'
RECEIPT_FILE = 'receipts.csv'
TIMECARD_FILE = 'timecards.csv'

# employee.csv file headers:
  # EMP ID, First Name, Last Name, Address, City, State, Zip, Classification, Pay Method, Salary, Commission Rate, Hourly Rate, Routing#, Account#, Office Phone,
  # DOB, SSN, Start Date, Permission Level, Job Title, Department, Office Email, Earning to Date, Archived?

# CLASS AND METHOD PSEUDOCODE:
  
# Application Class - Main Parent Class
  # Inherits from Tk.Tk
  
  # Constructor:
    # Uses parent constructor
    # Set title, geometry, and resizable values
    # Container for holding all of the different frame classes - dictionary - self.frames = {}
      # Keys are names for the different pages (Ex: 'profile_page') 
      # Values are call to constructor for that page (Ex: self.frames['profile_page'] = Profile_Page(--constructor args--))
      # Included Frames:
        # Login_Page, Profile_Page, Edit_Personal_Info_Page, Payroll_Info_Page, Edit_Payroll_Info_Page, Emp_Directory_Page, Add_Employee_Page, Add_Timecard_Page, Add_Receipt_Page,
    # user_info list - contains the users info for all the data fields
      # Initialize as empty list
    # employees list - contains list of lists, each list contains an employees id, first name, last name. Outer list contains a list for all employees that pass the filter (archived or not, within search parameters or not)
      # Initialize as empty list
    # viewed_employee list - contains list of an employees info for all the data fields
      # Initialize as empty list
    # viewed_employee_pay_info list - if the viewed employee is a commissioned or hourly employee, this list contains all the timecards or receipts for this employee
      # Initialize as empty list
    # timecards list - list of lists containing an employees ID and then all their currently saved timecards
      # Initialize as empty list
    # receipts list - list of lists containing an employees ID and then all their currently saved receipts
      # Initialize as empty list
    # all_employees_info list - list of lists containing all data fields for an employee, outer list contains a list for all employees that pass the filter
      # Initialize as empty list
  
  # change_frames function
    # Takes a frame name as an argument
    # Uses this name to get the value from the self.frames dictionary, which is the constructor
    # Calls reset() and tkraise() functions on that frame
    
  # get_user_info function - for updating the user_info list with the information in the employees.csv file
    # Opens the employees.csv file
      # Creates a csv reader
      # Traverses through file, checking for column 1 to match the global USER_ID value
      # If it finds a match
        # Traverses through the row, filling user_info list with the values in that row
        
  # get_employee_info function - for updating the viewed_employee list with the information in the employees.csv file
    # Takes an employee ID as an argument
      # Creates a csv reader
      # Traverses through file, checking for column 1 to match the passed employee ID value
      # If it finds a match
        # Traverses through the row, filling viewed_employee list with the values in that row
        
  # update_employee_info function - for updating the employees.csv file with information from the user_info list or the viewed_employee list
    # Takes an employee ID as an argument
    # Takes a "type" argument of "user" or "other", determines which list to pull info from 
    # create variable of tempfile using NamedTemporaryFile module
    # Open employees.csv with csvFile and tempfile
      # Create csv reader for csvFile
      # Create csv writer for tempfile
      # Traverse through the csvFile
        # For each row, check if the first column matches the employee ID argument
          # If it does not then write the contents from the reader to the tempfile
          # If it does then check if the type argument is user
            # If it is then write the contents of user_info list to the tempfile
            # If it is not then write the contents of viewed_employee list to the tempfile
    # When complete, use shutil.move to replace employees.csv with the tempfile
    
  # get_employee_pay_info function - for updating the viewed_employee_pay_info list with info from the receipt.csv or timecard.csv files
    # Takes an employee ID and "type" (commission or hourly) as arguments
    # Uses type argument to determine whether to open the receipts.txt or timecards.txt file
    # Opens the selected file for reading
      # Traverses over the file lines, looking for first column to match the employee ID
        # If it matches then creates list from that row
        # Sets the viewed_employee_pay_info list to point to this list
        # Stops traversing the loop
        
  # update_employee_pay_info function - for updating the timecards.csv or receipts.csv files with the info in the viewed_employee_pay_info list
    # Takes an employee ID as an argument
    # Takes a "type" argument of "commission" or "hourly"
    # Create variable of tempfile using NamedTemporaryFile module
    # Opens appropriate csv file based on type parameter
      # Create a csv reader for csvFile
      # Create a csv writer for tempfile
      # Traverse through the csvFile
        # For each row, check if the first column matches the employee ID argument
        # If it does not then write the contents from the reader to the tempfile
        # If it does then write the contents of viewed_empoyee_pay_info list to the the tempfile
    # When complete. use shutil.move to replace receipts.csv or timecards.csv with tempfile
    
  # get_employees function - for updating the employees list with the info in the employees.csv file
    # Takes a filter string as an argument
    # Takes a boolean as an argument for Archived (default of false)
    # Opens the employees.csv file
      # Creates a csv reader
      # Traverses through the file
        # If the employee id contains the filter as a sub-string OR the first name contains the filter as a sub-string OR the last name contains the filter as a substring AND the archive value matches
          # Then it will append the employees list with that rows values for the employee ID, first name, and last name
          
  # get_all_payroll_info function - for updating the receipts and timecards lists with the info in the receipts.csv and timecards.csv files
    # Opens the receipts.csv file
      # Create csv reader
      # Traverses through the file and updates the receipts list with the data from each row
    # Repeat for timecards.csv file
    
  # get_all_employees_info function - for udpating the all_employees_info list with the info in the employees.csv file
    # Opens the employees.csv file
      # Creates a csv reader
      # Traverses through the file and updates the all_employees_info list with the data from each row
    
    
# Login Page Frame Class
  # Inherits from Application Class
  # Constructor:
    # Include Label at top stating "Login" - column 0 row 0
    # include label space at the top of the page dedicated to error messages, initially blank - column 0 row 1
    # Display 2 Labels for Employee ID, and Password - column 0, rows 2 and 3
    # display 2 entry boxes next to matching labels - column 1, rows 2 and 3
    # button beneath the second entry box labeled 'Login'
      # Button calls login method, passing entry box values as arguments
    
  # login method:
    # Takes an employee ID and password string as arguments
    # Open passwords.csv for reading
      # Create a csv.reader object
      # Parse through file, comparing passed emp ID to first item in row
        # If emp ID matches then compare password argument to 2nd item in that row
          # If password matches then exit the loop and call successful_login method with the passed emp ID as the argument
          # If password doesn't match then exit the loop and call failed_login method
      # If traversal completes with no matches then call failed_login method
  
  # failed_login method:
    # Change the error label to say "Login Failed. Incorrect Employee ID or Password."
    # Set entry box values to be empty
    
  # successful_login method:
    # Takes the employee id as an argument
    # Set the USER_ID global variable equal to the passed argument
    # Call the parent class (application class) get_user_info function
    # Call the parent class (application class) change_frame function with a value of "profile_page" as the argument

    
# Profile Page Frame Class
  # Constructor:
    # top navbar with three buttons labeled: 'Payroll Info', 'Profile Page', and 'Directory' with padding inbetween them horizontally
      # Payroll Info Event:
        # Calls parent's get_user_info function
        # Calls parent's change_frame function with 'Payroll_Info_Page' as the argument
      # Profile Page Event:
        # Does nothing
      # Directory Event:
        # Calls parent's get_employees function with argument of "" (empty string) and false
        # Calls parent's change_frame function with 'Employee_Directory_Page' as the argument
    # below the top frame display the users ID, Name, and Job Title on the first row each in their own column with padding
    # the next row will display the users Address, Office Phone Number, and Company Email Address each in their own column with padding
      # All of the labels for this value is taken from the user_info list
    # in the next row on the last column with padding display a button labeled 'Edit Info'
      # when clicked, calls the parent class's change_frame function with an argument of "Edit_Personal_Info_Page"
    # the south east corner will display a button labeled 'Help'
      # When clicked, calls the parent class's change_frame function with an argument of "Help_Page"
    

# Edit Personal Info Page Frame Class
  # Constructor:
    # Initialize with variables equal to info from user_info list
    # left column on the frame has labels: 'First Name', 'Last Name', 'Street', 'City', 'State', 'Zip', and 'Phone' each label will be on its own row
    # right column will have text entry boxes next to each label
      # Text entry boxes are pre-populated with data from user_info list
    # below the text entry boxes and labels will be 2 buttons on the same row labeled 'Okay' and 'Cancel'
    # Okay Button:
      # When clicked changes variables to the new input values
      # Calls validate_info function
        # If it returns true then:
          # It updates the user_info list with the new variable values
          # It calls the parent's update_employee_info function with arguments of using the USER_ID and "user" as arguments
          # It calls the parent's change_frame function with argument of 'Personal_Info_Page'
        # If it returns false then:
          # It displays an error message at the bottom with the fields that were incorrect
    # space at the bottom is reserved for error messages
  
  # validate_info function
    # Compares variables with regex values that represent the correct formats for each entry type
    # If all variables pass then it returns true
    # Otherwise it returns a list of the variables that did not pass
  
  
# Payroll Info Page Frame Class
  # Constructor:
    # top navbar will have the same three buttons from the Profile Page Class labeled: 'Payroll Info', 'Profile Page', and 'Directory'
    # Payroll Info Event:
        # Does nothing
      # Profile Page Event:
        # Calls parent's get_user_info function
        # Calls parent's change_frame function with 'Profile_Page' as the argument
      # Directory Event:
        # Calls parent's get_employees function with argument of "" (empty string) and false
        # Calls parent's change_frame function with 'Employee_Directory_Page' as the argument
    # with added padding below the top navbar will display the users payment type, payment method, salary or comission rate or hourly rate depending on employee status each in their own column of the grid
    # the row below this will display the users bank routing number, bank account number, and earnings to date each in their own column
      # This info is populated using the user_info list
    # in the next row on the last column with padding display a button labeled 'Edit Payment Info'
      # when clicked, calls the parent class's change_frame function with an argument of "Edit_Payroll_Info_Page"
  # the south east corner will display a button labeled 'Help'
    # When clicked, calls the parent class's change_frame function with an argument of "Help_Page"
    
  
# Edit Payment Info Page Frame Class
  # Constructor:
    # Initialize with variables equal to info from user_info list
    # left column on the frame has labels: 'Bank Routing Number', 'Bank Account Number' and 'Payment Method'
    # right column will have text entry boxes next to each label
      # Text entry boxes are pre-populated with data from user_info list
    # below the text entry boxes and labels will be 2 buttons on the same row labeled 'Okay' and 'Cancel'
    # Okay Button:
      # When clicked changes variables to the new input values
      # Calls validate_info function
        # If it returns true then:
          # It updates the user_info list with the new variable values
          # It calls the parent's update_employee_info function with arguments of using the USER_ID and "user" as arguments
          # It calls the parent's change_frame function with argument of 'Payroll_Info_Page'
        # If it returns false then:
          # It displays an error message at the bottom with the fields that were incorrect
    # space at the bottom is reserved for error messages
  
  # validate_info function
    # Compares variables with regex values that represent the correct formats for each entry type
    # If all variables pass then it returns true
    # Otherwise it returns a list of the variables that did not pass
 
'''**PENDING**'''
# Employee Directory Page Frame Class
  # Constructor:
    # top navbar will have the same three buttons from the Profile Page Class labeled: 'Payroll Info', 'Profile Page', and 'Directory'
    # below the navbar displays text entry box centered horizontally on page with the label focused on 'First Name' 
    # the row below the text entry box has three radio buttons labeled: 'First Name', 'Last Name', and 'ID'
    # each radio button has its own value and will change the text entry box above it deleting any previously entered content using a change_frame function
    # on the same row of the text entry box on the west side of the page will display a button labeled 'Refresh'
    # east of the text entry box will display a button labeled 'Search'
    # in row below the radio buttons displays a tree view spanning 10 rows and 4 columns with headers: 'First Name', 'Last Name', 'Employee ID', and a button labeled 'See More Info'
    # tree view menu will have a scroll bar on the east side
    # column to the east in the row below the radio buttons will have two buttons side by side with padding labeled: 'Submit Reciept' and 'Submit Timecard'
    # the next row in this column will have a button with padding labeled 'Add Employee'
    # the next row in this column will have a button with padding labeled 'Generate Full Report'
    # the next row in this column will have a button with padding labeled 'Generate Payroll Report'
    # the south east corner will display a button labeled 'Help'
      # When clicked, calls the parent class's change_frame function with an argument of "Help_Page"
 
# PROGRAM LAUNCH PSEUDOCODE:

# if __name__ == '__main__'
  # Create application object
  # Create login page object with application as parent class
  # Call app.mainloop()







if __name__ == '__main__':
  app = Application()
  Login_Page(app)
  app.mainloop()
