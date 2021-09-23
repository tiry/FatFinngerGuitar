import sys
import signal
import os
import jack
import threading
import numpy
import time
from scipy.io.wavfile import write
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence
import chordsdb

# Guitar port in Jack 
guitar_port=1
# amplify captured signal
amplify=50000
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
    
    fileName ="output_" + str(counter)+ "_.wav" 
    write(fileName, fs, capture)
    guitar_signal=guitar_signal[int(3*cap_frames/4):]
    counter=counter+1
    samples_to_process.append(fileName)


@client.set_process_callback
def process(frames):
    #assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    data =  numpy.int16(client.inports[0].get_array() * amplify)
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

def chordsFound_cb(results: LabelledChordSequence):
  global lastChord
  global recentChords
  for chord in results.sequence:
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
        time.sleep(1)

chordino = Chordino(roll_on=1)
clear_conversion_cache()

max_samples_to_process=10

def checkChords():  
  global samples_to_process
  if len(samples_to_process)==0:
    print("nothing to check")
    return
  if len(samples_to_process)> max_samples_to_process:
    samples_to_process=samples_to_process[-max_samples_to_process:]
  
  files_to_extract_from=[]
  while (len(samples_to_process)>0 and len(files_to_extract_from)<max_samples_to_process):
    files_to_extract_from.append(samples_to_process.pop(0));

  res = chordino.extract_many(files_to_extract_from, callback=chordsFound_cb, num_extractors=4,
                              num_preprocessors=4, max_files_in_cache=50, stop_on_error=False)

  for processed in files_to_extract_from:
    os.remove(processed)

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
    quiz.start()

    print("Press Ctrl+C to stop")
    try:
        event.wait()
    except KeyboardInterrupt:
        print("\nInterrupted by user")