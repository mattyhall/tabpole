usage = '''Tab to sheet music.

Usage: tabpole.py [options] FILE

Options
    -h --help show this
    -o OUTPUT the file to write the lilypond document to. Defaults FILE.ly
    -c CONFIG the config file to use, if there isn't one use defaults
    -t TITLE  the title of the piece to be displayed in a header
    -a ARTIST the artist of the piece to be displayed in a header
'''

regex = r'''((
               \w+ # any number of alphanumerics for the drum name
               \s* # whitespacec
               \|  # bar to seperate drum name from music
               .+? # any character, with '?' for none greedy
               \n) # a whitespace at the end of a drum line
              +    # many drum lines 
              \n)  # a trailing newline'''

version_text = '\\version "2.16.2"'

layout_text = '''
#(define mydrums '(
                   (bassdrum      default #f         -3)
                   (snare         default #f          1)
                   (hihat         cross   #f          5)
                   (halfopenhihat cross   "halfopen"  5)
                   (pedalhihat    cross   #f         -5)
                   (openhihat     cross   "open"      5)
                   (ridecymbal    cross   #f          4)
                   (crashcymbal   xcircle #f          5)
                   (hightom       default #f          3)
                   (himidtom      default #f          2)
                   (lowtom        default #f         -1)))'''

header_text = '''\header {{
    title = "{0}"
    composer = "{1}"
}}'''

music_text = '''up = \\drummode {{ {0} }}
down = \\drummode {{ {1} }}
\\new DrumStaff <<
    \\set DrumStaff.drumStyleTable = #(alist->hash-table mydrums)
    \\new DrumVoice {{\\voiceOne \\up}}
    \\new DrumVoice {{\\voiceTwo \\down}}
>>'''

flam_func = '''
#(define (add-grace-property context-name grob sym val)
   (define (set-prop context)
    (let* ((current (ly:context-property context 'graceSettings))
            (new-settings (append current 
                                  (list (list context-name grob sym val)))))
      (ly:context-set-property! context 'graceSettings new-settings)))
      
  (make-apply-context set-prop))

#(define (grace-from-main-note print-chord? lngth music)
  (let* ((elts (ly:music-property music 'elements))
         (has-duration? 
           (lambda (x) (ly:duration? (ly:music-property x 'duration))))
         (mus (cond ((and (music-is-of-type? music 'event-chord) print-chord?)
                     (make-event-chord (event-chord-notes music)))
                    ((music-is-of-type? music 'event-chord)
                     (first (event-chord-notes music)))
                    (else music)))
         (note (map-some-music
                  (lambda (m)
                    (and (has-duration? m)
                         (begin
                           (set! (ly:music-property m 'duration)
                                 (ly:make-duration (if (> lngth 1) 4 3) 0 1 1))
                           (set! (ly:music-property m 'articulations) '())
                           m)))
                  (ly:music-deep-copy mus)))
         (next-note (ly:music-deep-copy note))
         (last-note (ly:music-deep-copy note))
         (m-list 
           (flatten-list 
             (list note 
                   (make-list (max 0 (- lngth 2)) next-note) 
                   last-note))))
  (cond ((= lngth 1 )
           note)
        ((> lngth 1)
           (list-set!  m-list 0
             (begin
                (ly:music-set-property! 
                    note 
                    'articulations
                    (list (make-music
                           'BeamEvent
                           'span-direction -1)))
                 note))          
           (list-set!  m-list (- lngth 1)
             (begin
                (ly:music-set-property! 
                    last-note 
                    'articulations
                    (list (make-music
                           'BeamEvent
                           'span-direction 1)))
                last-note))
            (make-sequential-music m-list))
         (else (make-sequential-music '())))))
graceRepeat =
#(define-music-function (parser location chord-repeat? how-much note) 
  ((boolean? #f) integer? ly:music?)
  #{ 
    \slashedGrace {  $(grace-from-main-note chord-repeat? how-much note) }
    $note 
  #})
flam = 
#(define-music-function (parser location music)(ly:music?)
  #{ \graceRepeat #1 $music #})
drag =
#(define-music-function (parser location music)(ly:music?)
  #{ \graceRepeat 2 $music #})
ruff =
#(define-music-function (parser location music)(ly:music?)
  #{ \graceRepeat #3 $music #})
'''
