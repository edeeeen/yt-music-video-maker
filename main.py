import subprocess, glob
from datetime import timedelta
from mutagen.mp3 import EasyMP3 

var = "ffmpeg -i \"concat:"
timetabletimes = [timedelta(seconds=0)]
timetablestrings = []
x=0
album = ""
songTitle = ""
artist = ""
# loop through each mp3 file
for file in glob.glob("*.mp3"):
    mp3 = EasyMP3(file)
    album = str(mp3["Album"][0])
    songTitle = str(mp3["Title"][0])
    artist = str(mp3["Artist"][0])
    #add the times together
    timetabletimes.append(timedelta(seconds=int(mp3.info.length)) + timetabletimes[x])
    #if it is less than an hour then get rid of the hour place
    if (str(timetabletimes[x])[0] == '0'):
        timetablestrings.append(str(timetabletimes[x])[2:] + " " + file.split(" ", 1)[1].split(".mp3")[0])
    else:
        timetablestrings.append(str(timetabletimes[x]) + " " + file.split(" ", 1)[1].split(".mp3")[0])
    var += file + "|"
    #make the video from cover.jpg
    subprocess.run("ffmpeg -loop 1 -i cover.jpg -i \"" + file + "\" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \"" + artist + " - " + songTitle + ".mp4\"")
    x += 1
var += "\" -c copy all.mp3"
#concat each track into all.mp3 then make a video from it.
subprocess.run(var)
subprocess.run("ffmpeg -loop 1 -i cover.jpg -i all.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \"" + artist + " - " + album + " [Full Album]" + ".mp4")
#print out the times for the description
for w in timetablestrings:
    print(w)