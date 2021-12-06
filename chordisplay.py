import pygame
import pygame.freetype

screenW=340
screenH=800
 
def _displayChord(screen, chordName, chordDef, success):

  c = (255,255,255)

  marginH=20
  marginV=80

  stepV=80
  stepH=60

  c = (255,255,255)
  if success:
    c = (100,255,100)
    

  bigFont.render_to(screen, (100, 620), chordName, c)

  if (chordDef==None):
    return

  for i in range(0,6):
    w=1
    if (i==0):
      w=5
    pygame.draw.line(screen, (255, 255, 255), (marginH,marginV+stepV*i),(screenW-marginH,marginV+stepV*i),w)

  for i in range(0,6):
    pygame.draw.line(screen, (255, 255, 255), (marginH+stepH*i,marginV),(marginH+stepH*i,marginV+marginV+stepV*5),1)
    finger = chordDef[i]
    if finger=='x':
      font.render_to(screen, (marginH+stepH*i-10, marginV/2), "X", (255, 255, 255))      
    elif finger=='0':
      font.render_to(screen, (marginH+stepH*i-10, marginV/2), "0", (255, 255, 255))
    else:
      fret = int(finger)
      pygame.draw.circle(screen, c, (marginH+stepH*i,marginV+stepV*(fret-0.5)), 20) 

  
bigFont = None
font = None

chord_event = pygame.USEREVENT + 1

def displayChord(chordName, chordDef=None, success=False):
  evt = pygame.event.Event(chord_event, {"name": chordName, "finger": chordDef, "success": success})
  pygame.event.post(evt)
  
def main():
  #pygame.init()
  
  pygame.display.init()
  pygame.font.init()
  pygame.freetype.init()

  screen = pygame.display.set_mode((screenW,screenH))
  pygame.display.set_caption("FatFingers Chord trainer")
  clock = pygame.time.Clock()
 
  global font
  global bigFont
  
  font = pygame.freetype.SysFont("Comic Sans MS", 24)
  bigFont = pygame.freetype.SysFont("Comic Sans MS", 48)


  while True:
    # Lock the framerate at 50 FPS
    clock.tick(50)
 
    # Handle events
    for event in pygame.event.get():
 
      if event.type == pygame.QUIT:
        print("quitting!")
        return
      elif event.type == pygame.KEYDOWN  and event.key == 113:
        print("quitting!")
        pygame.display.quit()
        pygame.quit()
        return
      elif event.type==chord_event:    
        print("Chord event")
        print(event.name) 
        screen.fill((0,0,0))      
        _displayChord(screen, event.name,  event.finger, event.success)
        pygame.display.flip()
 

    
if __name__ == "__main__":
  main()
