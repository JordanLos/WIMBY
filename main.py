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
    # Not LLD's are PBL's and will produce an IndexError - ignore them and move 
    # to next row
    try:
        row[4].split(' ')[1]
    except IndexError:
        continue
    # Break the rawEdm into components, including its unique PBL number
    else: 
        pbl = decomposeEdmLine( row[4] )
        house = row[2]
        street = row[3]
        plan = pbl[1]
        block = pbl[2]
        lot = pbl[3]
    # Test the unique PBL numbers for the current with for a match in the ESA 
    # list. If the match exists, create a new Contaminated_Site instace and add 
    # it to the list of contaminated sites
    for entry in ESA_PBL:
        if pbl[0] == entry:
            site = Contaminated_Site( house, street, plan, block, lot) 
            contaminatedSites.append( site )
# Convert list of objects to list of dictionary sets for JSON file
toJSON = [obj.__dict__ for obj in contaminatedSites]
# Convert list of dictionary sets to JSON file
with open('Contaminated-Sites-In-Edmonton.json','w') as f:
    for entry in toJSON:
        json.dump(entry, f, sort_keys=True, indent=4)

