# Tabpole

Tabpole is a python script that converts drum tabs, like the one that can be found in the ``USoE.tab`` file, and turns them into a [Lilypond](http://www.lilypond.org/) file. Tabpole gets its name from the humble [tadpole](https://www.google.co.uk/search?q=tadpole) which often live in ponds.

## Usage

```
tabpole.py [options] FILE

Options:
    -h --help  show help
    -o OUTPUT  the file to write the lilypond document to. Defaults to FILE.ly
    -c CONFIG  the config file to use, if there isn't one it uses default settings
    -t TITLE   the title
    -a ARTIST  the artist
```

You can then run `lilypond --pdf FILE.ly` to generate a PDF file of the tab

## Config
Tabpole can be configured by passing the script a config file with the `-c` flag. The config should be a json file with the following attributes:

 * flam   - the character used to show a flam (default `f`)
 * double - the character used to show two hits, twice the speed of the bar (default `d`)
 * open   - the character used to show an open hi-hat (default `O`)
 * drums  - a dictionary mapping drum names in the tab file to Lilypond voices.

For example to render this tab properly:

````
Muse - United States of Eurasia

Key
C:Crash 1     o:Drum Hit                   w:Washy Hi-Hats
R:Ride        f:Flam/Hi-Hat With Foot      t:Triplet
H:Hi-Hat      x:Hi-Hat Hit/Drum Rim        g:Ghost Note
S:Snare Drum  X:Cymbal Hit/Hi-Hat Accent   #:Cymbal Choke
T:Medium Tom  d:Double Hit                 r:One-Handed Roll
F:Floor Tom   b:Cymabal Bell
B:Bass Drum   O:Drum Accent/Open Hi-Hat

Intro

(rest 8 bars)

Verse

(rest 8 bars)

R|----X-------X---|----X-------X---|----X-------X---|----X-------X---|
S|----x-------x---|----x-------x---|----x-------x---|----x-------x---|

C|----------------|----------------|--------X-------|X---------------|
R|----X-------X---|----X-------X---|----X-----------|----------------|
S|----x-------x---|----x-------x---|----x-----------|------f-----f---|
T|----------------|----------------|----------od----|---------oo---o-|
F|----------------|----------------|------------ooo-|---------oo---o-|
B|----------------|----------------|--------o-------|o------oo--o-o-o|
````

The configuration file would look like:
````json
{
 "drums": {"R": "cymr",
           "S": "sn",
           "C": "cymc",
           "T": "tomh",
           "F": "toml",
           "B": "bd",
           "H": "hh"
          },
 "flam": "f",
 "open": "O",
 "double": "d"
}
````

There are a list of Lilypad drums, which are the values in the drums dictionary, [here](http://lilypond.org/doc/v2.16/Documentation/notation/common-notation-for-percussion#percussion-staves)
