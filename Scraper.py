#  -*- coding: utf-8 -*-
import urllib.request
import time
import re



# Find todays date
Date = (time.strftime("%Y-%m-%d"))

# Create URL
url = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?from=2016-12-11" #+ Date

#Scrape String data from webpage
response = urllib.request.urlopen(url).read().decode("utf-8")

#Parse out Urls and Titles of new Articles
#urls = re.findall('href="?\'?([^"\'><]*)', response)
titles = re.findall('citation="?\'?([^"\'><:]*)', response)
ids = re.findall('id="PMC?\'?([^"\'><]*)', response)

for i in range (0, len(ids)):

    url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:"+ids[i]+"&metadataPrefix=pmc"
    #print (url)
    contents = urllib.request.urlopen(url).read().decode("utf-8")
    Con =(str(contents))
    #print (Con)
    Tit = "download\\" +titles[i]+ ".xml"
    print (Tit)

    with open(Tit, 'w', encoding='utf-8') as f:
        f.write(Con)
        f.close()
    #with open('test.txt', 'w') as f:
      #  f.write("hi")
       # f.close()





    ## urllib.request.urlretrieve(urls[i], "Processing\\" + titles[i])



#For each article in List
# download article
#



#url = 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/50/30/Angew_Chem_Int_Ed_Engl_2016_Mar_1_55(10)_3295-3299.tar.gz'

#print("downloading with urllib")
#urllib.request.urlretrieve(url, "code.zip")



