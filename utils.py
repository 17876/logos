import re

def note_to_midi(note):
    if note == '0':
        return 0
    note_name_grouped = re.search('cis|c|dis|d|e|fis|f|gis|g|ais|a|h', note)
    note_name = note_name_grouped.group(0)
    striche = note.count('\'')
    klein_gross = 0

    if note_name == 'c':
        base_midi = 60
    if note_name == 'cis':
        base_midi = 61
    if note_name == 'd':
        base_midi = 62
    if note_name == 'dis':
        base_midi = 63
    if note_name == 'e':
        base_midi = 64
    if note_name == 'f':
        base_midi = 65
    if note_name == 'fis':
        base_midi = 66
    if note_name == 'g':
        base_midi = 67
    if note_name == 'gis':
        base_midi = 68
    if note_name == 'a':
        base_midi = 69
    if note_name == 'ais':
        base_midi = 70
    if note_name == 'h':
        base_midi = 71

    if note.find('8va') >= 0:
        transp = 1
    elif note.find('15va') >= 0:
        transp = 2
    elif note.find('22va') >= 0:
        transp = 3
    elif note.find('8vb') >= 0:
        transp = -1
    elif note.find('15vb') >= 0:
        transp = -2
    elif note.find('22vb') >= 0:
        transp = -3
    else:
        transp = 0

    if striche != 0:
        output_midi = base_midi + 12 * (striche - 1 + transp)
    else:
        if note.find('klein') >= 0:
            klein_gross = -1
        elif note.find('gross') >= 0:
            klein_gross = -2
        output_midi = base_midi + 12 * (klein_gross + transp)

    cents = re.search('[+-]\d+(\.\d+)?', note)
    if cents:
        cents_float = float(cents.group())
        micro = round(cents_float/100, 2)
    else:
        micro = 0

    output_midi = output_midi + micro

    if striche == 0 and transp == 0 and klein_gross == 0:
        int('h')  # simulates an error: exception if the input note is in a wrong format
    else:
        return output_midi


def midi_to_note(midi_):
    if midi_ == 0:
        return '0'
    cents = round((midi_ - int(midi_)) * 100, 1)
    midi_pitch = int(midi_)
    if cents > 50:
        cents = cents - 100
        midi_pitch = midi_pitch + 1
    octave = int(midi_pitch / 12)
    note = midi_pitch % 12

    note_name = ''
    octave_name = ''

    if note == 0:
        note_name = 'c'
    elif note == 1:
        note_name = 'cis'
    elif note == 2:
        note_name = 'd'
    elif note == 3:
        note_name = 'dis'
    elif note == 4:
        note_name = 'e'
    elif note == 5:
        note_name = 'f'
    elif note == 6:
        note_name = 'fis'
    elif note == 7:
        note_name = 'g'
    elif note == 8:
        note_name = 'gis'
    elif note == 9:
        note_name = 'a'
    elif note == 10:
        note_name = 'ais'
    elif note == 11:
        note_name = 'h'

    if octave == 0:
        octave_name = '-gross+22vb'
    elif octave == 1:
        octave_name = '-gross+15vb'
    elif octave == 2:
        octave_name = '-gross+8vb'
    elif octave == 3:
        octave_name = '-gross'
    elif octave == 4:
        octave_name = '-klein'
    elif octave == 5:
        octave_name = '\''
    elif octave == 6:
        octave_name = '\'\''
    elif octave == 7:
        octave_name = '\'\'\''
    elif octave == 8:
        octave_name = '\'\'\'\''
    elif octave == 9:
        octave_name = '\'\'\'\'+8va'
    elif octave == 10:
        octave_name = '\'\'\'\'+15va'
    elif octave == 11:
        octave_name = '\'\'\'\'+22va'
    if cents > 0:
        output = '{:s}{:s}+{:d}ct'.format(note_name, octave_name, round(cents))
    elif cents < 0:
        output = '{:s}{:s}{:d}ct'.format(note_name, octave_name, round(cents))
    else:
        output = '{:s}{:s}'.format(note_name, octave_name)
    return output