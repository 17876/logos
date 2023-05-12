# λόγος
ver. 01a

## Short Description
The programm is a tool for translation of a text into tone rows by giving a rule of translation.
It outputs lists of notes and/or Music XML file, which can be read by a notation software. In this project Finale is used.

## Requierments
+ Python3
Download the latest stable version at: https://www.python.org/downloads/

+ Libraries with key signatures for Finale

+ Font "Accidentals.ttf"

## Detailed Description
The programm takes a text file and translates it to a tone row.
The rule for the process of tranlsation should be given in a seprate JSON-File.
In this file the correspondance between the letters of the text and pitches should be established.

### Translation
#### Main algorithm
For every single letter, which schould be translated into a pitch a rule should be given.

A letter is not only connected to a certain pitch, but the resulting pitch changes every single time, the letter appears in the text.

A rule for the letter a could look as follows:

```json lines{
  "a": {
        "main_note": "cis'",
        "pattern": [1, 1, 1, -3],
        "units": "1/8",
        "alternative": "á",
        "modifier": "a"
    }
```

This means, that every time, when the letter "a" occurs in the text, the pitch cis' will be generated.
Additionally this fundamental pitch will be transposed depending on how many times this letter occured so far.
These transpositions happen according to the `pattern`-key of the dictionary.
The pattern key sets the relative transposition in `units`:
1/2 for half tones,
1/4 for quarter tones,
1/8 for eight tones.

In the example above the following pitches will be generated:

1. "a" occurs for the first time
Output: cis'

2. "a" occurs for the second time
Output: cis'+1*(1/8 tone) = cis' + 25ct

3. "a" occurs for the third time
Output: cis'+25ct + 1*(1/8 tone) = cis' + 50ct

4. "a" occurs for the fourth time
Output: cis'+50ct + 1*(1/8 tone) = cis' + 75ct

5. "a" occurs for the fifth time
Output: cis'+75ct - 3*(1/8 tone) = cis'

6. "a" occurs for the 6th time
Output: cis' + 1*(1/8 tone) = cis' + 25ct

So the pattern goes in cycle.

#### Alternatives / Accents
As in the example above it is possible to work with alternatives of letters.
This means that it is possible to give a letter an alternative with accent.
If the alternative occurs in the text the note gets a modifier: the doubled duration or an accent.
For double duration use `dd` for modifier, for accent over the note use `a`.
The alternatives are subjected to the same logic of transposition and from this perspective not considered as
different letters. For the process of the cyclic transposition the letter and its alternative are indistinguishable.

### Example for a JSON-File with translation rules
See rules_example.json:

```json lines {
    {
  "a": {
    "main_note": "cis'",
    "pattern": [1, 1, 1, -3],
    "units": "1/8",
    "alternative": "á",
    "modifier": "a"
  },
  "e": {
    "main_note": "d'",
    "pattern": [1, 1, -2],
    "units": "1/4",
    "alternative": "é",
    "modifier": "dd"
  },
  "ο": {
    "main_note": "h'",
    "pattern": [1, 1, -2],
    "units": "1/4",
    "alternative": "ό",
    "modifier": "dd"
  }
}
```

### Note Syntax
The programm uses following syntax for notes:
`<notename><octave><ct>`

`<notename>`  
c cis d dis e f fis g gis a ais h (german system).  


`<octave>`  
-great+22vb – sub sub contra octave  
-great+15vb – sub contra octave  
-great+8vb  – contra octave  
-great      – great octave  
-small      – small octave  
'          – 1 Line (middle c) octave  
''         – 2 Line octave  
'''        – 3 Line octave  
''''       – 4 Line octave  
''''+8va   – 5 Line octave  
''''+15va  – 6 Line octave  
''''+22va  – 7 Line octave  

`<ct>`  
Additional transpositon in cents.

Examples:  
ais''''+15va  
cis'  
d-great+8vb  
a-small  
dis-great+8vb+25ct  


### The Note Object


