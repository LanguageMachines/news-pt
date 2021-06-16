#!/bin/sh
#shell script to run the tokenizer

STARTDIR="/"

#for k in aa ab ac
do
	#first extract the files to a directory
	DIR="Locationaa/"
	mkdir $DIR
	echo "$DIR created"
        python3  pos_tag_json.2021.py $k
	# tokenize and convert to latin1
        cd $DIR
        for i in *txt
        do
            ucto -L por $i $i.tok 2> /dev/null 
            tr -s "‘’“”«»" "\"" < $i.tok |tr '—' '-' |iconv -c -f UTF-8 -t LATIN1 > $i.tok.lat1 
        done
        cd $STARTDIR
        echo "END $i -tokstep, $STARTDIR"
	

done
