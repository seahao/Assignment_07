#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# HLiang, 2021-Nov-21, Added create and write function under FileProcessor to create and write/overwrite file
# HLiang, 2021-Nov-21, Added functions 'a', 'd', 's' under DataProcessor to be called 
# HLiang, 2021-Nov-21, Tested all options 
# HLiang, 2021-Nov-28, Modify/use binary data
# HLiang, 2021-Nov-28, Add structured error handling
# HLiang, 2021-Nov-28, Tested all options and structured error handlings, except deletion is not working properly
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
     """Processing the data within runtime"""

     @staticmethod
     def add_data(Val1, Val2, Val3):
        """Function for storing data list to runtime

        Args:
            None

        Returns:
            list of user's inputs
        """
        return [Val1, Val2, Val3]
    
     @staticmethod
     def table_data(lstStr):
        """Fuction to transfer user's inputs to table

        Args:
            lstStr: user's inputs of strID, strTitle,and strArtist

        Returns:
            list of table(s)
        """
        intID = lstStr[0]
        dicRow = {'ID': intID, 'Title': lstStr[1], 'Artist': lstStr[2]}
        lstTbl.append(dicRow)
        
     @staticmethod
     def del_data(intIDDel):
        """Fuction to delete CD per user's selection

        Args:
            intIDDel: user's selection of CD to be deleted

        Returns:
            if user's selection is found in inventory the entry will be deleted
            if user's selection is missing in inventory then the CD is not found
        """
        
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
            

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        with open (file_name, 'rb') as objFile:
            while True:
                try:
                    line = pickle.load(objFile)
                    data = line.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow) 
                except:
                    break
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to write/overwrite data ingestion from runtime to txt storage

        opens a file for writing, creates the file if it does not exist

        Args:
            file_name (string): name of file used to write the data
            table (list of dict): save data from runtime to file

        Returns:
            None.
        """       
        with open(file_name, 'wb') as objFile:
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                pickle.dump((','.join(lstValues) + '\n') ,objFile)
            
    @staticmethod
    def create_file(file_name):

        objFile = open(strFileName, 'xb') #create file if needed
        objFile.close()

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
 
    @staticmethod
    def Num_input():
        """Ask user's inputs of ID number 
           Separate ID input as function for structured error handling

        Args:
            None          

        Returns:
            ID

        """
        Val0 = input('Enter ID: ').strip()
        return Val0

    @staticmethod
    def user_input():
        """Ask user's inputs of ID, Title, and Artist

        Args:
            Val1 for user's ID
            Val2 for user's Title
            Val3 for user's Artist           

        Returns:
            a table of 3 values

        """
        Val0 = IO.Num_input()
        Val1 = Error.e_value(Val0) # Through structured error handling to get an integer
        Val2 = input('Enter Title: ').strip()
        Val3 = input('Enter Artist: ').strip()
        return Val1, Val2, Val3

# -- Structured Error Hanlding  -- #
class Error:
    @staticmethod
    def e_value(Num):
        while True:
            try:
                int(Num)
                return int(Num) #returning a integer
                break
            except ValueError as e:
                print('Please input an integer!')
                print('Python built in error:')
                print(type(e), e, e.__doc__, sep='\n') 
                print('Please input a valid ID number!')
                Num = IO.Num_input()
            except Exception as e:
                print('General error!')
                print('Python built in error:')    
                print(type(e),e,e.__doc__,sep ='\n')
                print('Please input a valid ID number!')
                Num = IO.Num_input()

    @staticmethod
    def e_file(file_name):
        try:
            with open(file_name) as objFile:
                objFile.close()
        except FileNotFoundError as e:
            print('Text file not found!')
            print('Python built in error:')    
            print(type(e), e, e.__doc__,sep='\n') 
            print('A new file has been created as', file_name)
        except Exception as e:
            print('General error!')
            print('Python built in error:')    
            print(type(e), e, e.__doc__,sep ='\n')           
    

# 1. When program starts, read in the currently saved Inventory
#1.1 Erro Handling
Error.e_file(strFileName) # Structured error handling - file

# 1.2. Create file if needed
try: FileProcessor.create_file(strFileName)
except:
    pass
   
#1.3 Read file    
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.user_input()
        
        # 3.3.2 Add item to the table
        lisStr = DataProcessor.add_data(strID, strTitle, strArtist)
        DataProcessor.table_data(lisStr)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove       
        IDDel = IO.Num_input()
        # 3.5.1.3 structured error handling to make sure the input is an integer
        intIDDel = Error.e_value(IDDel)
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_data(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
          # 3.6.2.1 save data
          FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
        
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




