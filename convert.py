import urllib
import os

def covertSong(url):
	os.system("rm -f output.mp3")
	urllib.request.urlretrieve(url, "newsong")
	command = "ffmpeg -i newsong -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 output.mp3"
	os.system(command)
