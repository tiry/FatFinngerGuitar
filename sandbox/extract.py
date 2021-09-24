from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence
import sys, getopt

files_to_extract_from = [
  'rsi.wav'
#  ,'output.wav'
]

#for i in range(0,30):
#  files_to_extract_from.append("output_" + str(i) + "_.wav")

lastChord=""

def save_to_db_cb(results: LabelledChordSequence):
  # Every time one of the files has had chords extracted, receive the chords here
  # along with the name of the original file and then run some logic here, e.g. to
  # save the latest data to DBb
  #print(results)
  global lastChord
  for chord in results.sequence:
    if (chord.chord!='N'):
      if (lastChord!=chord.chord):
        lastChord=chord.chord
        print(lastChord)

def main(argv):

  chordino = Chordino(roll_on=1)


  # Optionally clear cache of file conversions (e.g. wav files that have been converted from midi)
  clear_conversion_cache()

  res = chordino.extract_many(files_to_extract_from, callback=save_to_db_cb, num_extractors=2,
                              num_preprocessors=2, max_files_in_cache=10, stop_on_error=False)

if __name__ == "__main__":
  main(sys.argv[1:])
