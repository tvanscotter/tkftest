options=("streamers" "nominees" "number of tweets" "show tweets" "add streamer" "delete streamer" "save log" "quit")
select opt in "${options[@]}"
do
    case $opt in
        "streamers")
        liststreamers
            ;;
        "nominees") 
	    nominees
            ;;
        "number of tweets")
            numtweets
            ;;
        "show tweets")
            showtweets
            ;;
	"add streamer")
	    addStreamer.sh
	    ;;
	"delete streamer")
	    delStreamer.sh
	    ;;
    "save log")
        savelog.sh
        ;;
        "quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
