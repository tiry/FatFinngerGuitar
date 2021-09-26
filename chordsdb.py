import random
import time
import chordisplay

chords = {"E":      "022100",
          "Em":     "022000",
          "E7":     "020100",
          "Em7":    "020030",
          "Emaj7":  "021100",
          "A":      "x02220",
          "Am":     "x02210",
          "A7":     "x02020",
          "Am7":    "x02010",
          "Amaj7":  "x02120",
          "D":      "xx0232",
          "Dm":     "xx0231", 
          "D7":     "xx0212", 
          "Dm7":    "xx0211", 
          "Dmaj7":  "xx0222", 
          "C":      "x32010", 
          "G":      "320033", 
          "F":      "x3321x", 
          }

def chord2Ascii(chord):

  fingers = chords[chord]
  pad= " "*2
  lines=[]
  
  if (len(chord)>3):
    lines.append(pad + chord)
  else:
    lines.append(pad*2 + chord)
  
  head="0 "
  for letter in fingers:
    if letter=="x":
      head=head+"X"  
    else:
      head = head + "="

  lines.append(head)
  for fretIdx in range(1,9):
    fret=pad
    for string in fingers:
      if string==str(fretIdx):
        fret=fret+"O"
      else:
        fret = fret + "|"
    lines.append(fret)

  while (lines[-1]==pad + "||||||" and len(lines)>6):
    lines.pop()  
  return "\n".join(lines)


def pickRandomChord(prev):
    chord = prev
    while (prev==chord):
        idx = random.randrange(0, len(chords))
        chord = list(chords.keys())[idx]
    return chord
    
def generateRandomChords(chordsCount):
    c=""
    l=[]
    for i in range(chordsCount):
        c = pickRandomChord(c);
        l.append(c)
    return l

def generateRandomChordsGroups(groupCount):
    c=""
    l=[]
    for i in range(groupCount):
        c = pickRandomChord(c);
        
        note = c[:1]
        for chord in chords:
            if chord[:1]==note:
                l.append(chord);
    return l


def buildTest(scenarioId, count):

    test=[]

    selectedChords = []
    if (scenarioId==0):
        selectedChords = generateRandomChords(count)
    elif (scenarioId==1):
        selectedChords = generateRandomChordsGroups(1+int(count/5))[:count]
    else:
        print("unknown scenario")
        return test 

    #print("selectedChords")
    #print(str(selectedChords))

    for c in selectedChords:
        test.append({
            "name" : c,
            "fingers" : chords[c],
            "allocatedTimeS" : 6,
            "executionTimeS" : 0,
            # state = -1 : not run
            # state = 1 : success with visual help
            # state = 2 : success without visual help
            # state = 0 : failed / timeout
            "state": -1,
            "started": 0
            })
    return test

def default_wasChordPlayed(chord):
    return False;

def _runStep(step, wasChordPlayed):

    #print(step);

    t0=time.time()
    step["started"]=t0

    print("\n\n\n")
    print("_"*60)
    
    print(" Play " + step["name"] )
    
    chordisplay.displayChord(step["name"])


    while time.time()-t0<step["allocatedTimeS"]:
        time.sleep(0.1)
        if wasChordPlayed(step["name"]):
            step["state"] = 2
            step["executionTimeS"] = time.time()-t0
            return

    if step["state"] < 2:
        # second chance
        print("\nReview chord diagram\n")
        print(chord2Ascii(step["name"]))
        chordisplay.displayChord(step["name"], chords[step["name"]])


    while time.time()-t0<2*step["allocatedTimeS"]:
        time.sleep(0.1)
        if wasChordPlayed(step["name"]):
            step["state"] = 1
            step["executionTimeS"] = time.time()-t0
            return

    step["executionTimeS"] = time.time()-t0
    if step["state"] == -1:
        step["state"] = 0


def runScenario(scenarioId, count, wasChordPlayed):

    if (wasChordPlayed==None):
        wasChordPlayed = default_wasChordPlayed

    test = buildTest(scenarioId, count)
    for step in test:
        _runStep(step, wasChordPlayed)
    return test

def printTest(test):
    count = len(test)
    score = 0
    avgTime = 0
    for s in test:
        score = score + s["state"]
        avgTime = avgTime + s["executionTimeS"]
    print(" Score {0} / {1} ".format(score, count*2))
    avgTime = avgTime / count
    print(" Average Response tome (s) {0} ".format(avgTime))
    
        

#for c in generateRandomChords(10):
#    print(chord2Ascii(c))    



#for c in generateRandomChordsGroups(5):
#    print(chord2Ascii(c))    

#print(buildTest(0, 11))

#print(buildTest(1, 11))


#runScenario(0, 5)


