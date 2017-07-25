from data import download, csvToList, decomposeESA, decomposeEdmLine

# download()

rawESA = csvToList('ESA-data.txt', 1)
ESA_PBL = decomposeESA( rawESA )

rawEdm = csvToList('./data/Property_Information_Data.csv')

edmLine = decomposeEdmLine( rawEdm[52][4] )
print( edmLine )

edm_PBL = []

if rawEdm[2][4]:
    print(str(rawEdm[2][4]))
for row in rawEdm:
    try:
        row[4].split(' ')[1]
    except IndexError:
        continue
    else:
        pbl = decomposeEdmLine( row[4] )
        edm_PBL.append( pbl )

match = 0
for entry in edm_PBL:
    if entry[0][2] != '2':
        match = match + 1

print( match )
    
