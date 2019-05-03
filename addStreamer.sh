#!/usr/bin/env bash

if [ ${#1} -gt 0 ]
then
	FILE=${1}
else
	FILE="nowlivemapfile.txt"
fi

if [ ! -f ${FILE} ]
then
	"${FILE} not found"
	exit
fi

count=$(grep -c "|" $FILE)
if [ ${count} -gt 0 ]
then
	printf "This file ${FILE} has the wrong format: twitch:twitter|opt new format is: twitch:twitter:facebook:opt\n"
	exit
fi

printf "Enter twitch handle: "
read twitch
twitch=$(echo ${twitch} | tr '[:upper:]' '[:lower:]')

count=$(grep -c "^${twitch}:" $FILE)
if [ ${count} -gt 0 ]
then
	printf "Twitch handle ${twitch} already in the list\n"
	exit
fi

printf "Enter twitter handle: "
read twitter

printf "Enter facebook handle: "
read facebook

printf "Enter Option if any (N for nominee, O for optout): "
read option

printf "Add ${twitch} ${twitter} ${facebook} ${option} (y/n): "
read addit

if [ ${addit} == "Y" -o ${addit} == "y" ]
then
	cp ${FILE} ${FILE}$$
	cp ${FILE} ${FILE}_SAVE

	printf "${twitch}:${twitter}:${facebook}" >> ${FILE}$$

	if [ ${#option} -gt 0 ]
	then
		printf ":${option}\n" >> ${FILE}$$
	else
		printf "\n" >> ${FILE}$$
	fi
	sort ${FILE}$$ > ${FILE}
fi
