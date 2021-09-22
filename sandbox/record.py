import sounddevice as sd
import sys, getopt
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 1  # Duration of recording
sd.default.channels = 0, 2
sd.default.device=None,18

def main(argv):
    print("Start")

    device_info = sd.query_devices(sd.default.device, 'output')
    print(device_info)

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, blocking=False)

    print("Wait")
    sd.wait()  # Wait until recording is finished
    print("Save")

    write('output.wav', fs, myrecording)  # Save as WAV file 


if __name__ == "__main__":
   main(sys.argv[1:])

