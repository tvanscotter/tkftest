####!/usr/bin/env bash

cmd=$(basename $0)
PS3="Select the Streamer: "
if [ -z ${NOWLIVESET} ]
then
    echo "Environment variables not set. Run ' . nowliveenv.sh' to set them"
    exit
fi
pyscript=${NOWLIVESCRIPT}
defaults=${NOWLIVEDEFAULTS}
mapfile=${NOWLIVEMAPFILE}

#mapfile="FBV3twitch_twitter.txt"
#pyscript="FBstreamer_discord.py"

txt=$(echo "$1" | tr "'" "^")
txt=$(echo ${txt} | tr -d '\n')
shift 1

# txt=$(echo "$txt" | tr "!" "=")

if [ $# -gt 2 ]
then
	checkitout="${3}"
	c="-c"
	shift 3
else
	checkitout=""
	c=""
	shift 2
fi

msgid=1
if [ ${cmd} = "v7FBtweetText.sh" -o ${cmd} = "now2live.sh" ]
then
	msgid=2
fi

if [ -f ${mapfile} ]
then
	num=$(grep -c ":" ${mapfile})
	if [ $num -gt 0 ]
	then
		twitchlist=$(cat ${mapfile} | grep -v "#" | cut -f1 -d":")
	else
		echo "there are no streamers at this time"
		exit
	fi
else
	echo "${mapfile} not found"
	exit
fi

# echo ${twitchlist}

twitchset=(${twitchlist} "quit")

select streamer in "${twitchset[@]}"
do 
	case $streamer in
		quit)
		exit
		;;
		*)
		break
		;;
	esac
done

# echo -n "Last greeting used:"
# cat logs/lastgreeting

if [ ${AUTOGREETING} ]
then
	lastgreet=$(cat logs/lastgreeting)
	numgreets=$(wc -l greetfile)
	numgreets=$(cat greetfile | wc -l)

	case ${AUTOGREETING} in
		random)
		greeting=$((1 + RANDOM % ${numgreets}))
		;;
		*)
		if [ ${lastgreet} -eq ${numgreets} ]
		then
			greeting=1
		else
			((greeting=lastgreet+1))
		fi
	esac

	#echo "last: ${lastgreet} num: ${numgreets} greeting: ${greeting}"
	echo ${greeting} > logs/lastgreeting
else
	echo "Current list of greetings:"
	num=0
	while read line
	do
		((num=num+1))
		echo "${num}: ${line}"
		greetinglist=${greetinglist}${num}" "
	done < greetfile

	echo "select the number of the greeting you want to use for this now-live:"

	greetings=(${greetinglist})
	select greeting in "${greetings[@]}"
	do
		case greeting in
			*)
			break
			;;
		esac
	done

	echo ${greeting} > logs/lastgreeting
fi

#if [ $cmd = "tweetText.sh" ]
#then
#	${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini ${c} "${checkitout}" | tr "^" "'"
	txt=$(echo "${txt}" | tr "^" "'")
	${pyscript} -t ${streamer} -s "${txt}" ${@} ${NOWLIVEDEFAULTS} -${msgid} -g ${greeting}
#else
#	${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini -n ${checkitout} | tr "^" "'"
#fi

#${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini | tr "^" "'" | tr "=" "!"

