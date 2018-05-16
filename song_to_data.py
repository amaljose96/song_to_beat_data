from aubio import source, tempo
import sys
import os

"""
Main Objective:
Input : An MP3 file containing a song
Output : A data structure containing data related to each beat.
"""


#Step 1 : Read the data
if(len(sys.argv)<2):
    print("Filename not given.")
    exit();
song_name=sys.argv[1]
win_s, hop_s = 256, 128                                 #Set as a standard for future use.
samplerate= 44100                                       #Most of the songs are 44100Hz

s = source(song_name, 0, hop_s)
print("Opening file "+song_name)
samplerate=s.samplerate
print("Sample rate="+str(s.samplerate))
tempo_finder = tempo("default", win_s, hop_s, samplerate)   #aubio's tempo : Used to find beat frame



samples_per_beat=[]
no_samples_for_beat=0
beat_no=0
frames_limit=80

s = source(song_name, 0, hop_s)                     #Opening song file.
samplerate=s.samplerate

frames_count=0;
data_count=0;
beat_count=0;
print("\nNow writing data into beats_data.txt")
output=open("beats_data_unverified.txt","w");

while True:
    samples, read = s()
    if(frames_count<frames_limit):              #If not reached limit, write into file
        for sample in samples:
            output.write(str(sample)+"\t")
            data_count=data_count+1;
        frames_count=frames_count+1;
    is_beat = tempo_finder(samples)
    if is_beat:                                 #If a beat, reset everything and output \n
        print("Wrote beat "+str(beat_count)+" with "+str(frames_count)+" frames and "+str(data_count)+" columns")
        sys.stdout.write("\033[F")
        beat_count=beat_count+1;
        frames_count=0
        data_count=0;
        output.write("\n")
    if read < hop_s:
        break

print("\n"+str(beat_count)+" rows. ")
print("Verifying data....");
#VERIFICATION PART : To check if all data points have the required dimensions
req_samples=frames_limit*hop_s+1;                   #The +1 is to account for the last empty element. To be fixed later.
data=[]
inputfile=open("beats_data_unverified.txt","r")
outputfile=open("beats_data.txt","w")
row_widths=[]
for line in inputfile:
    data.append(line)
    row_widths.append(len(line.rstrip("\n").split("\t")))

outputfile.write(str(hop_s)+"\t"+str(frames_limit)+"\t"+str(samplerate)+"\n")
row=0;
for rw in row_widths:
    if(req_samples!=rw):
        print("Data "+str(row)+" corrupt with "+str(rw)+" and not "+str(req_samples))  #Not the required dimensions, discarded
    else:
        outputfile.write(data[row])
    row=row+1;
print("Verified data.")
newname=song_name.split('.')[0]+"_data.txt"
os.rename("beats_data.txt", newname)
os.remove("beats_data_unverified.txt")
