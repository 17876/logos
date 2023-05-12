import unittest
from note import Note


class TestNote(unittest.TestCase):
    def test_init_with_midi_01(self):
        note = Note(61.25)
        result = note.midi
        expected = 61.25
        self.assertEqual(result, expected)

    def test_init_with_midi_02(self):
        note = Note(61.25)
        result = note.note
        expected = 'cis\'+25ct'
        self.assertEqual(result, expected)

    def test_init_with_note_01(self):
        note = Note('cis\'+25ct')
        result = note.note
        expected = 'cis\'+25ct'
        self.assertEqual(result, expected)

    def test_init_with_note_02(self):
        note = Note('cis\'+25ct')
        result = note.midi
        expected = 61.25
        self.assertEqual(result, expected)

    def test_print(self):
        note = Note('cis\'+25ct')
        print(note)


if __name__ == '__main__':
    unittest.main()