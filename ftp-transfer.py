import ftplib
import sys
import time 

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
with open( 'ESA' + '-' + now + '.txt', 'w' ) as file_object:
    for item in EsaList:
        file_object.write( str( item ) +"\n" )
    print('Printing to: ESA' + '-' + now + '.txt')
