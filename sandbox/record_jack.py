import sys
import signal
import os
import jack
import threading
import numpy
from scipy.io.wavfile import write

guitar_port=1
amplify=20000
fs = 44100  # Sample rate

argv = iter(sys.argv)
# By default, use script name without extension as client name:
defaultclientname = os.path.splitext(os.path.basename(next(argv)))[0]

clientname = "Tiry Chord Listener"
servername = None

client = jack.Client(clientname, servername=servername)

if client.status.server_started:
    print("JACK server started")
if client.status.name_not_unique:
    print("unique name {0!r} assigned".format(client.name))

event = threading.Event()

guitar_signal=[]
counter=0

def dumpFrames():
    global guitar_signal
    global counter
    print ("concatenate " + str(len(guitar_signal)) + " np arrays")
    capture = numpy.concatenate(guitar_signal)
    #print("size {0}".format(len(capture)))    
    #print("max value {0}".format(numpy.max(numpy.abs(capture))))
    #capture = numpy.int16(capture * amplify)
    #capture = numpy.int16(capture/numpy.max(numpy.abs(capture)) * 32767)
    
    write("output_" + str(counter)+ "_.wav", fs, capture)
    guitar_signal=guitar_signal[100:]
    counter=counter+1

@client.set_process_callback
def process(frames):
    #assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    #print(frames)
    #print(client.inports[0].get_buffer())
    data =  numpy.int16(client.inports[0].get_array() * amplify)
    #print(data.ndim)
    #print(len(data))
    guitar_signal.append(data)
    if (len(guitar_signal)>200):
        dumpFrames()

    #for i, o in zip(client.inports, client.outports):
    #    o.get_buffer()[:] = i.get_buffer()


@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown!")
    print("status:", status)
    print("reason:", reason)
    event.set()


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

    #for src, dest in zip(capture, client.inports):
    client.connect(capture[guitar_port], client.inports[0])

    #playback = client.get_ports(is_physical=True, is_input=True)
    #if not playback:
    #    raise RuntimeError("No physical playback ports")

    #for src, dest in zip(client.outports, playback):
    #    client.connect(src, dest)

    print("Press Ctrl+C to stop")
    try:
        event.wait()
    except KeyboardInterrupt:
        print("\nInterrupted by user")