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
rawESA = csv_to_list(filename + '.txt', 1)
# Iterate Through Full ESA list to identify:
# 1) ATLA Numbers (7 digits), 2) Edmonton (3rd digit==2)
workingESA = []
for row in rawESA:
    # LLD is in the 4th column
    # Atla Number is first in';' delimited set
    # Below removes all but first set of numbers in the set
    lld = row[3].split(';')[0]

    # Tests for Edmonton LLD number
    if ( len(lld) == 7):
        if lld[2] =='2':
            workingESA.append( row )
workingPBL = csv_to_list('Property_Information_Data.csv')
#------- UNUSED NOW BUT USEFUL LATER CODE 
# Checks to see ESA classifications - some are cleaned up
#classSet = []
#classOnly = []
#for row in workingESA:
#    classOnly.append( row[2] )
#classSet = set( classOnly )
#print( classSet )

#----------CONVERT TO JSON----------#
import json

with open(filename + '.json', 'w') as f_obj:
    json.dump(workingESA, f_obj, sort_keys=True, indent=4)


#----------ADDRESS CLASS----------#
class Contaminated_Site():
    """An individual contaminated site"""

    def __init__(self, house, street, plan, block, lot):
        self.house = house
        self.street = street
        self.plan = plan
        self.block = block
        self.lot = lot

# Create a list of House Objects that are all contaminated sites
# PBL LISTING               ESA List
# 0 Account Number       0 Esrd File Number     
# 1 Suite                1 Operation Name
# 2 House Number         2 File Classification
# 3 Street Name          3 LLD
# 4 LLD                  4 Documents in File
# 5 Zoning               5 Linc
# 6 Lot Size             6 10TM Point Coordinates
# 7 Actual Year Built   
# 8 Lat.                
# 9 Long                

ESAllds = []

for row in workingESA:
    lld = row[3].split(';')
    print( lld )

    # Some ESA have multiple PBL's, Only 1
    # PBL for each ESA will be used and that PBL will
    # be the first listed.

    # Separate Plan Block Lot and zfill to ensure single PBL number is 
    # consistent
    plan = lld[0].zfill(7)

    if len(lld) >=2 and lld[1]:
        block = lld[1].split(' ')[0]
        block = block.zfill(4)
    else:
        block = '0000'

    if len(lld) >=3 and lld[2]:
        workingLot = lld[2].split(' ')[0]
    else:
        workingLot = '000000'

    # Some LLD's have multiple lot numbers
    hasComma = workingLot.find(',')
    hasDash = workingLot.find('-')
    if hasComma==-1 and hasDash==-1:
        lot = workingLot
    elif hasComma < hasDash:
        lot = workingLot.split(',')[0]
    elif hasDash < hasComma:
        lot = workingLot.split('-')[0]
    lot = lot.zfill(6)


    workingPBL = ''.join([plan,block,lot])
    ESAllds.append( workingPBL )


#-------Basic Error Checking-----------#
LLDS = []
for entry in ESAllds:
    LLDS.append( len(entry))
if set(LLDS) != 17:
    print('PBL Numbers have incorrect length')

if len(workingESA) != len(ESAllds):
    print('Lists not equal!: ' + 'workingESA length: ' + len(workingESA) + 
        'ESAllds: ' + len(ESAllds) )
else:
    print('Lengths equal')

i = 0
match = True
while i < 1436:
    if ESAllds[i][:7] != workingESA[i][3][:7]: 
        print('Plots not equavivalent')
        match = False
        break
    i = i + 1
    
if match:
    print('Plots are equivalent')


