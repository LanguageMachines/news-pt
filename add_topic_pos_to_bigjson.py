#Iris, Jan 2021
# script to read in the huge json file,
#add two new fields to jsonfile: pos-tagged title and body
#these are stored at 2 locations on ponyland and we have so many files that  used sub-dirs to keep it managalbe.
# Merijn extracted the html pages and used the last 3 digits of every  doc-ID for coding the dirs
#entry:  8195113
#['casinos', 'Macau']
# and iris used a  size-based split function to divide the  huge file into pieces.
# these range from aa to ax
#8195113.body.txt.mbt


import json
import subprocess
import sys
import os
import glob
import re
import html

dirpath="pathtodir"

# input is a string containing the html page content
# use regex to fin the part that contains relevant keywords
def get_keywords(html_doc):
    keywords = set()
    for match in re.findall('<meta name=[\'"](news_)?keywords[\'"] content=[\'"]([^">]*)[\'"] */>', html_doc):
        content = html.unescape(match[1])
        if content:
            for keyword in content.split(','):
                keyword = keyword.strip()
                keywords.add(keyword)
    return sorted(keywords, key=lambda kwd: kwd.lower())


with open("news2016.json",'r',encoding="utf-8") as jfile:
    for l in jfile.readlines():
        l = l.strip()
        document = json.loads(l)
        doc_ident = str(document['_id'])
        print("entry: ", doc_ident)
        doc_url = document['url']
        doc_title = document['title']
        doc_body = document['body']

        #finding the HTML  file on our server: reconstruct the location
        last_digits = doc_ident[-3:] #last 3 digits: is the dir-name
        file_topic = glob.glob(dirpath + last_digits+ "/" + doc_ident +"/" + doc_ident+ ".html")
        if not file_topic:
            print("no keywords for ", doc_ident)
        else:
            if(os.path.isfile(file_topic[0])):
               f = open(file_topic[0], 'r')
               print(file_topic)
               htmlblurb = str(f.read())
               document['keywords'] = get_keywords(htmlblurb)
               print(document['keywords'] )
               f.close()

        #glob function returns a list -making a string from the lists -doesnt work
        file_bname = glob.glob(dirpath + doc_ident + ".body.txt.mbt")
        if not file_bname:
            print("Error not an existing file!",doc_ident, file_bname)
        else:
            print(file_bname[0])
        #document['POS-title'] = ""
        #document['POS-body'] = ""
            if(os.path.isfile(file_bname[0])):
               f = open(file_bname[0], 'r')
               document['POS-body']= str(f.read())
               #  print(document['POS-body'])
               f.close
            else:
                print("ERROR cant open file_bname, why?",file_bname) 

        file_tname = glob.glob(dirpath +  doc_ident + ".title.txt.mbt")
        if not file_tname:
           print("Error not an existing title file!", doc_ident, file_tname)
        else:
            if( os.path.isfile(file_tname[0])):
                f = open(file_tname[0], 'r')
                document['POS-title']= f.read()
                #print(document['POS-title'])
                f.close
            else:
                print("ERROR cant open file_tname, why?", file_tname)

        with open("ptnews.updated.v1.json", "a", encoding='utf-8') as write_file:
            json.dump(document, write_file, ensure_ascii=False)
            write_file.write('\n')


jfile.close()
