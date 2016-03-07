#!/bin/bash

unicharset_extractor *.box


mftraining -F font_properties -U unicharset -O eng.unicharset *.tr

cntraining *.tr

mv shapetable eng.ryan.exp2a.shapetable

mv normproto eng.ryan.exp2a.normproto

mv inttemp eng.ryan.exp2a.inttemp

mv pffmtable eng.ryan.exp2a.pffmtable

mv eng.unicharset eng.ryan.exp2a.unicharset

combine_tessdata eng.ryan.exp2a.

cp eng.ryan.exp2a.traineddata /usr/local/share/tessdata
