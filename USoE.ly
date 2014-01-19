\version "2.16.2"

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
                   (lowtom        default #f         -1)))

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

\header {
    title = "United States of Eurasia"
    composer = "Muse"
}
up = \drummode { r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>2 <cymr sn>4 r4 <cymr sn>4 <cymc>8 <tomh>16 <tomh>32 <tomh>32 <toml>16 <toml>16 <toml>8 <cymc>4 r8 \flam <sn>8 r16 <tomh toml>16 <tomh toml>8 \flam <sn>8 <tomh toml>8 <cymc>8 <hh>8 <hh>8 <tomh toml>16 <tomh toml>16 <tomh toml>16 <hho sn>8 r16 <tomh toml>8 \flam <sn>8 <cymc>8 <hh>8 <hh>8 <hho sn>8 r16 <tommh>32 <tommh>32 <tommh>16 <tomh>32 <tomh>32 <tomh>32 <tomh>32 <toml>32 <toml>32 <toml>32 <toml>32 <toml>32 <toml>32 <cymc>8 <hh>8 <hh>8 <hho sn>8 \flam <sn>8 <tomh toml>8 r16 <tomh toml>8 r16 <cymc>8 <hh>8 <hh>8 \flam <toml>8 \flam <sn>8 \flam <tommh>8 \flam <tomh>8 \flam <toml>8 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 <cymc sn>8 \flam <sn>8 <cymc>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hh>16 <sn>16 <hh>8 <sn>32 <sn>32 <tomh>16 <toml>16 <toml>16 <cymc>8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <sn>8 <cymr>8 r8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <sn>8 <cymr>8 r8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <sn>8 <cymr>8 r8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <tomh>8 <sn>32 <sn>32 <toml>16 <cymc>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>8 <sn>16 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>8 <hh>8 <hh sn>16 <hh>16 <hh>16 <hh>16 <hho>16 <sn>16 <hh>8 <sn>32 <sn>32 <tomh>16 <toml>16 <toml>16 <cymc>8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <sn>8 <cymr>8 r8 <cymr>8 <sn>8 <cymr>8 r16 <sn>16 <cymr>8 <sn>8 <cymr>8 r8 <cymr>8 <sn>8 <cymr>8 <cymc>8 <tommh>32 <tommh>32 <tommh>32 <tommh>32 <tomh>32 <tomh>32 <tomh>32 <tomh>32 <toml>8 <cymc>8 <cymr>8 <cymr>8 \flam <sn>8 r16 <tomh toml>16 <tomh toml>8 \flam <sn>8 <tomh toml>8 <cymc>8 <hh>8 <hh>8 <tomh toml>16 <tomh toml>16 <tomh toml>16 <hho sn>8 r16 <tomh toml>8 \flam <sn>8 <cymc>8 <hh>8 <hh>8 <hho sn>8 r16 <tommh>32 <tommh>32 <tommh>16 <tomh>32 <tomh>32 <tomh>32 <tomh>32 <toml>32 <toml>32 <toml>32 <toml>32 <toml>32 <toml>32 <cymc>8 <hh>8 <hh>8 <sn cymc>8 <sn cymc>16 <toml>16 <toml>16 <toml>16 <toml>8 \flam <sn>8 <cymc>8 <hh>8 <hh>8 \flam <toml>8 \flam <sn>8 \flam <tommh>8 \flam <tomh>8 \flam <toml>8 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <toml>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>4 <cymc>8 <toml>8 \flam <sn>8 <tommh>16 <tommh>16 <tomh>16 <tomh>16 <toml>16 <toml>16 \flam <sn>8 \flam <toml>8 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <cymc>8 <toml>16 <toml>16 <cymc sn>4 <toml>16 <toml>16 <toml>16 <toml>16 <cymc sn>4 <toml>16 <toml>16 <toml>16 <toml>16 <cymc sn>4 <toml>16 <toml>16 <toml>16 <toml>16 <cymc sn>4 <toml>16 <toml>16 <toml>16 <toml>16 \flam <sn>8 \flam <toml>8 <cymc>1 }
down = \drummode { r1 r1 r1 r1 r1 r1 r2 <bd>2 <bd>4 r8 r16 <bd>16 <bd>8 r16 <bd>8 <bd>8 <bd>16 <bd>2 r8 <bd>16 <bd>8 <bd>8 <bd>16 <bd>4 r8 r16 <bd>16 <bd>2 <bd>4 r8 r16 <bd>8 <bd>8 <bd>16 <bd>8 <bd>16 <bd>16 <bd>4 r8 r16 <bd>8 <bd>8 <bd>8 <bd>8 <bd>16 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>8 r16 <bd>8 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>8 r16 <bd>4 r16 <bd>2 <bd>4 r8 r16 <bd>16 <bd>8 r16 <bd>8 <bd>8 <bd>16 <bd>2 r8 <bd>16 <bd>8 <bd>8 <bd>16 <bd>4 r8 r16 <bd>16 <bd>2 <bd>2 r4 r16 <bd>8 r16 <bd>4 r8 r16 <bd>8 <bd>8 <bd>8 <bd>8 <bd>16 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>4 r8 <bd>8 <bd>4 <bd>8 <bd>8 <bd>8 r16 <bd>8 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>8 <bd>16 <bd>4 r16 <bd>16 <bd>16 <bd>16 <bd>4 r16 <bd>16 <bd>16 <bd>16 <bd>4 r16 <bd>16 <bd>16 <bd>16 <bd>4 r16 <bd>16 <bd>16 <bd>16 <bd>8 <bd>8 <bd>16 <bd>1 }
\new DrumStaff <<
    \set DrumStaff.drumStyleTable = #(alist->hash-table mydrums)
    \new DrumVoice {\voiceOne \up}
    \new DrumVoice {\voiceTwo \down}
>>