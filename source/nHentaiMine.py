import urllib
import urllib2
import os

illegalChars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                '/', ' ', '$', '|', '\'', '"', ':', ';', '@', '+', \
				'`', '!', '=']

urlFile = open("test.txt", "r")
urlAddresses = urlFile.read().splitlines()
originalDir = os.getcwd()

def getNameAndGallery(someUrl):
	# got this from a website
	req = urllib2.Request(someUrl, headers={'User-Agent' : "Magic Browser"}) 
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
			# print "Cleaning name..."
			headerStr = headerStr.replace(symbol, "")
	# print headerStr
	# remove them quotes
	rawMediaId = rawMediaId.replace("\"","")
	# split that shit into a list
	tempLst = rawMediaId.split(":")
	# can i get yo numbah?
	galleryNum = int(tempLst[1])
	return [headerStr, galleryNum]

def downloadAlbums(mangaName, mangaID, pageNum, pageCode):
	picNum = pageNum
	pageStatus = pageCode
	#make a new folder
	try:
		os.mkdir(mangaName)
	except OSError:
		print "Directory already exists. Overwritten."
	os.chdir(mangaName)
	print os.getcwd()
	# I need to find a way
	while pageStatus != 404:
		downloadUrl = "https://i.nhentai.net/galleries/%i/%i.jpg" % (mangaID, picNum)
		# print pageStatus
		fileName = "%i.jpg" % picNum
		pageStatus = urllib.urlopen(downloadUrl).getcode()
		if pageStatus != 404:
			print "Downloading " + downloadUrl + " as " + fileName
			urllib.urlretrieve(downloadUrl, fileName)
		
		picNum += 1
	else:
		print "---END OF ALBUM---"	
		os.chdir(originalDir)		

for currentURL in urlAddresses:
	picNum = 1
	pageStatus = 1
	hentaiName = getNameAndGallery(currentURL)[0]
	hentaiID = getNameAndGallery(currentURL)[1]
	print hentaiName
	print hentaiID
	downloadAlbums(hentaiName, hentaiID, picNum, pageStatus)

urlFile.close()
