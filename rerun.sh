#!/usr/bin/env bash

#prog=/Users/tvs/discord/src/streamer_discord.py
#prog=/Users/tvs/discord/src/FBstreamer_discord.py
#defaults=@FBtestdefaults.ini
#defaults=@defaults.ini

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
fi
if [ ${#3} -gt 0 ]
then
    msgid=${3:-2}
fi
case $cmd in
    "rerun.sh")
        ${prog} -t ${streamer} -s "${txt}" -r ${defaults}
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

