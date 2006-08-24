import sys
import os
import locale
import gettext
import ConfigParser
import socket

from wax import *
from wax.tools.choicedialog import ChoiceDialog
from wax.tools.progressdialog import ProgressDialog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT

sys.path.append(os.path.realpath('../'))

import const
from searchlyrics import SearchLyrics

def _(data):
	return data

#socket.setdefaulttimeout(10)

artist = "Simple Plan"
song = "Jump"

search = SearchLyrics()
result = search.SearchLyrics(artist, song)

if result.has_key('error'):
	error = result['error']
	print error

if result.has_key('songlist') == False:
	print _("No correspondence found 1")

elif len(result['songlist']) == 0:
	print _("No correspondence found 2")
		
else:
	songSelected = []

	# Song choice
	if len(result['songlist'].values()) == 1:
			songSelected = result['songlist'][0]
	else:
			choices = []
			
			for results in result['songlist'].values():
					choices.append("%s - %s"  % (results[1], results[0]))
					
			print choices

	# Download lyrics
	lyrics = []
	lyrics['artist'] = songSelected[0]
	lyrics['song'] = songSelected[1]
	lyrics['hid'] = songSelected[2]

	print "Downloading '%s' ..." % (lyrics['song'])
	lyrics['lyrics'] = search.ShowLyrics(lyrics['hid'])
					
	# Detect errors
	if lyrics['lyrics'].has_key('error'):
			error = lyrics['lyrics']['error']
			errorFrame = MessageDialog(self, _("Error"), error, ok=1,
																icon='error')
			errorFrame.ShowModal()
			errorFrame.Destroy()
			statusBar[1] = error

	nb.tab[cTab].lyricsText.Clear()

	for lines in lyrics['lyrics']['lyrics'].split('\n'):
			print lines.strip()
			
	print "[%s - %s]\r\r" % (lyrics['artist'], lyrics['song'])