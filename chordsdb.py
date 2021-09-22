import random

chords = {"E":      "022100",
          "Em":     "022000",
          "E7":     "020100",
          "Em7":    "020030",
          "EMaj7":  "021100",
          "A":      "x02220",
          "Am":     "x02210",
          "A7":     "x02020",
          "Am7":    "x02010",
          "AMaj7":  "x02120",
          "D":      "xx0232",
          "Dm":     "xx0231", 
          "D7":     "xx0212", 
          "Dm7":    "xx0211", 
          "DMaj7":  "xx0222", 
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
    

c=""
for i in range(10):
    c = pickRandomChord(c);
    print(chord2Ascii(c))    
