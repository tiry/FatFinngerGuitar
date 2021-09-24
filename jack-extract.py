import sys
import signal
import os
import jack
import threading
import numpy
import time
from scipy.io.wavfile import write
from chord_extractor.extractors import Chordino
from ramChordino import RAMChordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence
import chordsdb

# Guitar port in Jack 
guitar_port=1
# amplify captured signal
amplify=5
# Sampling rate
fs = 44100 

# frames captured before flushing
cap_frames=150

clientname = "Tiry Chord Listener"
servername = None
lastChord = ""

argv = iter(sys.argv)

client = jack.Client(clientname, servername=servername)

if client.status.server_started:
    print("JACK server started")
if client.status.name_not_unique:
    print("unique name {0!r} assigned".format(client.name))

event = threading.Event()

samples_to_process=[]
guitar_signal=[]
counter=0

def dumpFrames():
    global guitar_signal
    global counter
    global samples_to_process
    capture = numpy.concatenate(guitar_signal)
    guitar_signal=guitar_signal[int(3*cap_frames/4):]
    counter=counter+1
    samples_to_process.append(capture)

@client.set_process_callback
def process(frames):
    assert frames == client.blocksize
    data = numpy.asarray(client.inports[0].get_array() * amplify).astype(numpy.float32)
    guitar_signal.append(data)
    if (len(guitar_signal)>cap_frames):
        dumpFrames()

@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown!")
    print("status:", status)
    print("reason:", reason)
    event.set()

recentChords=[]
chordino = RAMChordino(roll_on=1)
clear_conversion_cache()
max_samples_to_process=10

### handle Chord detector

def chordsFound_cb(results: LabelledChordSequence):
  global lastChord
  global recentChords
  for chord in results:
    played=chord.chord.strip()
    if (played!='N'):
      if (lastChord!=played):
        lastChord=played
        recentChords.append(lastChord)
        if (len(recentChords)>4):
            recentChords=recentChords[:4]
        print(lastChord)

def chordWatcher():
    while True:
        if len(samples_to_process)>0:
            checkChords()
        time.sleep(0.1)

def checkChords():  
  global samples_to_process
  if len(samples_to_process)==0:
    print("nothing to check")
    return

  while (len(samples_to_process)>0):
    sample = samples_to_process.pop(0)
    #sample = numpy.asarray(sample).astype(numpy.float32)
    res = chordino.ramExtract(sample, fs)
    chordsFound_cb(res)

### Handle Test

def wasChordPlayed(chord):
    #print("looking for " + chord + " in " + str(recentChords))
    for c in recentChords:
        if c==chord:
            print("\nYEAHHHHHH!!!\n")
            return True
    return False

def chordQuestions():
    test=chordsdb.runScenario(0, 5, wasChordPlayed)
    print("\n" +"-"*40 + " end of test \n")
    chordsdb.printTest(test)

client.inports.register("input_0")


with client:
    # When entering this with-statement, client.activate() is called.
    # This tells the JACK server that we are ready to roll.
    # Our process() callback will start running now.

    # Connect the ports.  You can't do this before the client is activated,
    # because we can't make connections to clients that aren't running.
    # Note the confusing (but necessary) orientation of the driver backend
    # ports: playback ports are "input" to the backend, and capture ports
    # are "output" from it.

    capture = client.get_ports(is_physical=True, is_output=True)
    if not capture:
        raise RuntimeError("No physical capture ports")

    client.connect(capture[guitar_port], client.inports[0])

    print("start detector thread")   
    detector = threading.Thread(target=chordWatcher, args=())
    detector.start()


    print("start quizz thread")   
    quiz = threading.Thread(target=chordQuestions, args=())
    #quiz.start()

    print("Press Ctrl+C to stop")
    try:
        event.wait()
    except KeyboardInterrupt:
        print("\nInterrupted by user")