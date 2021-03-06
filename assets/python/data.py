
def download():
    """ Downloads ESA list from the ESRD site"""

    import ftplib

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
        
    with open( './../../data/ESA-data.txt', 'w' ) as file_object:
        for item in EsaList:
            file_object.write( str( item ) +"\n" )
        print('Saving to: ESA-data.txt')

# Create Function to move CSV to List
def csvToList(infile, rmRow=''):
    """Converts CSV file to a list, option to delete Row
    should the file contain '----'"""
    import csv
    
    listName = []
    with open(infile) as f:
        reader = csv.reader(f)

        for row in reader:
            listName.append( row )

        if rmRow:
            del listName[rmRow]

    return listName

# ----- Process ESA -----#
# Iterate Through Full ESA list to identify:
# 1) ATLA Numbers (7 digits), 2) Edmonton (3rd digit==2)
def decomposeESA(rawESA):
    """ Decomposes the ESA into a single 17 digit PBL number. The raw ESA file has the following column headers:
    0. Esrd File Number 
    1. Operation Name 
    2. File Classification 
    3. LLD ( Some PBL's and some ATLA numbers)
    4. Documents in File
    5. Linc 
    6. 10TM Point Coordinates  """

    inProcessESA = []
    # takes first numbers from LLD
    for row in rawESA:
        lld = row[3].split(';')[0]

        # Tests for Edmonton LLD number ('2' in the third digit)
        if ( len(lld) == 7):
            if lld[2] =='2':
                inProcessESA.append( row )
    # Decomposes ESA by splitting the LLD and padding the plan(7), block(4), and lot(6)
    # with the appropriate amount of zeros.  
    ESA_PBL = []
    for row in inProcessESA:
        pbl = row[3].split(';')

        plan = pbl[0].zfill(7)

        # Only use first if the row has multiple LLD's.
        if len(pbl) >=2 and pbl[1]:
            block = pbl[1].split(' ')[0]
            block = block.zfill(4)
        else:
            block = '0000'

        if len(pbl) >=3 and pbl[2]:
            workingLot = pbl[2].split(' ')[0]
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


        inProcessPBL = ''.join([plan,block,lot])
        ESA_PBL.append( inProcessPBL )
    
    return( ESA_PBL )

# Decomepose Line of EDMONTON to PBL
def decomposeEdmLine( cell ):
    """ Decomposes a LLD in the Edmonton Property Data to a list of its plan, block, lot, and PBL"""
    # The function will be passed the cell by the calling line
    inProcessPbl = cell.split('/')[0]
    inProcessPbl = cell.split(' ')
    
    plan = inProcessPbl[1]

    try:
        inProcessPbl[4]
    except IndexError:
        block = '0000'
    else:
        block = inProcessPbl[4]

    try:
        inProcessPbl[7]
    except IndexError:
        lot = '000000'
    else:
        lot = inProcessPbl[7]

    pbl = plan.zfill(7) + block.zfill(4) + lot.zfill(6)

    return( pbl, plan, block, lot )

def findContaminatedSites(rawEdm, ESA_PBL):
    class Contaminated_Site():
        """An individual contaminated site"""

        def __init__(self, esrdFileNum, house, street, plan, block, lot, lat, lng):
            self.esrdFileNum = esrdFileNum
            self.house = house
            self.street = street
            self.plan = plan
            self.block = block
            self.lot = lot
            self.lat = lat
            self.lng = lng

    contaminatedSites = []
    for row in rawEdm:
        # Not LLD's are PBL's and will produce an IndexError - ignore them and move 
        # to next row
        try:
            row[4].split(' ')[1]
        except IndexError:
            continue

        # Break the rawEdm into components, including its unique PBL number
        else: 
            esrdFileNum = row[0]
            pbl = decomposeEdmLine( row[4] )
            house = row[2]
            street = row[3]
            plan = pbl[1]
            block = pbl[2]
            lot = pbl[3]
            lat = row[8]
            lng = row[9]
        # Test the unique PBL numbers for the current with for a match in the ESA 
        # list. If the match exists, create a new Contaminated_Site instace and add 
        # it to the list of contaminated sites
        for entry in ESA_PBL:
            if pbl[0] == entry:
                site = Contaminated_Site( esrdFileNum, house, street, plan, block, lot, lat, lng )
                contaminatedSites.append( site )
    return contaminatedSites
