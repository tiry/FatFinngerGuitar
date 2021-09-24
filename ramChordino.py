from chord_extractor.extractors import Chordino
from chord_extractor.base import ChordChange
import vamp
from typing import List

class RAMChordino(Chordino):

    def ramExtract(self, data, rate) -> List[ChordChange]:

        #for i in range(0, len(data)):
        #    print (str(data[i]) + " " + str(type(data[i])))
        chords = vamp.collect(data, rate, 'nnls-chroma:chordino', parameters=self._params)
        return [ChordChange(timestamp=float(change['timestamp']),
                            chord=change['label']) for change in chords['list']]

