####!/usr/bin/env bash

cmd=$(basename $0)

if [ -z ${NOWLIVEMAPFILE} ]
then
    echo "Environment variables not set. Run '. nowliveenv.sh' to set them"
    exit
fi

mapfile=${NOWLIVEMAPFILE}
#mapfile="FBV3twitch_twitter.txt"

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

case ${cmd} in
	dupemenu.sh)
	prog=dupe.sh
	;;
	missedmenu.sh)
	prog=missed.sh
	;;
	rerunmenu.sh)
	prog=rerun.sh
	;;
	*)
	echo "Invalid option ${cmd}"
	exit
	;;
esac

select streamer in "${twitchset[@]}"
do 
	case $streamer in
		quit)
		exit
		;;
		*)
		grep ${streamer} ${mapfile}
		${prog} ${streamer} "$@"
		break
		;;
	esac
done