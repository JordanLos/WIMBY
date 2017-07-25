from data import download, csvToList, decomposeESA

# download()

rawESA = csvToList('ESA-data.txt', 1)
ESA_PBL = decomposeESA( rawESA )

for entry in ESA_PBL:
    print( entry )



