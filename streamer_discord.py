#!/usr/local/bin/python3

#
# Author: Tom Van Scotter
# Date: 12/12/18
# Update Date: 12/23/18
# Update Date: 04/29/19
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
	print ("\nUse this script to generate three sets of text:")
	print ("\nthe first text string is a single line to be used as the text for a message in the TKF discord #now-live channel")
	print ("\nthe second text string is a multi-line string to be used to send a tweet")
	print ("\nthe third text string is a multi-line string to be used to post a message to facebook")
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

# this function reads the mapfile into a dictionary containing:
# the streamer's twitch handle, twitter handle (if any), facebook handle (if any) and an option (if applicable)
# the format of the mapfile is: twitch:twitter:facebook:option
# the values of option are: N - nominee and O - opt-out
# if the option is N, then this streamer has been nominatd for to be on the TKF streamer list
# but has not yet been accepted by committee vote. nominated streamers will have twitter
# and facebook posts created for them. The text of the messages will be slightly different
# if the option is O, no messages will be generated for this streamer

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

def getGreetings(filename):
#	streamerlist = {'napfan': {'twitter': 'tvanscotter', 'option': '', 'facebook': 'vanscotter'}}
#	return streamerlist
	greetingnum=0
	if os.path.isfile(filename):
		d={}
		with open(filename, 'r') as f:
			for line in f:
				greetingnum+=1
				d[greetingnum] = line.strip('\n')
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

def log(logfile,twitch,twitter,facebook,nominee,rerun,tkf,missed,multiple):

	if os.path.isfile(logfile):
		lfile = open(logfile, 'a')
		tweetcount = countTweets(logfile) + 1
	else:
		print (f'Creating logfile {logfile}\n')
		lfile = open(logfile, 'w')
		lfile.write('%20s\t%18s\t%18s\t%18s\t%s\t%s\t%s\n' %
			("date".ljust(20),"twitch".ljust(18),"twitter".ljust(18),"facebook".ljust(18),"tkftype".ljust(8),"live".ljust(10),"tkfOrNot".ljust(6))) 
		lfile.write('%20s\t%18s\t%18s\t%18s\t%s\t%s\t%s\n' %
			("----".ljust(20),"------".ljust(18),"-------".ljust(18),"--------".ljust(18),"-------".ljust(8),"----".ljust(10),"--------".ljust(6)))
		#lfile.write('%s' % 
		#	("date                          twitch                  twitter            facebook         tkftype         live            tkfORnot\n\n"))

	# there are 4 types for the stream as far as the log is concerned
	# a stream can be:
	# live - the normal situation, streamer goes live
	# rerun - streamer starts stream with a VOD
	# multiple - streamer issues subsequent now-live with-in an hour or so
	#            general assumption is that something went wrong and they
	#            re-started stream. no need to tweet/post again
	# missed - the streamer started a live stream and finished the live stream
	#          while I was AFK and did not get a chance to tweet/post

	if rerun:
		live="rerun"
	elif missed:
		live="missed"
	elif multiple:
		live="multiple"
	else:
		live="live"

	# Initially I was using this code to generate tweets for non-TKF streamers
	# those didn't contain any of the TKF tags/links
	# haven't been doing this for a while. may be time to pull this out of the code and log

	if tkf:
		tkfstr="notTKF"
	else:
		tkfstr="TKF"

	now = datetime.datetime.now()

	lfile.write('%4d-%02d-%02d %02d:%02d:%02d\t%18s\t%18s\t%18s\t%s\t%s\t%s\n' % 
		(now.year,now.month,now.day,now.hour,now.minute,now.second,twitch.ljust(18),twitter.ljust(18),
			facebook.ljust(18),nominee.ljust(8),live.ljust(10),tkfstr.ljust(6)))
#	lfile.write('\nnumber of tweets: %d\n' % (tweetcount))
	lfile.close()

def main():
	
#	sys.exit()

	msgidx = 1 # this determines if part of the message is 'Go check it out!' or 'Time to learn things!'
	nominee = "streamer" # the value will be changed to 'nominee' if the option value for the streamer
						 # the mapfile is N
	option = ""

	# I kind of got carried away with the command line args

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

	greetings = getGreetings('greetfile')

	# Use 'Time to learn things!' if arg -2 is present

	if args['message2']:
		msgidx = 2

	# if mapfile is provided on the command line then use it
	# otherwise use the default name

	if args['mapfile']:
		mapfile = args['mapfile']
	else:
		mapfile = "twitch_twitter.txt"

	# if logfile is provided on the command line then use it
	# otherwise use the defualt name

	if args['logfile']:
		logfile = args['logfile']
	else:
		logfile = "twitch_twitter.log"

	# set the default greeting for the tweet/post

	greeting="Hey everyone, "

	# if the greeting number was provided on the command line
	# then use that number to find the value in the greetings dictionary

	if args['greeting']:
		greeting =  greetings.get(int(args['greeting']), "Hola everyone, ")
	
	# verbose was mainly for testing. should either add a bunch of stuff
	# to display or remove the option altogether

	if args['verbose']:
		print ("mapfile: ",mapfile,"\nlogfile: ",logfile)
	
	# print the usage message if --usage on command line or no twitch handle provided

	if args['usage'] or not args['twitchhandle']:
		usage()
		sys.exit()
	
	streamer = args['twitchhandle']
	mapInfo = getHandleMapping(mapfile)

	# if twitter handle was not included in the arguments
	# then get it from the mapfile
	# i decided not to add a command argument for facebook handle
	# so we will always get the facebook handle from the mapfile
	# also get the option from the mapfile

	if not args['twitterhandle']:
		twitter = mapInfo[streamer]['twitter']
		if not twitter:
			twitter = '@' + args['twitchhandle']
	else:
		twitter = args['twitterhandle']

	option = mapInfo[streamer]['option']
	facebook = mapInfo[streamer]['facebook']

	if option == "N":
		nominee = "nominee"
	elif option == "O":
		print ("\nStreamer: ", args['twitchhandle'], " has opted out of personal tweets. RT from TKF twitter if streamer does their own tweet\n")
		sys.exit()

	# set up the string for the last part of the tweet / FB post

	if nominee == "nominee":
		htags="#NerdHype #TwitchEDU\nFind more like this at @TheKnowledgeFe1"
		htagsFB="#NerdHype #TwitchEDU\nFind more like this at https://twitter.com/TheKnowledgeFe1"
	else:
		htags="#NerdHype #TwitchEDU\nFind this and more at @TheKnowledgeFe1"
		htagsFB="#NerdHype #TwitchEDU\nFind this and more at https://twitter.com/TheKnowledgeFe1"

	# print something if no stream text / stream title provided

	if not args['streamtext']:
		streamertext = 'enjoy the stream!'
	else:
		streamertext = args['streamtext']
	
	# this makes a slight change to the first line of the tweet / FB post
	# just for a little variety so we aren't completelt bot-ish

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

	# if the streamer said it was a re-run change include that in the tweet / FB post

	livererun=""
	if args["reRun"]:
		livererun = " is showing a re-run on https://www.twitch.tv"
	else:
		livererun = " is live on https://www.twitch.tv/"
	
	stream = "\n" + streamer + livererun + streamer + " ! Go check it out!\n"

	if args['dontShowCopyPasta']:
		print ("\nDISCORD: copy/pasta this for TKF discord #now-live channel")
	
	# print the discord link

	if not args['missed'] and not args['multiples']:
		print (stream)
	
	stream = greeting + twitter + livererun + streamer + moretext + "\n"

	stream+= streamertext.strip('\n') + "\n"

	# originally, I was using this to generate tweets for non-TKF streamers
	# haven't been doing that lately but the code still is still here
	# it does not include any TKF tags / links
	
	if not args['notTKF']:
		stream+= htags + "\n"
	if args['dontShowCopyPasta']:
		print ("TWITTER: copy/pasta this for tweet\n")

	# print the tweet. if the size is more than the limit, remove something after pasting into twitter
	# if the tweet opertion is ever automated this code will have to do the size reduction somehow

	if not args['missed'] and not args['multiples']:
		print (stream)
		print ("Tweet is " + str(len(stream)) + " characters. 280 max.\n")

	# generate the facebook post text

	# twitchURL = "https://www.twitch.tv/" + streamer

	stream = greeting

	if not facebook:
		stream+= streamer
	else:
		stream+= facebook
	
	stream+= livererun + streamer + moretext + "\n"
	
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
		if '@' not in twitter:
			twitter=""
		log(logfile,streamer,twitter,facebook,nominee,args['reRun'],args['notTKF'],args['missed'],args['multiples'])

	sys.exit()
	
main()
