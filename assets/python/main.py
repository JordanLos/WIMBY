import json
from data import download, csvToList, decomposeESA, decomposeEdmLine, findContaminatedSites

download()
rawESA = csvToList('./../../data/ESA-data.txt', 1)
ESA_PBL = decomposeESA( rawESA )
rawEdm = csvToList('./../../data/Property_Information_Data.csv')

contaminatedSites = findContaminatedSites( rawEdm, ESA_PBL )

# Convert list of objects to list of dictionary sets for JSON file
toJSON = [obj.__dict__ for obj in contaminatedSites]
# Convert list of dictionary sets to JSON file
with open('./../../data/Contaminated-Sites-In-Edmonton.json','w') as f:
    jstring = json.dumps([entry.__dict__ for entry in contaminatedSites],sort_keys=True, indent=4 )
    f.write(jstring)

with open('./../../data/Contaminated-Sites-In-Edmonton.geojsonp','w') as f:
    # Format for geoJSON
    f.write('eqfeed_callback(')
    f.write('{\n\t"type": "FeatureCollection",\n\t"features": [')

    # Insert All attributes
    fspecOpen = '\n\t\t{\n\t\t\t"type": "Feature",\n\t\t\t"properties": ' \
        '{},\n\t\t\t"geometry": {\n\t\t\t\t"type": ' \
        '"Point",\n\t\t\t\t"coordinates": [\n\t\t\t\t\t'
    fspecEnd = '\n\t\t\t\t]\n\t\t\t}\n\t\t},'
    
    with open('./../../data/Contaminated-Sites-In-Edmonton.json','r') as f1:
        cSitesJson = json.load(f1)
        for entry in cSitesJson:
            print( entry )
            f.write(fspecOpen)
            f.write(entry['lng'] + ',' + entry['lat'] )
            f.write(fspecEnd)
        f.write('\n\t]\n});')
