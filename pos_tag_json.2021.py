
#Iris, Jan 2021
# script to read in the huge json file,
# extract the relevant items from json per document: title and doc_body
#
 
import json
import sys

DIRPATH="pathtodir"
#we read in the  orginal json file
jsonfile= sys.argv[1]

# we  write separte text files to the outdirname
outdirname = DIRPATH +jsonfile+"/"
#we also extract the IDS and write them to a list (outlist)
listname= outdirname+"/"+jsonfile+".ids"
outlist = open(listname, 'w')


injson =DIRPATH+jsonfile
with open(injson,'r',encoding='utf-8') as jfile:
	for l in jfile.readlines():
		l = l.strip()
		document = json.loads(l)
		doc_ident = document['_id']
		doc_url = document['url']
		doc_title = document['title']
		doc_body = document['body']

		file_bname = outdirname + str(doc_ident) + ".body.txt"
		file_tname = outdirname + str(doc_ident) + ".title.txt"

		f = open(file_bname, 'w')
		f.write(doc_body)
		f.close

		f = open(file_tname, 'w')
		f.write(doc_title)
		f.close

#		print("entry: ", doc_ident)
		outlist.write(str(doc_ident)+"\n")

        #json.dump()json.dump(doc_body.decode('utf-8'),f)--> doesnt work -encoing problems
jfile.close()
outlist.close()
