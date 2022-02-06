#!/bin/bash
cat idsblank.txt | while read LINHA
do
   id=$(echo $LINHA) # pega o  IDS 
   
   if [ -e "legendas/$id.txt" ] ; then
      python2.7 getTranscriptYoutube.py -id $id -lang pt > legendas/$id.txt     
   else
      echo "Já baixamos a legenda do arquivo $id.txt" 
   fi
done

