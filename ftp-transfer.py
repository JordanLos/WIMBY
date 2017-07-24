import ftplib
import sys
import time 

#-----DOWNLOAD ESA LIST AND SAVE AS CSV-----#

# Connect to FTP Client and cd to directory containing brownfields`
ftp = ftplib.FTP('ftp.gov.ab.ca')
ftp.login()
ftp.cwd('/env/ESAR')

# Create a list of all ESA entries
# Note: Each index in the list is a string
EsaList = []
ftp.retrlines('RETR CompleteEsaSiteList.csv', EsaList.append )

# Politely log out
ftp.quit()

# Print Length of List to confirm Download Worked
print('There are ' +  str(len( EsaList )) + ' items in the file' )

# Get Date and Time to Distinguish files
now = time.strftime("%H.%M.%S--%m-%d-%Y")

# Save EsaList into a file
filename =  'ESA' + '-' + now 
    
with open( filename + '.txt', 'w' ) as file_object:
    for item in EsaList:
        file_object.write( str( item ) +"\n" )
    print('Saving to: ' + filename + '.txt')

#------CREATE A LIST OF LIST FROM CSV-----#
import csv

# Create Function to move CSV to List
def csv_to_list(infile, rmRow=''):
    """Converts CSV file to a list, option to delete Row
    should the file contain '----'"""
    
    listName = []
    with open(infile) as f:
        reader = csv.reader(f)

        for row in reader:
            listName.append( row )

        if rmRow:
            del listName[rmRow]

    return listName

# Make a working list for the ESA and PBL CSV files
workingESA = csv_to_list(filename + '.txt', 1)
workingPBL = csv_to_list('Property_Information_Data.csv')


#----------CONVERT TO JSON----------#
import json

with open(filename + '.json', 'w') as f_obj:
    json.dump(workingESA, f_obj, sort_keys=True, indent=4)



