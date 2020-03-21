from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from tkinter.filedialog import askdirectory
from os import walk
import csv


f = []
folder = askdirectory()


for (dirpath, dirnames, filenames) in walk(folder):
    f.extend(filenames)

finalDir = []
for filename in filenames:
    finalDir.append(folder + "/"+ filename)



#LAT LONG
#Name
#filename, date, time, gps coordinates

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

exif = get_exif(finalDir[1])

print(get_labeled_exif(exif).get('DateTimeDigitized'))

csvFile = []
csvFirstRow = ['FileName','DateTime','Lat','Long']
csvFile.append(csvFirstRow)

for singleDir in finalDir:
    eachRow = []
    eachRow.append('FileName')
    exif = get_exif(singleDir)
    geotags = get_geotagging(exif)
    coord = get_coordinates(geotags)
    eachRow.append(get_labeled_exif(exif).get('DateTimeDigitized'))
    eachRow.append(coord[0])
    eachRow.append(coord[1])
    csvFile.append(eachRow)

with open('bbCutooData.csv', 'w', newline='') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(csvFile)


