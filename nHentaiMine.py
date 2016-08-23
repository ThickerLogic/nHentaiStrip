import urllib
import urllib2
import os


illegalChars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                '/', ' ', '$', '|', '\'', '"', ':', ';', '@', '+', \
				'`', '!', '=']

urlFile = open("urls.txt", "r")

urlAddresses = urlFile.read().splitlines()
	
print urlAddresses

for currentURL in urlAddresses:
	picNum = 1
	pageStatus = 1
	

# got this from a website
req = urllib2.Request(currentURL, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen( req )
pageSource = con.read()
# find where "media_id" is located in the source and move back a space
idIndex = pageSource.find("media_id") - 1
headerIndex = pageSource.find("<h1>") + 4

# retrieve both "media_id" and the following number as a string
rawMediaId = pageSource[idIndex:pageSource.find(",", idIndex)]
headerStr = pageSource[headerIndex:pageSource.find("</h1>", headerIndex)]
# find a more efficient way to remove illegal characters
headerStr = headerStr.replace("|","")
for symbol in illegalChars:
	if not headerStr.find(symbol) == -1:
		print "Cleaning name..."
		headerStr = headerStr.replace(symbol, "")
print headerStr
# remove them quotes
rawMediaId = rawMediaId.replace("\"","")
# split that shit into a list
tempLst = rawMediaId.split(":")
# can i get yo numbah?
galleryNum = int(tempLst[1])

try:
	os.mkdir(headerStr)
except OSError:
	print "Directory already exists. Overwritten."
os.chdir(headerStr)
print os.getcwd()

#make a function with a while loop out of this crap


# works well so far, but it's making an extra file
def downloadAlbums(albumURL):
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

urlFile.close()