# Song to Beat Data

This project converts a song into an unlabelled dataset which can be used for other purposes.
This project uses [Aubio module](https://github.com/aubio/aubio) by @aubio .

## song_to_data.py

This file takes in an mp3 file. All mp3 files are supported. The maximum tempo of the song is 250bpm.
Output of this file is the entire song converted into numerical data. (saved as <song_name\>\_data.txt)
This output file consists of just 80 frames of data at every beat.

### How it works

The music file is read using **source**. The hopsize is fixed at 128.

Now, 128 samples are read as a frame. The tempo detector (using aubio) detects if its a beat or not. If its a beat a new data point is initiated as empty. If its not a beat, its appended to the current data point.
80 such frames are appended into a datapoint. This gives a total of 10,240 data points for a beat. (with a sampling rate of 44100, this corresponds to 0.2s of sound)
The data points corresponding to each beat is saved into <song_name\>\_data.txt

The outputfile has a header consisting of hop size, frames in a data point and sampling rate.

The data is also verified to contain same dimensions as hopsize*frames ie. 10240.

Note : This data can be played again using **sink** in aubio after reshaping a datapoint into (hopsize,frames)


## data_verifier.py

This file takes in <song_name\>\_data.txt as input and checks if every datapoint is of hopsize*frames dimensions ie. 10240 columns.

## Installation

You require aubio module.

> pip install aubio

## Usage

To run the converter

> python2 song_to_data.py \<Name of the music file\>

To run the data_verifier

> python2 data_verifier.py <song_name\>\_data.txt
