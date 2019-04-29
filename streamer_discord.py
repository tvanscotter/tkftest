#!/usr/local/bin/python3

#
# Author: Tom Van Scotter
# Date: 12/12/18
# Update Date: 12/23/18
#
# Synopsis:
# Generate text strings to be used for a discord message, a tweet, and a FaceBook post

# we need to use the discord message only when the MEE6 bot is not working
# seems to be happening more often this week
#
# examples of these strings:
#
# discord message:
# DrMickLive is now live on https://www.twitch.tv/DrMickLive ! Go check it out!
#
# tweet:
# @DrMickLive is now live on https://www.twitch.tv/DrMickLive ! Go check it out!
# Community Choice Game Night: [Game] Sessions with a Therapist
# #NerdHype #TwitchEDU
#
# facebook:
# 
# @tom.vanscotter is live on https://www.twitch.tv/napfan ! Go check it out!
# Testing FB / twitch / twitter
# If the streamer has a facebook account we would include it. right now it is the first thing in the first line of the message. If they don't have one then it would just show their twitch handle.
# NerdHype #TwitchEDU
# Find this and more at @TheKnowledgeFellowship
# Twitter: https://twitter.com/tvanscotter

import os
import sys
import argparse
import datetime
import re

def usage():
	print ("Usage: ")
	print ("\nUse this script to generate two sets of text:")
	print ("\nthe first text string will be a single line and can be used as the text for a message in the TKF discord #now-live channel")
	print ("\nthe second text string will be a multi-line string that can be used to send a tweet")
	print ("Single tick-marks are required for the streamer text if it is more than one word")
	print ("There may be special characters that don't work well in the streamer text")
	print ("Haven't found any yet but it's early-on using this script")
	print ("You must provide the twitch handle. If you omit the twitter handle the program will prepend @ to twitch handle")
	print ("If you omit the streamer text the program with insert NOTEXT and it will look silly")
	print ("\ntry these examples:\n",sys.argv[0]," -t rockitsage -s 'Shiny rocks and stuff'")
	print ("\n",sys.argv[0]," -t rockitsage -w @rockitsage -s 'Shiny rocks and stuff'")
	print ("\n",sys.argv[0]," -t rockitsage -w @rockitsage")
	print ("\nPlease feel free to make any changes to this code you want. Let the author know if you do something really cool.")
	print ("Run: ", sys.argv[0], " -h for syntax\n")
	

# this function checks to see if the value twitch is in the list user dict
# and returns the value for twitch if so or False if not
# the value of twitch in the usermap dict is the twitch streamer's twitter handle
# and code have optional "!Y" on the end. This signifies that the streamer is
# currently a nominee and will get a slightly different 
# Find more like this at @TheKnowledgeFe1 vs Find this and more at @TheKnowledgeFe1

def getTwitter(twitch,usermap):
	if twitch in usermap:
		return usermap[twitch]
	else:
		return False

# read the entries from the file into a dict structure
# the format of the file is:
# twitch-handle:twitter-handle[|Y]
# the optional [|Y] indicates that the streamer is on the nominations list and
# will get a slightly different tweet than the streamers who are on the #list-of-streamers

def getTwitterList(filename):
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			d = dict(line.strip().split(':') for line in f)
		f.close()
		return d
	else:
		return False

def getHandleMapping(filename):
#	streamerlist = {'napfan': {'twitter': 'tvanscotter', 'option': '', 'facebook': 'vanscotter'}}
#	return streamerlist
	if os.path.isfile(filename):
		d={}
		with open(filename, 'r') as f:
			for line in f:
				twitch,twitter,facebook,option=line.strip().split(':')
				d[twitch] = {'twitter': twitter, 'facebook': facebook, 'option': option}
		f.close()
		return d
	else:
		return False

def countTweets(logfile):

	tweetcount=0

	file = open(logfile, "r")

	for line in file:
		if re.search("^20", line):
			tweetcount+=1

	file.close()

	return tweetcount

def log(logfile,twitch,twitter,nominee,rerun,tkf,missed,multiple):

	tweetcount=1

	if os.path.isfile(logfile):
		lfile = open(logfile, 'a')
		tweetcount = countTweets(logfile) + 1
	else:
		print (f'Creating logfile {logfile}\n')
		lfile = open(logfile, 'w')
		lfile.write('%s' % 
			("date                            twitch                          twitter                 tkftype         live            tkfORnot\n\n"))

	if nominee:
		nom="nominee"
	else:
		nom="streamer"

	if rerun:
		live="rerun"
	elif missed:
		live="missed"
	elif multiple:
		live="multiple"
	else:
		live="live"

	if tkf:
		tkfstr="notTKF"
	else:
		tkfstr="TKF"

	now = datetime.datetime.now()

	lfile.write('%4d-%02d-%02d\t%02d:%02d:%02d\t%25s\t%17s\t%s\t%s\t%s\n' % 
		(now.year,now.month,now.day,now.hour,now.minute,now.second,twitch.ljust(25),twitter.ljust(17),
			nom.ljust(8),live.ljust(8),tkfstr.ljust(6)))
#	lfile.write('\nnumber of tweets: %d\n' % (tweetcount))
	lfile.close()

def main():
	
#	sys.exit()

	msgidx = 1
	nominee = False
	optout = False
	option = ""

	parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

	parser.add_argument('-c','--changeCheckItOut', help='change the Check it out message to this string', required=False)
	parser.add_argument('-d','--dontShowCopyPasta', help='dont show the copy/pasta messages', action='store_false', required=False)
	parser.add_argument('-f','--mapfile', help='the full path of the mapfile', required=False)
	parser.add_argument('-g','--greeting', help='choose the greeting : Hey everyone, This just in, etc', required=False)
	parser.add_argument('-k','--nolog', help='dont add a log entry', action='store_true', required=False)
	parser.add_argument('-l','--logfile', help='the full path of the logfile', required=False)
	parser.add_argument('-m','--missed', help='stream started and finished while AFK', action='store_true', required=False)
	parser.add_argument('-n','--notTKF', help='dont include TKF hashtags for non-TFK streamers', action='store_true', required=False)
	parser.add_argument('-p','--multiples', help='stream went live multiple times quickly. probable tech issue', action='store_true', required=False)
	parser.add_argument('-r','--reRun', help='streamer is showing a VOD rerun. change message appropriately', action='store_true', required=False)
	parser.add_argument('-s','--streamtext', help='the streamers message text', required=False)
	parser.add_argument('-t','--twitchhandle', help='the streamers twitch handle', required=True)
	parser.add_argument('-u','--usage', help='display the command usage notes', action='store_true', required=False)
	parser.add_argument('-v','--verbose', help='display additional processing info', action='store_true', required=False)
	parser.add_argument('-w','--twitterhandle', help='the streamers twitter handle', required=False)
	parser.add_argument('-1','--message1', help='use the message 1 content', action='store_true', required=False)
	parser.add_argument('-2','--message2', help='use the message 2 content', action='store_true', required=False)

	args = vars(parser.parse_args())

	greetings = {
		1: "Hey everyone, ",
		2: "Have you heard? ",
		3: "This just in, ",
		4: "Hello folks, ",
		5: "Did you know? ",
		6: "Greetings friends, ",
		7: "Here's a thing, ",
		8: "And now this: ",
		9: "",
	}

	if args['message2']:
		msgidx = 2

	#mapfile = "/Users/tvs/discord/src/twitch_twitter.txt"
	#logfile = "/Users/tvs/discord/src/twitch_twitter.log"

	if args['mapfile']:
		mapfile = args['mapfile']
	else:
		mapfile = "twitch_twitter.txt"

	if args['logfile']:
		logfile = args['logfile']
	else:
		logfile = "twitch_twitter.log"

	greeting="Hey everyone, "

	if args['greeting']:
		greeting =  greetings.get(int(args['greeting']), "Hola everyone, ")

	# if the log file last changed status is yesterday
	# give the user a chance to run the savelog.sh

	curday = datetime.datetime.now().strftime("%Y%m%d")
	
	if args['verbose']:
		print ("mapfile: ",mapfile,"\nlogfile: ",logfile)

	# mylist = getTwitterList('twitch_twitter.txt')
	
	if args['usage'] or not args['twitchhandle']:
		usage()
		sys.exit()
	
	# if twitter handle was not included in the arguments
	# then get it from the mapfile
	# then split that value to see if the streamer is a nominee or on the streamer list

	mapInfo = getHandleMapping(mapfile)

	streamer = args['twitchhandle']

	if not args['twitterhandle']:
		twitter = mapInfo[streamer]['twitter']
		option = mapInfo[streamer]['option']
	#	twitternom = getTwitter(args['twitchhandle'].lower(),mylist)
		if args['verbose']:
			print ("twitter, nom ", twitter, " ", option)
		if not twitter:
			twitter = '@' + args['twitchhandle']
	else:
		twitter = args['twitterhandle']

	if option == "N":
		nominee = True
	elif option == "O":
		optout = True
		print ("\nStreamer: ", args['twitchhandle'], " has opted out of personal tweets. RT from TKF twitter if streamer does their own tweet\n")
		sys.exit()

	if nominee:
		htags="#NerdHype #TwitchEDU\nFind more like this at @TheKnowledgeFe1"
		htagsFB="#NerdHype #TwitchEDU\nFind more like this at https://twitter.com/TheKnowledgeFe1"
	else:
		htags="#NerdHype #TwitchEDU\nFind this and more at @TheKnowledgeFe1"
		htagsFB="#NerdHype #TwitchEDU\nFind this and more at https://twitter.com/TheKnowledgeFe1"

	if not args['streamtext']:
		args['streamtext'] = 'NOTEXT'
	
	streamertext = args['streamtext']
	
	if args['changeCheckItOut']:
		moretext = ' ! ' + args['changeCheckItOut']
		if args['verbose']:
			print (args['changeCheckItOut'])
			print (moretext)
	else:
		if msgidx == 1:
			moretext = ' ! Go check it out!'
		else:
			moretext = ' ! Time to learn things!'

	stream = "\n" + streamer + " is now live on https://www.twitch.tv/" + streamer + " ! Go check it out!\n"
	
	if args['dontShowCopyPasta']:
		print ("\nDISCORD: copy/pasta this for TKF discord #now-live channel")
	
	# print the discord link

	print (args['missed'], " ", args['multiples'])
	if not args['missed'] and not args['multiples']:
		print (stream)
	
	if args['reRun']:
		stream = greeting + twitter + " is showing a re-run on https://www.twitch.tv/" + streamer + moretext + "\n"
	else:
		stream = greeting + twitter + " is live on https://www.twitch.tv/" + streamer + moretext + "\n"

	stream+= streamertext.strip('\n') + "\n"

	if not args['notTKF']:
		stream+= htags + "\n"
	if args['dontShowCopyPasta']:
		print ("TWITTER: copy/pasta this for tweet\n")

	# print the tweet

	if not args['missed'] and not args['multiples']:
		print (stream)

	print ("Tweet is " + str(len(stream)) + " characters. 280 max.\n")

	# generate the facebook post text

	# print (mapInfo)

	twitchURL = "https://www.twitch.tv/" + streamer

	facebook = mapInfo[streamer]['facebook']
	if not facebook:
		facebook = streamer
	#if len(facebook) > 2 and '@' in facebook:
	#	facebook=facebook[0:-2]

	stream = greeting + facebook + " is live on " + twitchURL + moretext + "\n"
	stream+= '"' + streamertext.strip('\n') + '"' + "\n"
	
	if '@' in mapInfo[streamer]['twitter']:
		stream+= "Twitter: https://twitter.com/" + twitter[1:] +"\n"

	stream+= htagsFB + "\n"
	
	# print the facebook post

	if args['dontShowCopyPasta']:
		print ("FACEBOOK: copy/pasta this for facebook\n")
	
	if not args['missed'] and not args['multiples']:
		print (stream + "\n")

	if not args['nolog']:
		log(logfile,streamer,twitter,nominee,args['reRun'],args['notTKF'],args['missed'],args['multiples'])

	sys.exit()
	
main()

'''
if len(sys.argv) > 1:

	streamer=sys.argv[1]
	 
	if len(sys.argv) > 2:
		twitch=sys.argv[2]
	else:
		twitch=streamer
	
	stream = "\n" + streamer + " is now live on https://www.twitch.tv/" + streamer + " ! Go check it out!\n"
	
	print ("\ncopy/pasta this for TKF discord #now-live channel")
	print (stream)
	
	if len(sys.argv) > 3:
		streamertext=sys.argv[3]
		stream2 = twitch + " is now live on https://www.twitch.tv/" + streamer + " ! Go check it out!\n"
		stream2+= streamertext + "\n" + htags + "\n"
		print ("copy/pasta this for tweet\n")
		print (stream2)
	
else:
	print ("Usage: ", sys.argv[0], " streamer-handle [twitch handle] ['streamer text']")
	print ("\nUse this script to generate two sets of text:")
	print ("\nthe first text string will be a single line and can be used as the text for a message in the TKF discord #now-live channel")
	print ("\nthe second text string will be a multi-line string that can be used to send a tweet")
	print ("Single tick-marks are required for the streamer text if it is more than one word")
	print ("There may be special characters that don't work well in the streamer text")
	print ("Haven't found any yet but it's early on using this script")
	print ("\ntry this as an example:\n",sys.argv[0]," rockitsage @rockitsage 'Shiny rocks and stuff'")
	print ("\nPlease feel free to make any changes to this code you want. Let the author know if you do something really cool.")
'''