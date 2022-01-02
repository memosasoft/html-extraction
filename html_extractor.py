# Python program to AI smart spider project

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

url_address = []
url_visited = []
root_url = []

MIN_KEYWORDS_IN_URL = 2
MIN_KEYWORDS_IN_CONTENT = 11

RELAX_TIME = 0.1

keys = ["python", "code", "programming", "tutorial", "coding", "exemples", "sample", "java", "c++","technical", " subjects", " snippets", " HTML", " CSS", " JavaScript", " SQL", " PHP", " jQuery", " XML ", "DOM ", "Bootstrap ", "Tutorials", " Articles ", "Programming"]

#This function read the texte
def getUrl():
    counter_training = 0
    # keywords needed to spider
    global keys
    global url_address;
    
    
    url_address = get_urls_from_file(url_address)
    
    # loop thrue array of urls
    for current_url in url_address:
        
        if counter_training > 20:
            MIN_KEYWORDS_IN_URL = 3
            MIN_KEYWORDS_IN_CONTENT = 5
            
        counter_training = counter_training + 1
            
        index = 0
        # SPIDER A NEW URL
        print("SPIDER A NEW URL\n\n")
        print("URL : " + current_url)
            
        if (check_url_for_keywords(current_url, keys)):
            print("initial test - PASSED")
            print("The link has query keywords")
        
        time.sleep(RELAX_TIME)
        
        print("Fetching URL...")
        try:
            # get html file
            if (current_url.find("http")>=0):
                res = requests.get(current_url)
            else:
                res = requests.get("http:/"+ current_url)
        except:
            
            print("ERROR IN RESPONSE FETCHING URL with current_url")
            continue
        
        time.sleep(RELAX_TIME)
        
        print("Adding url to visited sites...")
        if not current_url in url_visited:
            url_visited.append(current_url)
            url_address.remove(current_url)
            
        html_page = res.content
        
        time.sleep(RELAX_TIME)
        
        title =""
        description = ""
        keywords = ""
        
        soup_spider = BeautifulSoup(html_page, 'html.parser')
        
        the_text = soup_spider.get_text()
        con_word = ""
        
        for word in the_text.split():
            word = str(word.strip())
            con_word = con_word + " " + word
            con_word = con_word.replace("  ", " ")
            con_word = con_word.strip() + " "
            
       
        the_text = con_word
        #response = summarize(the_text)
        
        for title in soup_spider.find_all('title'):
            title = title.get_text() 
        
        for link in soup_spider.findAll(attrs={"name":"description"}):
            
            link = link.get("content")
            
            if link == None:
                break
            print(link)
            description = description + " " + str(link)
            
        for link in soup_spider.findAll(attrs={"name":"keywords"}):
        
            link = link.get("content")
            if link == None:
                break
            print(link)
            keywords = keywords + " " + str(link)
            
                
        if title == None or description == None or keywords == None:
            break
        
        all_the_text = title + " " + description + " " + keywords + the_text
        
        globalo_int = 0
        # loop thrue array of urls
        for i in url_address:
            globalo_int = globalo_int + 1
        
        print("We have " + str(globalo_int) + " in the url buffer")
        print("Checking quality of html site...")
        time.sleep(RELAX_TIME)     
        
        if (check_text_for_keywords(all_the_text, keys)):
            print("Second test - PASSED")
        else:
            continue   
        
        print("Extracting liks...")
        time.sleep(RELAX_TIME)
        url_address = extractUrls(current_url, html_page, "a", "href")
        url_address = extractUrls(current_url, html_page, "link", "href")  
        print("found urls: " + str(index))
        time.sleep(RELAX_TIME)
        dateTimeObj = datetime.now()
                
        try:
            # open file with list of url
            f = open(dateTimeObj.strftime("./spider/" +"web-%Y%S%f.html"), "w")
            f.write("<html><head></head><body>")
            f.write("<b>Title:</b><h1> " + str(title) + "</h1><br><br>")
            f.write("<b>Description:</b> " + str(description) + "<br><br>")
            f.write("<b>Keywords:</b>  " + str(keywords) + "<br><br>")
            f.write("<b>url:</b>  <a href=\"" + str(current_url) + "\">" + str(current_url) + "</a><br><br>")
            f.write("<b>section:</b>  " + str(the_text[0:len(the_text)/4]) + "...<br><br>")
            f.write("</body></html>")
            f.close()
            
            save_urls_from_file()
        except:
            print("ERROR in saving output to file") 
    
    MIN_KEYWORDS_IN_URL = 1
    MIN_KEYWORDS_IN_CONTENT = 2
    counter_trainer = 0
    getUrl()
               
            
def check_url_for_keywords(current_url, keys):
    hit = 0
    cursor = 0
    for k in keys:
        print(hit)
        if len(k)>=5:
            if (current_url.lower().find(k[0:5].lower(), cursor)>=0):
                hit = hit + 1    
                cursor = current_url.lower().find(k[0:5].lower(),cursor)+ 1
    cursor = 0
    for k in keys:
        print(hit)
        if (current_url.lower().find(k.lower(), cursor)>=0):
            hit = hit + 1 
            cursor = current_url.lower().find(k[0:5].lower(),cursor)+ 1
            
    if(hit >= MIN_KEYWORDS_IN_URL):
        return True

    return False

def check_text_for_keywords(text, keys):
    hit = 0
    cursor = 0
    for k in keys:
        k = k.strip()
        print(hit)
        if len(k)>=5:
            if (text.lower().find(k[0:5].lower(), cursor)>=0):
                hit = hit + 1
                cursor = text.lower().find(k[0:5].lower(),cursor)+ 1
    cursor = 0
    for k in keys:
        k = k.strip()
        print(hit)
        if (text.lower().find(k.lower(), cursor)>=0):
            hit = hit + 1
            cursor = text.lower().find(k.lower(),cursor)+ 1
            
    if(hit >= MIN_KEYWORDS_IN_CONTENT):
        return True
    
    return False
    
def save_urls_from_file():
    
    # open file with list of url
    with open("urls.txt", "w") as file: 
        # reading each line     
        for url in url_address: 
            # Read all lines in t
            url = url.strip()
            file.write(url+"\n")
            
    # open file with list of url
    with open("urls_visited.txt", "w") as file: 
        # reading each line     
        for url in url_address: 
            # Read all lines in t
            url = url.strip()
            file.write(url+"\n")
    
    # open file with list of url
    with open("urls_roots.txt", "w") as file: 
        # reading each line     
        for url in root_url: 
            # Read all lines in t
            url = url.strip()
            file.write(url+"\n")
 

def get_urls_from_file(url_address):

    # open file with list of url
    with open("urls.txt", "r") as file: 
        # reading each line     
        for url in file: 
            # Read all lines in t
            url = url.strip()
            url_address.append(url)

    # Delete old dictionnary file
    f = open("urls.txt", "w")
    f.write("")
    f.close()
    
    return url_address
    
#This function read the texte
def extractUrls(current_url, html_page, tag, sub_tag):
            
    global url_address
    global root_url

    html = current_url # your HTML
    soup_spider = BeautifulSoup(html_page, 'html.parser')

    keys = ["python", "code", "programming", "tutorial"]
    index = 0
    for link in soup_spider.find_all(tag):
        print(link)
        link = link.get(sub_tag)
        index = index + 1 
        if(link==None):
            continue
        if (link.find("facebook")>=0):
            continue
        if (link.find("google")>=0):
            continue
        if (link.find("bing")>=0):
            continue
        if (link.find("yahoo")>=0):
            continue
        if (link.find("instagram")>=0):
            continue
        if (link.find("youtube")>=0):
            continue
        if (link.find("redit")>=0):
            continue
        if (link.find("tutorialspoint")>=0):
            continue
        if (link.find("javascript")>=0):
            continue
        if (link.find("#")>=0):
            continue
        if (len(link)<5):
            continue
        
        if (check_url_for_keywords(link, keys)):
            print("Links in link test passed")
        else:
            continue
        
        if not link is None:
            if link.find("http")<0:
                # get root https path
                root_path = get_path(current_url, link)
                if not root_path in root_url:
                    root_url.append(root_path)
                else:
                    continue
                if link[0] == "/":
                    link = root_path + link
                else:
                    link = root_path + "/" + link
                    
        if not link in url_address:
            if not link in url_visited:           
                if (link != current_url):
                    if link.find("http")>=0:
                        url_address.append(link)
                        print(link) 
    
    print("URLS found " + str(index))
    time.sleep(RELAX_TIME)
    
    return url_address 

def get_path(url, link): 
    
    if (url.find("https://")>=0):
        url = url.replace("https://","")
        split_url = url.split("/")   
        return "https://" + split_url[0]
    
    if (url.find("http://")>=0):
        url = url.replace("http://","")   
        split_url = url.split("/")   
        return "http://" + split_url[0]
    
    # Just a guess
    url = url.replace("https://","")
    split_url = url.split("/")   
    return "https://" + split_url[0]

def convert_to_binary(string):
    
    # Python3 code to demonstrate working of
    # Converting String to binary
    # Using join() + bytearray() + format()
    
    # initializing string 
    test_str = "GeeksforGeeks"
    
    # printing original string 
    print("The original string is : " + str(test_str))
    
    # using join() + bytearray() + format()
    # Converting String to binary
    res = ''.join(format(i, '08b') for i in bytearray(test_str, encoding ='utf-8'))
    
    # printing result 
    print("The string after binary conversion : " + str(res))
          
                
getUrl()