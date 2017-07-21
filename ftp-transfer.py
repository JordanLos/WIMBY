import ftplib
import sys
import time 

#-----DOWNLOAD AND SAVE AS CSV-----#

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

workingEsa = []
with open(filename + '.txt') as f:
    reader = csv.reader(f)
    
    for row in reader:
       workingEsa.append( row )

    # Second Row is series of '----' and not needed
    del workingEsa[1]


#----REMOVAL ALL BUT EDMONTON------#

# Legal Land Description Contians ATLA and ATS
# First, we must isolate the first number
testEsa = []
for row in workingEsa[:10]:
    testEsa.append( row[3].split(';')[0] )

# Iterate Through full ESA list to identify:
# 1) ATLA numbers (7 digits), 2) Edmonton (3rd digit == 2)
edmontonLlds = []
for row in workingEsa:
    # LLD is in the 4th column
    # ATLA number is first in ';' delimited set in LLD
    # Removes all but the first set of numbers for each LLD entry
    lld = row[3].split(';')[0]

    # Tests for Edmonton ATLA 
    if ( len(lld) == 7 ):
        if lld[2] == '2':
            edmontonLlds.append( row )

#----------CONVERT TO JSON----------#
import json

with open('Edmonton-ESA' + now + '.json', 'w') as f_obj:
    json.dump(edmontonLlds, f_obj, sort_keys=True, indent=4)
    print('Saving to: Edmonton-ESA' + now + '.json')
