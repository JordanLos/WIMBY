import json
from data import download, csvToList, decomposeESA, decomposeEdmLine

# download()

rawESA = csvToList('ESA-data.txt', 1)
ESA_PBL = decomposeESA( rawESA )
rawEdm = csvToList('./data/Property_Information_Data.csv')

class Contaminated_Site():
    """An individual contaminated site"""

    def __init__(self, house, street, plan, block, lot):
        self.house = house
        self.street = street
        self.plan = plan
        self.block = block
        self.lot = lot
contaminatedSites = []

for row in rawEdm:
    try:
        row[4].split(' ')[1]
    except IndexError:
        continue
    else:
        pbl = decomposeEdmLine( row[4] )
        house = row[2]
        street = row[3]
        plan = pbl[1]
        block = pbl[2]
        lot = pbl[3]
    for entry in ESA_PBL:
        if pbl[0] == entry:
            site = Contaminated_Site( house, street, plan, block, lot) 
            contaminatedSites.append( site )

print( len( contaminatedSites ))             


