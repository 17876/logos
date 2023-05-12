from utils import note_to_midi, midi_to_note

# class for note
class Note:
    def __init__(self, init_value, duration=None, articulation=None, comment=None):
        if type(init_value) == str: # we have a note
            self.note = init_value
            self.midi = note_to_midi(init_value)
        else:
            self.midi = init_value # we have midi
            self.note = midi_to_note(init_value)

        if duration:
            self.duration = duration
        else:
            self.duration = 'None'

        if articulation:
            self.articulation = articulation
        else:
            self.articulation = 'None'

        if comment:
            self.comment = comment
        else:
            self.comment = 'None'

    def __str__(self):
        line = 'Note: {:s}, MIDI: {:.02f}, Duration: {:s}, Articulation: {:s}, Comment: {:s}'.format(self.note, self.midi, self.duration,
                                                                                                     self.articulation, self.comment)
        return line

def note_obj_to_dict(note_obj):
    output = {}
    output['note'] = note_obj.note
    output['midi'] = note_obj.midi
    output['duration'] = note_obj.duration
    output['articulation'] = note_obj.articulation
    output['comment'] = note_obj.comment
    return output

def dict_to_note_obj(dct):
    note = dct['note']
    midi = dct['midi']
    duration = dct['duration']
    articulation = dct['articulation']
    comment = dct['comment']
    return Note(midi, duration, articulation, comment)
