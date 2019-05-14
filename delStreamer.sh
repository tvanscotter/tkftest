#!/usr/bin/env bash

#FILE="twitch_twitter.txt"
if [ -z ${NOWLIVESET} ]
then
    echo "Environment variables not set. Run '. nowliveenv.sh' to set them"
    exit
fi
FILE=${NOWLIVEMAPFILE}

if [ ! -f ${FILE} ]
then
	"${FILE} not found"
	exit
fi

if [ $# -eq 0 ]
then
	printf "Enter twitch handle: "
	read twitch
	twitch=$(echo ${twitch} | tr '[:upper:]' '[:lower:]')
else
	twitch=${1}
fi

count=$(grep -c "^${twitch}:" $FILE)
if [ ${count} -eq 0 ]
then
	printf "Twitch handle ${twitch} does not exist in ${FILE}\n"
	exit
fi

printf "Deleting ${twitch} ...\n"

mv ${FILE} ${FILE}$$

while IFS='' read -r line || [[ -n $line ]]
do
	name=$(echo $line | cut -f1 -d":")
	if [ "${name}" != ${twitch} ]
	then
		echo "$line" >> ${FILE}
	fi
done < ${FILE}$$
