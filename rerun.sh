#!/usr/bin/env bash

if [ -z ${NOWLIVESET} ]
then
    echo "Environment variables not set. Run ' . nowliveenv.sh' to set them"
    exit
fi
prog=${NOWLIVESCRIPT}
defaults=${NOWLIVEDEFAULTS}

cmd=$(basename $0)
streamer=${1}
if [ ${#2} -gt 0 ]
then
    txt=$(echo "$2" | tr "'" "^")
    txt=$(echo ${txt} | tr -d '\n')
fi
if [ ${#3} -gt 0 ]
then
    msgid=${3:-2}
fi
case $cmd in
    "rerun.sh")
        lastgreet=$(cat logs/lastgreeting)
	    numgreets=$(wc -l greetfile | cut -f8 -d" ")
		if [ ${lastgreet} -eq ${numgreets} ]
		then
			greeting=1
		else
			((greeting=lastgreet+1))
		fi
	    echo "last: ${lastgreet} num: ${numgreets} greeting: ${greeting}"
        ${prog} -t ${streamer} -s "${txt}" -r ${defaults} -g ${greeting}
        ;;
    "missed.sh")
        ${prog} -t ${streamer} -m ${defaults}
        ;;
    "dupe.sh")
        ${prog} -t ${streamer} -p ${defaults}
        ;;
    *)
        printf "Invalid option $cmd. Valid options are: rerun.sh, missed.sh, dupe.sh\n"
        ;;
esac

