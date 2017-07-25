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


