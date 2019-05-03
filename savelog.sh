#!/usr/bin/env bash

logfiledir="logs"
logfile="twitch_twitter.log"
year=$(date '+%Y')
monthday=$(date '+%m%d')
month=$(date '+%m')
day=$(date '+%d')
logdir="${logfiledir}/${year}/${month}"
cronrun="n"
datestamp=${date}

if [ $# -eq 0 ]
then
	savelogfile="${logdir}/${logfile}.${year}${month}${day}"
else
	case $# in
		1)
		if [ ${1} = "c" ]
		then
			cronrun="y"
			day=$(date -v-1d '+%d')
			month=$(date -v-1d '+%m')
			year=$(date -v-1d '+%Y')
		else
			day=${1}
		fi
		;;
		2)
		day=${1}
		month=${2}
		;;
		3)
		day=${1}
		month=${2}
		year=${3}
		;;
		*)
		echo $(date)
		echo "$@ is too many arguments"
		echo "Usage: $(basename $0)"
		echo "Usage: $(basename $0) [day]"
		echo "Usage: $(basename $0) [day] [month]"
		echo "Usage: $(basename $0) [day] [month] [year]"
		exit
		;;
	esac
		
	logdir="${logfiledir}/${year}/${month}"
	savelogfile="${logdir}/${logfile}.${year}${month}${day}"
fi

if [ ! -d ${logdir} ]
then
	mkdir -p ${logdir}
fi

if [ -f ${savelogfile} ]
then
	echo "$(date): Save logfile ${savelogfile} already exists"
	exit
fi

if [ -f ${logfiledir}/${logfile} ]
then
	echo "$(date): moving ${logfiledir}/${logfile} to ${savelogfile} ..."
	mv ${logfiledir}/${logfile} ${savelogfile}

else
	printf "$(date): file ${logfiledir}/${logfile} does not exist\n"
fi

