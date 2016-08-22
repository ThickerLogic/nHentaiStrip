import urllib
import urllib2
import os

illegalChars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                '/', ' ', '$', '|', '\'', '"', ':', ';', '@', '+', \
				'`', '!', '=']

#url1 = 'https://i.nhentai.net/galleries/113951/12.jpg'
url2 = "https://nhentai.net/g/57324/"

print """
I'm making an app to strip images from nHentai.
It's gonna be SWEET!
"""

#urllib.urlretrieve(url1, "picNum.jpg")

# got this from a website
req = urllib2.Request(url2, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen( req )
megaStr = con.read()
# find where "media_id" is located in the source and move back a space
idNum = megaStr.find("media_id") - 1
headerId = megaStr.find("<h1>") + 4
print headerId
# retrieve both "media_id" and the following number as a string
ultrStr = megaStr[idNum:megaStr.find(",", idNum)]
headerStr = megaStr[headerId:megaStr.find("</h1>", headerId)]
# find a more efficient way to remove illegal characters
headerStr = headerStr.replace("|","")
for symbol in illegalChars:
	if not headerStr.find(symbol) == -1:
		print "Cleaning name..."
		headerStr = headerStr.replace(symbol, "")
print headerStr
# remove them quotes
ultrStr = ultrStr.replace("\"","")
# split that shit into a list
newLst = ultrStr.split(":")
# can i get yo numbah?
galleryNum = int(newLst[1])

try:
	os.mkdir(headerStr)
except OSError:
	print "Directory already exists. Overwritten."
os.chdir(headerStr)
print os.getcwd()

#make a function with a while loop out of this crap
picNum = 1
pageStatus = 1

# works well so far, but it's making an extra file
while pageStatus != 404:
	downloadUrl = "https://i.nhentai.net/galleries/%i/%i.jpg" % (galleryNum, picNum)
	# print pageStatus
	fileName = "%i.jpg" % picNum
	pageStatus = urllib.urlopen(downloadUrl).getcode()
	if pageStatus != 404:
		print "Downloading " + downloadUrl + " as " + fileName
		urllib.urlretrieve(downloadUrl, fileName)
	
	picNum += 1
else:
	print "---END OF ALBUM---"

