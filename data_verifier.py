import sys
import os
if(len(sys.argv)<2):
    print("Filename not given.")
    exit();
data_name=sys.argv[1]

data=[]
inputfile=open(data_name,"r")
outputfile=open("beats_data_verified.txt","w")
row_widths=[]
for line in inputfile:
    data.append(line)
    row_widths.append(len(line.rstrip("\n").split("\t")))

header=data[0]
data=data[1:]
row_widths=row_widths[1:]
hop_s=int(header.rstrip("\n").split("\t")[0])
frames_limit=int(header.rstrip("\n").split("\t")[1])
samplerate=int(header.rstrip("\n").split("\t")[2])
print("Read data with hop_s="+str(hop_s)+" and frames per beat="+str(frames_limit)+" Sample rate = "+str(samplerate))
test_value=row_widths[0]
row=0;
outputfile.write(str(hop_s)+"\t"+str(frames_limit)+"\t"+str(samplerate)+"\n")
for rw in row_widths:
    if(test_value!=rw):
        print("Data "+str(row)+" corrupt with "+str(rw)+" and not "+str(test_value))
    else:
        outputfile.write(data[row])
    row=row+1;
print("Data has "+str(len(row_widths))+" rows and "+str(row_widths[0])+" columns")

os.remove(data_name)
os.rename("beats_data_verified.txt",data_name)
