import mechanize,urllib,re,sys,os
from bs4 import BeautifulSoup

class myurlopener(urllib.FancyURLopener):
        version='Mozilla/5.0 (Windows NT 8.1; rv:10.0) Gecko/20100101 Firefox/10.0'
urllib._urlopener = myurlopener()

global_files = set()
global_folders = set()
global_files_list = []
global_folders_list = []


#link = sys.argv[1]
def main(link):
    http = urllib.urlopen(link)
    global global_files
    global global_folders
    global global_files_list
    global global_folders_list

    if http.code == 200:
        html = http.read()
        soup = BeautifulSoup(html,'lxml')
        anchor_tags_list = soup.find_all('a')

        href_list = []

        print "Processing tags for Link : {0}\n".format(link)
        for x in anchor_tags_list:
            try:
                xx = x['href']
                if xx.find('http') == -1:
                    xx = sys.argv[1]+'/'+xx
                href_list.append(xx)
            except:
                pass
        files = []
        folders = []

        for y in href_list:
            last_elem = y.split('/')[-1]
            if last_elem.find('.') != -1:
			    files.append(y)

        for y in href_list:
            depth = len(y.split('/'))
            if depth > 4 :
                full_folder = y.split('/',3)[-1]
                for i in range(1,depth-3):
                    folders.append(full_folder.rsplit('/',i)[0])

        for value in folders:
            global_folders.add(value)
        for value in files:
            global_files.add(value)

        global_files_list = list(global_files)
        global_folders_list = list(global_folders)

#       print str(global_files_list) + '\n'
#       print str(global_folders_list) + '\n'

        print "Processing for Link : {0} is complete.\n---------------------------------------------------------".format(link)

    else:
        print " Error Code = "+str(http.code)

main(sys.argv[1])

for link in global_files_list:
    a = ['html','php','jsp','aspx']
    if any(x in link for x in a):
        try:
            main(link)
        except:
            print "Some Error Processing Link"

print str(global_files_list) + '\n'
print str(global_folders_list) + '\n'
