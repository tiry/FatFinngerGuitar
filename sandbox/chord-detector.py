import sounddevice as sd
import sys, getopt
from scipy.io.wavfile import write
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence
import threading

fs = 44100  # Sample rate
seconds = 1  # Duration of recording
sd.default.channels = 0, 2
sd.default.device=None,18

seq=0;
samples_to_process=[];

def record(duration): 
   print("Listener for " + str(duration) + " s")
   newrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
   sd.wait()  # Wait until recording is finished
   fname = 'output' + seq + '.wav'
   write(fname, fs, newrecording)  # Save as WAV file 
   seq=seq+1
   samples_to_process.append(fname)

def chordsFound_cb(results: LabelledChordSequence):
  # Every time one of the files has had chords extracted, receive the chords here
  # along with the name of the original file and then run some logic here, e.g. to
  # save the latest data to DBb
  print(results)

def checkChords():

  chordino = Chordino(roll_on=1)

  # Optionally clear cache of file conversions (e.g. wav files that have been converted from midi)
  clear_conversion_cache()

  files_to_extract_from=[]
  while (len(samples_to_process)>0 and len(files_to_extract_from<5)):
    files_to_extract_from.append(samples_to_process.pop(0));

  res = chordino.extract_many(files_to_extract_from, callback=chordsFound_cb, num_extractors=2,
                              num_preprocessors=2, max_files_in_cache=10, stop_on_error=False)


def main(argv):

   print("start detector thread")   
   detector = threading.Thread(target=checkChords, args=())
   detector.start()

   print("Start listen loop")
   while(True):
      record(seconds);


if __name__ == "__main__":
   main(sys.argv[1:])

