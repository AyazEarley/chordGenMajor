import random
import pygame.midi
import time
from mido import Message, MidiFile, MidiTrack

def genChords(length):

    transitionTable = {
        'I' : {"V6": 15, "V64 I6": 5, "V": 10,
            "IV": 20, "IV64 I" : 5, "IV6": 5,
                "ii" : 10, "ii6" : 10,
                "vi" : 10,
                "iii" : 3, "iii64 IV6": 1, "iii64 vi" : 1},
        'I6' : {"V64 I" : 5, "V": 10,
                "IV": 45,
                "ii": 10, "ii6": 25,
                "vii06 I": 5},
        
        'ii' : {"V" : 90, "I6 ii6" : 10},
        'ii6' : {"V" : 90, "I6 ii" : 10},

        'iii': {"IV" : 80, "vi" : 20},

        'IV' : {"I" : 20, "I6" : 20, "V" : 40, "ii" : 15, "ii6" : 5},
        'IV6' : {"I" : 10, "V" : 40, "V6": 30, "ii6" : 15, "ii": 5},

        'V' : {"I" : 80, "I6": 10, "vi" : 10},
        'V6' : {"I" : 100},

        'vi' : {"IV" : 30, "ii" : 50, "I": 5, "V": 15 }
        

    }

    numChords = length
    chords = "I"
    last = chords
    for i in range(numChords + 1):
        previous = chords.split()[-1]
        options = transitionTable[previous]
        next = random.choices(list(options.keys()), weights = list(options.values()))[0]
        chords += " " + next
        last = next

    while(last != 'I'):
        previous = chords.split()[-1]
        options = transitionTable[previous]
        next = random.choices(list(options.keys()), weights = list(options.values()))[0]
        chords += " " + next
        last = next
    return chords




pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(2)
velocity = 127

def playChords(chords):
    midiTable = {
        'I' : [48, 64, 67, 72],
        'I6' : [52, 60, 67, 72],
        'ii' : [50, 62, 65, 69],
        'ii6' : [53, 62, 65, 69],
        'iii' : [52, 60, 67, 71],
        'iii64' : [47, 60, 67, 71],
        'IV' : [53, 65, 69, 72],
        'IV6' : [45, 65, 69, 72],
        'IV64' : [48, 65, 69, 72],
        'V' : [55, 62, 67, 71],
        'V6' : [47, 62, 67, 71],
        'V64' : [50, 62, 67, 71],
        "vi" : [45, 64, 69, 72],
        "vii06" : [50, 62, 65, 71]
    }

    chords = chords.split()
    for chord in chords:
        pitches = midiTable[chord]
        for pitch in pitches:
            player.note_on(pitch, velocity)
        time.sleep(1)
        for pitch in pitches:
            player.note_off(pitch, velocity)



from mido import MidiFile, MidiTrack, Message

def writeMIDI(filename, chords):
    midiTable = {
        'I' : [48, 64, 67, 72],
        'I6' : [52, 60, 67, 72],
        'ii' : [50, 62, 65, 69],
        'ii6' : [53, 62, 65, 69],
        'iii' : [52, 60, 67, 71],
        'iii64' : [47, 60, 67, 71],
        'IV' : [53, 65, 69, 72],
        'IV6' : [45, 65, 69, 72],
        'IV64' : [48, 65, 69, 72],
        'V' : [55, 62, 67, 71],
        'V6' : [47, 62, 67, 71],
        'V64' : [50, 62, 67, 71],
        "vi" : [45, 64, 69, 72],
        "vii06" : [50, 62, 65, 71]
    }

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    duration = 480
    velocity = 100

    chords = chords.split()

    for chord in chords:
        pitches = midiTable[chord]

        for i, pitch in enumerate(pitches):
            track.append(Message('note_on', note=pitch, velocity=velocity, time=0))

        for i, pitch in enumerate(pitches):
            track.append(Message('note_off', note=pitch, velocity=velocity, time=duration if i == 0 else 0))

    mid.save(filename) 