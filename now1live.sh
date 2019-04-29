####!/usr/bin/env bash

cmd=$(basename $0)

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

echo "Last greeting used:"
cat logs/lastgreeting

greetings=("1" "2" "3" "4" "5" "6" "7" "8" "9")

echo "Greetings are:"
echo "1:Hey everyone"
echo "2:Have you heard?"
echo "3:This just in"
echo "4:Hello folks"
echo "5:Did you know?"
echo "6:Greetings friends"
echo "7:Here's a thing"
echo "8:And now this"
echo "9:(none)"

select greeting in "${greetings[@]}"
do
	case greeting in
		*)
		break
		;;
	esac
done

echo ${greeting} > logs/lastgreeting

#if [ $cmd = "tweetText.sh" ]
#then
#	${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini ${c} "${checkitout}" | tr "^" "'"
	txt=$(echo "${txt}" | tr "^" "'")
	${pyscript} -t ${streamer} -s "${txt}" ${@} ${NOWLIVEDEFAULTS} -${msgid} -g ${greeting}
#else
#	${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini -n ${checkitout} | tr "^" "'"
#fi

#${pyscript} -t ${streamer} -s "${txt}" ${@} @FBtestdefaults.ini | tr "^" "'" | tr "=" "!"

