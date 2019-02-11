echo 'Blank lines';
grep -cvP '\S' $CORPUS.conll.*;
echo 'B-NP tokens';
grep -c B-NP $CORPUS.conll.*;
echo 'Lines';
wc -l $CORPUS.conll.*;
