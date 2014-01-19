import re
from itertools import takewhile
from data import regex, music_text, flam_func, usage, layout_text, header_text, version_text
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

def get_drum_name(text):
    return text.strip().split('|')[0]

def is_empty(notes):
    return all(note == '-' for note in notes)

def is_bar(notes):
    return all(note == '|' for note in notes)

def get_all_drums(self, lines):
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

def parse_lines(text):
    '''Remove anything which is not notes and group lines together'''
    # remove any spaces on the left
    text = '\n'.join([line.lstrip() for line in text.split('\n')])
    parsed = re.findall(regex, text, re.VERBOSE)
    # remove the last element of the split as it should be an empty line
    lines = []
    for line in parsed:
        lines.append(bar for bar in line[0].split('\n') if bar != '')
    return lines

class TabToSheetMusic:
    def __init__(self, lilypond_drums, flam_note, double_note, open_note):
        self.lilypond_drums = lilypond_drums
        self.flam_note = flam_note
        self.open_note = open_note
        self.double_note = double_note

    def generate_lilypond(self, text, title='', artist=''):
        # remove carriage returns
        text = text.replace('\r', '')
        lines = parse_lines(text)
        up_music = []
        down_music = []
        for line in lines:
            up = {}
            down = {}
            for drum in line:
                drum_name = get_drum_name(drum)
                music = '|'.join(drum.split('|')[1:])
                if self.lilypond_drums[drum_name] in up_drums:
                    up[drum_name] = music
                elif self.lilypond_drums[drum_name] in down_drums:
                    down[drum_name] = music
            up_music_line, ubars = self.create_music(up)
            down_music_line, dbars = self.create_music(down)
            # if there are no bars we want to rest for each bar
            if ubars == 0:
                up_music_line = ['r1'] * dbars 
            elif dbars == 0:
                down_music_line = ['r1'] * ubars
            up_music.extend(up_music_line)
            down_music.extend(down_music_line)
        music = music_text.format(' '.join(up_music), ' '.join(down_music))
        header = ''
        if title != '' or artist != '':
            header = header_text.format(title, artist)
        return '\n'.join([version_text, layout_text, flam_func, header, music])


    def create_music(self, notes):
        lilypond = []
        keys = list(notes.keys())
        # a list of tuples with notes. For this example:
        #    B|x--
        #    S|--x
        # the result would be [('x','-'), ('-','-'), ('-', 'x')]
        music = list(zip(*notes.values()))
        bar_length = len(list(takewhile(lambda x: not is_bar(x), music)))
        i = 0
        bars = 0
        while i < len(music):
            note = music[i]
            if is_empty(note):
                empties = len(list(takewhile(is_empty, music[i:])))
                lengths = get_note_lengths(empties, bar_length)
                lilypond.extend(['r' + str(length) for length in lengths])
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
                    drum = self.lilypond_drums[keys[j]]
                    if note != '-':
                        drums_hit.append(drum)
                    if note == self.double_note:
                        double = True
                    if note == self.open_note and drum == 'hh':
                        hhopen = True
                    if note == self.flam_note:
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
                lilypond.extend('r' + str(length) for length in lengths[1:])
                i += empties
        return lilypond, bars

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
    title = artist = ''
    if args['-t'] is not None:
        title = args['-t']
    if args['-a'] is not None:
        artist = args['-a']
    tab = args['FILE']
    if not os.path.exists(tab):
        print('Tab file {0} does not exist'.format(tab))
        sys.exit()
    output = os.path.splitext(os.path.basename(tab))[0] + '.ly'
    if args['-o'] is not None:
        output = args['-o'] 
    data = open(tab, 'r').read()
    
    ly = TabToSheetMusic(lilypond_drums, flam_note, double_note, open_note).generate_lilypond(data, title, artist)
    with open(output, 'w') as f:
        f.write(ly)
