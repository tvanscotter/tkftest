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

def log(logfile,twitch,twitter,facebook,nominee,rerun,nottkf,misseddupe):

	if os.path.isfile(logfile):
		lfile = open(logfile, 'a')
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
	elif misseddupe:
		live=misseddupe
	else:
		live="live"

	# Initially I was using this code to generate tweets for non-TKF streamers
	# those didn't contain any of the TKF tags/links
	# haven't been doing this for a while. may be time to pull this out of the code and log

	if nottkf:
		tkfstr="notTKF"
	else:
		tkfstr="TKF"

	now = datetime.datetime.now()

	if nominee == "N":
		nominee = "nominee"
	else:
		nominee = "streamer"
	
	if '@' not in twitter:
		twitterstr=""
	else:
		twitterstr=twitter
	
	lfile.write('%4d-%02d-%02d %02d:%02d:%02d\t%18s\t%18s\t%18s\t%s\t%s\t%s\n' % 
		(now.year,now.month,now.day,now.hour,now.minute,now.second,twitch.ljust(18),twitterstr.ljust(18),
			facebook.ljust(18),nominee.ljust(8),live.ljust(10),tkfstr.ljust(6)))
#	lfile.write('\nnumber of tweets: %d\n' % (tweetcount))
	lfile.close()

class discordMsg():
	"""docstring for discordMsg"""
	def __init__(self, streamer, rerun, showheaders):
		super(discordMsg, self).__init__()
		self.streamer = streamer
		self.rerun = rerun
		self.showheaders = showheaders
	def text(self):
		text=""
		live = " is now live on "
		notlive = " is now showing a rerun on "
		if self.rerun:
			status = notlive
		else:
			status = live
		if self.showheaders:
			text = "\nDISCORD: copy/pasta this for discord post\n"
		
		text += "\n" + self.streamer + status + "https://www.twitch.tv/" + self.streamer + " ! Go check it out!\n"
		return text
		
class getCommon():
	"""docstring for getCommon"""
	def __init__(self,args):
		super(getCommon, self).__init__()
		self.args = args
		if self.args['mapfile']:
			filename = self.args['mapfile']
		else:
			filename = 'twitch_twitter.txt'
		self.mapInfo = getHandleMapping(filename)
		self.streamer = self.args['twitchhandle']
	def greeting(self):
		if self.args['greeting']:
			greetings = getGreetings('greetfile')
			return greetings.get(int(self.args['greeting']), "Yo nerds, ")
		else:
			return("Hey everyone, ")
	def endline1(self):
		if self.args['message2']:
			return("Time to learn things!")
		else:
			return("Go check it out!")
	def logfile(self):
		if self.args['logfile']:
			return(self.args['logfile'])
		else:
			return("twitch_twitter.log")
	def twitchhandle(self):
		return(self.args['twitchhandle'])
	def twitter(self):
		return(self.mapInfo[self.streamer]['twitter'])
	def facebook(self):
		return(self.mapInfo[self.streamer]['facebook'])
	def option(self):
		return(self.mapInfo[self.streamer]['option'])
	def verbose(self):
		return(self.args['verbose'])
	def rerun(self):
		return(self.args['reRun'])
	def twitterlastlines(self):
		if self.mapInfo[self.streamer]['option'] == "N":
			return("#NerdHype #TwitchEDU\nFind more like this at @TheKnowledgeFe1")
		else:
			return("#NerdHype #TwitchEDU\nFind this and more at @TheKnowledgeFe1")
	def facebooklastlines(self):
		if self.mapInfo[self.streamer]['option'] == "N":
			return("#NerdHype #TwitchEDU\nFind more like this at https://twitter.com/TheKnowledgeFe1")
		else:
			return("#NerdHype #TwitchEDU\nFind this and more at https://twitter.com/TheKnowledgeFe1")
	def livererun(self):
		if self.args['reRun']:
			return(" is showing a rerun on ")
		else:
			return(" is live on ")
	def misseddupe(self):
		if self.args['missed']:
			return("missed")
		elif self.args['multiples']:
			return('duplicate')
		else:
			return(False)
	def streamertext(self):
		return(self.args['streamtext'])
	def showheaders(self):
		if self.args['dontShowCopyPasta']:
			return(False)
		else:
			return(True)
	def nolog(self):
		if self.args['nolog']:
			return(True)
		else:
			return(False)
	def notTKF(self):
		return(self.args['notTKF'])

class twitterMsg():
	"""docstring for twitterMsg"""
	def __init__(self, greeting, streamer, livererun, endline1, streamertext, lastlines, twitter, showheaders):
		super(twitterMsg, self).__init__()
		self.greeting = greeting
		self.streamer = streamer
		self.livererun = livererun
		self.endline1 = endline1
		self.streamertext = streamertext
		self.lastlines = lastlines
		self.twitter = twitter
		self.showheaders = showheaders
	def text(self):
		text=""
		twitchurl = "https://www.twitch.tv/"
		if self.twitter:
			handle = self.twitter
		else:
			handle = self.streamer
		if self.showheaders:
			text = "TWITTER: copy/pasta this for tweet\n\n"
		
		text += self.greeting + handle + self.livererun + twitchurl + self.streamer + " ! " + self.endline1 + "\n"
		text += self.streamertext + "\n"
		text += self.lastlines + "\n"
		return(text)

class facebookMsg():
	"""docstring for twitterMsg"""
	def __init__(self, greeting, streamer, livererun, endline1, streamertext, lastlines, twitter, facebook, showheaders):
		super(facebookMsg, self).__init__()
		self.greeting = greeting
		self.streamer = streamer
		self.livererun = livererun
		self.endline1 = endline1
		self.streamertext = streamertext
		self.lastlines = lastlines
		self.twitter = twitter
		self.facebook = facebook
		self.showheaders = showheaders
	def text(self):
		text=""
		twitchurl = "https://www.twitch.tv/"
		twitterurl = "https://twitter.com/"
		if self.facebook:
			handle = self.facebook
		else:
			handle = self.streamer
		if self.showheaders:
			text = "FACEBOOK: copy/pasta this for FB post\n\n"
		
		text += self.greeting + handle + self.livererun + twitchurl + self.streamer + " ! " + self.endline1 + "\n"
		text += '"' + self.streamertext + '"' 
		if '@' in self.twitter:
			text += "\nTwitter: " + twitterurl + self.twitter[2:]
		text += "\n"
		text += self.lastlines + "\n"
		return(text)

def main():

	# I kind of got carried away with the command line args

	parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

	parser.add_argument('-c','--changeCheckItOut', help='change the Check it out message to this string', required=False)
	parser.add_argument('-d','--dontShowCopyPasta', help='dont show the copy/pasta messages', action='store_true', required=False)
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

		# print the usage message if --usage on command line or no twitch handle provided

	if args['usage'] or not args['twitchhandle']:
		usage()
		sys.exit()

	common = getCommon(args)

	if common.verbose():

		print ("greeting:", common.greeting())
		print ("endline1:", common.endline1())
		print ("logfile:", common.logfile())
		print ("twitchhandle:", common.twitchhandle())
		print ("twitter:", common.twitter())
		print ("facebook:", common.facebook())
		print ("option:", common.option())
		print ("twitterlastlines:", common.twitterlastlines())
		print ("facebooklastlines:", common.facebooklastlines())
		print ("livererun:", common.livererun())
		print ("streamertext:", common.streamertext())
		print ("showheaders:", common.showheaders())

	if common.option() == 'O':
		print ("\nStreamer:", common.twitchhandle(), "has opted out of tweets, FB posts from TKF.\n")
		sys.exit()

	if not common.misseddupe():
		discord = discordMsg(common.twitchhandle(),common.rerun(),common.showheaders())
		print (discord.text())

		twitter = twitterMsg(common.greeting(),common.twitchhandle(),common.livererun(),common.endline1(),common.streamertext(),
		common.twitterlastlines(),common.twitter(),common.showheaders())
		print (twitter.text())
	
		facebook = facebookMsg(common.greeting(),common.twitchhandle(),common.livererun(),common.endline1(),common.streamertext(),
		common.facebooklastlines(),common.twitter(),common.facebook(),common.showheaders())
		print (facebook.text())

	if common.nolog():
		print("Log will not be added for", common.twitchhandle())
	elif common.misseddupe():
		print(common.misseddupe(), "now-live logged for", common.twitchhandle())
	else:
		print("Now-live logged for", common.twitchhandle())
	log(common.logfile(),common.twitchhandle(),common.twitter(),common.facebook(),common.option(),
	common.rerun(),False,common.misseddupe())
	sys.exit()
	
main()
