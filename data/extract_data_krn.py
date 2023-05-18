from fnmatch import fnmatch
import music21  # the modified version from our fork of the music21 library: https://github.com/Music-Miners/music21
import verovio
import os
import pickle
import time
import numpy as np

logs_path = None
data = []

def convert_krn_to_mei(path) -> str:
    toolkit = verovio.toolkit()
    try:
        toolkit.loadFile(path)
        mei = toolkit.getMEI()
    except:
        write_log("\tCannot convert the .krn to the .mei file. Wrong syntax.\n")
    return mei


def convert_mei_to_music_objects(mei) -> music21.stream.Score:
    piece = None
    try:
        conv = music21.mei.MeiToM21Converter(mei)
        piece = conv.run()
        piece = transpose_to_C(piece)
    except:
        write_log("\tCannot convert the mei data to the music objects representation.\n")
    return piece

def transpose_to_C(piece):
    key = piece.analyze('key')
    i = music21.interval.Interval(key.tonic, music21.pitch.Pitch('C'))
    return piece.transpose(i)

def get_3d_representation_of_the_piece(piece):
    entity = None
    try:
        notes = []
        durations = []
        phrases = []
        for element in piece.flat:
            if isinstance(element, music21.note.Note) or isinstance(element, music21.note.Rest): 
                if element.isRest:
                    notes.append(128)
                else:
                    notes.append(element.pitch.midi)
                durations.append(element.duration.quarterLength)
                phrases.append(element.phraseStop)
        entity = [notes,durations,phrases]
        if 1 not in set(phrases):
            msg = "\tThe .krn file has no phrases.\n"
            write_log(msg)
            raise Exception(msg)
    except:
        write_log("\tCannot convert the muse data to the 3d vector representation.\n")
    return entity
    

def write_log(msg):
    global logs_path
    print(msg)
    f = open(logs_path, "a")
    f.write(msg)
    f.close()


def main():
    global logs_path
    epoch = int(time.time())
    logs_path = os.path.join(os.getcwd(),"logs_lorraine.txt".format(epoch))
    data_path = os.path.join(os.getcwd(),"data_lorraine.pkl".format(epoch))

    root = None
    root = input("Enter the name of the root directory.\n-->")
    while(True):
        if not os.path.exists(root):
            root = input("The entered path does not exist. Please try again.\n-->")
            print(root)
        else:
            break

    pattern = "*.krn"

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                write_log("\n{}\n".format(os.path.join(path, name)))
                mei = convert_krn_to_mei(os.path.join(path, name))
                if mei is None:
                    write_log("FAILED\n")
                    continue
                piece = convert_mei_to_music_objects(mei)
                if piece is None:
                    write_log("FAILED\n")
                    continue
                entity = get_3d_representation_of_the_piece(piece)
                if entity is None:
                    write_log("FAILED\n")
                    continue
                data.append(entity)
                write_log("SUCCEEDED\n")

    with open(data_path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


main()