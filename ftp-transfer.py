import ftplib
import sys

# Connect to FTP Client and cd to directory containing brownfields`
ftp = ftplib.FTP('ftp.gov.ab.ca')
ftp.login()
ftp.cwd('/env/ESAR')

# Create a list of all ESA entries
EsaList = []
ftp.retrlines('RETR CompleteEsaSiteList.csv', EsaList.append )

# Politely log out
ftp.quit()

# Print Length of List to confirm Download Worked
print('There are ' +  str(len( EsaList )) + ' items in the file' )



