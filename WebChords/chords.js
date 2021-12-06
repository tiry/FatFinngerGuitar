let keyCtl, title, notesDisplay ,tableDisplay, formula;

let notes = "A-BC-D-EF-G"

let notesLabels=[]

let formulas = {
  "major" : [2,2,1,2,2,2,1],
  "minor" : [2,1,2,2,1,2,2]
}

let keySelectorWidth=300;

let selectedKeyIndex=0;

function getKeyByIndex(idx) {
  if (idx == notes.length) {
    return "G#";
  }
  k = notes[idx];
  if (k=="-") {
    k = notes[idx-1]+ "#";
  }
  return k;
}

function getSelectedKey() {
  idx = keyCtl.value();
  currentKey = getKeyByIndex(idx);
  notesLabels[idx].style("color", "red");
  if (selectedKeyIndex!=idx) {
    notesLabels[selectedKeyIndex].style("color", "black");
  }
  selectedKeyIndex=idx;
  return currentKey;
}

function getKeyIndex(key) {

  k = key[0];
  for (i=0; i < notes.length; i++) {
    if (k==notes[i]) {
      break;
    }
  } 
  if (key.length>1) {
    if (key[1]=="#") {
      return i+1;
    } else {
      return i-1;
    }
  }
  return i;
}


function getFormula() {
  return formula.value();
}

function setup() {
  // create canvas
  createCanvas(1000, 800);

  // create Key Selector
  let label = createElement('h2', 'Key:');
  label.position(20, 5);

  keyCtl = createSlider(0, 10, 0, 1);
  keyCtl.position(100, 65);
  keyCtl.style('width', keySelectorWidth+'px');


  keyCtl.input(function() {redraw()});


  for (n in notes) {
    l = createElement('h2', notes[n]);
    l.position(100-5 +n*(keySelectorWidth/10), 5);
    notesLabels.push(l);
  }

  // create Formula Selector
  label = createElement('h2', 'Formula :');
  label.position(460,5);

  formula = createRadio();
  for (f in formulas) {
    formula.option(f, f);
  }
  formula.selected('major'); 
  formula.style('width', '400px');
  formula.position(580, 30);

  formula.input(function() {redraw()});

  title = createElement('h1', '');
  title.position(500,80);

  notesDisplay = createElement('h1', 'XXXX');
  notesDisplay.position(750,10);


  tableDisplay = createElement('div', 'XXXX');
  tableDisplay.position(50,150);

  textAlign(CENTER);
  textSize(50);


  noLoop();
}


function getNotesSerie(key, formula) {
  l = [];

  idx = getKeyIndex(key);

  l.push(key);

  intervals = formulas[formula];

  f=0;
  
  for (i=1; i < 14; i++) {

    if (intervals[f]>1) {
      l.push("-");
    }
    idx = (idx + intervals[f])%12;
    l.push(getKeyByIndex(idx));
    f=(f+1)%7;
  }

  return l;
}

function findChord(kNotes, idx) {

  let components = [kNotes[idx]];

  let intervals =[];

  let steps = 1;
  let count = 1;

  // locate triad
  while (components.length<3) {
    n = kNotes[idx+steps];
    if (n!="-") {
      count++
      // third
      if (count==3 || count==5) {
        components.push(n);
        intervals.push(steps);
      }
    }
    steps++;
  }

  name = components[0] + " ";
  s1=intervals[0];
  s2=intervals[1]-s1;

  let quality="";

  if (s1==4 && s2==3) {
    quality = "Major";
  }
  else if (s1==3 && s2==4) {
    quality = "minor";
  }
  else if (s1==3 && s2==3) {
    quality = "Dim";
  } else {
    quality = "WTF";
  }

  return { name: name + quality, notes: components};
}

function findChords(kNotes) {

  chords=[];

  idx=0;

  while (idx < kNotes.length && chords.length<7) {

    let root = kNotes[idx];
    if (root!="-") {
      chords.push(findChord(kNotes, idx));
    }
    idx++;
  }

  return chords;
}

function getChordPictureURL(name, idx) {

  let root = name[0];
  let sharp=false;
  let flat=false;
  let quality = name.substring(1);

  if (name[1]=="#") {
    sharp=true;
    quality = name.substring(2); 

    if (root=="G") {
      root="A";
      sharp=false;
      flat=true;
    }
    else if (root=="A") {
      root="B";
      sharp=false;
      flat=true;
    }
    else if (root=="D") {
      root="E";
      sharp=false;
      flat=true;
    }
  }


  let base = root.toUpperCase();
  if (sharp) {
    base = base + "sharp";
  } else if (flat) {
    base = base + "b";
  }

  url = "https://tombatossals.github.io/react-chords/media/guitar/chords/";

  url += base + "/";
  url += quality.trim().toLowerCase() + "/";
  url += + idx + ".svg";

  return url;

}



function draw() {

  
  let key = getSelectedKey();
  let formula = getFormula();
  title.html("Chords in the Key of " + key + " " + formula);

  let kNotes = getNotesSerie(key, formula);
  
  notesDisplay.html(kNotes.join(" "));

  let chords = findChords(kNotes);

  let l1="<tr>";
  let l2="<tr>";
  let l3="<tr>";
  let l4="<tr>";
  
  for (i=0; i < chords.length; i++) {
    l1 += "<th>" + chords[i].name + "</th>";
    l2 += "<td>" + chords[i].notes + "</td>";
    l3 += "<td> <img src='" + getChordPictureURL(chords[i].name, 1) + "'></img></td>";
    l4 += "<td> <img src='" + getChordPictureURL(chords[i].name, 2) + "'></img></td>";    
  }
  l1 += "</tr>";
  l2 += "</tr>";
  l3 += "</tr>";
  l4 += "</tr>";
    

  tableDisplay.html("<table class='chords'>" + l1 + l2 + l3 + l4 + "</table>");

  
}
