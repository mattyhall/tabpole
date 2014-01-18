import re
from itertools import takewhile
from data import regex, music_text, flam_func, usage
import json
from docopt import docopt
import os.path
import sys

# These are set later, not constant
up_drums = ['cymr', 'sn', 'cymc', 'tomh', 'tommh', 'toml', 'hh', 'hho', 'hhho', 'ss', 'tomfl', 'tomfh', 'tomml', 'ss', 'hc']
down_drums = ['bd', 'hhp']

lilypond_drums = {'R': 'cymr', 'S': 'sn', 'C': 'cymc', 'T': 'tomh', 't': 'tommh', 'F': 'toml', 'B': 'bd', 'H': 'hh'}

flam_note = 'f'
open_note = 'O'
double_note = 'd'

def parse_lines(text):
    '''Remove anything which is not notes and group lines together'''
    parsed = re.findall(regex, text, re.VERBOSE)
    # remove the last element of the split as it should be an empty line
    # TODO: Filter out empty strings
    return [line[0].split('\n')[:-1] for line in parsed]

def get_drum_name(text):
    return text.split('|')[0].replace(' ', '')

def is_empty(notes):
    return all(map(lambda x: x == '-', notes))

def is_bar(notes):
    return all(map(lambda x: x == '|', notes))

def get_all_drums(lines):
    drums = set()
    for line in lines:
        for drum in line:
            drums.add(get_drum_name(drum))
    return drums

def get_note_lengths(empties, bar_length):
    note_lengths = [64, 32, 16, 8, 4, 2, 1]
    if empties in note_lengths:
        return [int(bar_length / empties)]
    lengths = []
    while True:
        if empties == 0:
            return lengths
        if empties / note_lengths[0] >= 1:
            empties -= note_lengths[0]
            # divide the bar_length by the note_length. eg 4 notes in a bar of 16 will become a quarter note (4)
            lengths.append(int(bar_length / note_lengths[0]))
        else:
            note_lengths = note_lengths[1:]

def create_music(notes, bar_length):
    lilypond = []
    keys = list(notes.keys())
    # a list of tuples with notes. For this example:
    #    B|x--
    #    S|--x
    # the result would be [('x','-'), ('-','-'), ('-', 'x')]
    music = list(zip(*notes.values()))
    i = 0
    bars = 0
    while i < len(music):
        note = music[i]
        if is_empty(note):
            empties = len(list(takewhile(is_empty, music[i:])))
            lengths = get_note_lengths(empties, bar_length)
            lilypond.extend(map(lambda x: 'r' + str(x), lengths))
            i += empties
        elif is_bar(note):
            i += 1
            bars += 1
        else:
            drums_hit = []
            double = False
            hhopen = False
            flam = False
            for j, note in enumerate(note):
                drum = lilypond_drums[keys[j]]
                if note != '-':
                    drums_hit.append(drum)
                if note == double_note:
                    double = True
                if note == open_note and drum == 'hh':
                    hhopen = True
                if note == flam_note:
                    flam = True
            empties = len(list(takewhile(is_empty, music[i+1:]))) + 1
            lengths = get_note_lengths(empties, bar_length)
            drums = []
            for drum in drums_hit:
                if drum == 'hh' and hhopen:
                    drums.append('hho')
                else:
                    drums.append(drum)
            # Two hits
            if double:
                length = lengths[0] * 2
                lilypond.append('<' + ' '.join(drums) + '>' + str(length))
                lilypond.append('<' + ' '.join(drums) + '>' + str(length))
            elif flam:
                lilypond.append('\\flam <' + ' '.join(drums) + '>' + str(lengths[0]))
            else:
                lilypond.append('<' + ' '.join([drum for drum in drums]) + '>' + str(lengths[0]))
            lilypond.extend(['r' + str(x) for x in lengths[1:]])
            i += empties
    return lilypond, bars

def main(lines):
    up_music = []
    down_music = []
    bar_length = 16
    for line in lines:
        up = {}
        down = {}
        for drum in line:
            drum_name = get_drum_name(drum)
            music = '|'.join(drum.split('|')[1:])
            if lilypond_drums[drum_name] in up_drums:
                up[drum_name] = music
            elif lilypond_drums[drum_name] in down_drums:
                down[drum_name] = music
        up_music_line, ubars = create_music(up, bar_length)
        down_music_line, dbars = create_music(down, bar_length)
        # if there are no bars we want to rest for each bar
        if ubars == 0:
            up_music_line = ['r1'] * dbars 
        elif dbars == 0:
            down_music_line = ['r1'] * ubars
        up_music.extend(up_music_line)
        down_music.extend(down_music_line)
    music = music_text.format(' '.join(up_music), ' '.join(down_music))
    return '\n'.join([flam_func, music])


if __name__ == '__main__':
    args = docopt(usage)
    if args['-c'] is not None:
        f = args['-c']
        if not os.path.exists(f):
            print('Config file {0} does not exist'.format(f))
            sys.exit()
        config = json.loads(open(f, 'r').read())
        try:
            lilypond_drums = config['drums']
            flam_note = config['flam']
            double_note = config['double']
            open_note = config['open']
        except IndexError:
            print('Config files must have values for "flam", "double", "open" and "drums"')
            sys.exit()
    tab = args['FILE']
    if not os.path.exists(tab):
        print('Tab file {0} does not exist'.format(tab))
        sys.exit()
    output = os.path.splitext(os.path.basename(tab))[0] + '.ly'
    if args['-o'] is not None:
        output = args['-o'] 
    data = open(tab, 'r').read()
    ly = main(parse_lines(data))
    with open(output, 'w') as f:
        f.write(ly)
