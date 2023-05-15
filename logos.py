import json
import linecache
import os
import os.path
import re
import sys
from note import Note
from note import note_obj_to_dict, dict_to_note_obj

# prints an exception
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    line_no = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_no, f.f_globals)
    print('Exception in ({}, line {}): {}'.format(filename, line_no, exc_obj))

# generates the music xml parameter for durations
def get_xml_durations(n_of_notes_per_system, durations):
    n_of_beats_im_takt = 0
    beat_type = 0
    xml_note_duration = 0
    divisions = 0
    xml_note_type = ''
    dot = False

    if durations == '2':  # half
        n_of_beats_im_takt = n_of_notes_per_system
        beat_type = 2
        xml_note_duration = 4
        divisions = 2
        xml_note_type = 'half'
        dot = False
    elif durations == 'p4':  # dotted quarter
        n_of_beats_im_takt = n_of_notes_per_system * 3
        beat_type = 8
        divisions = 2
        xml_note_duration = 3
        xml_note_type = 'quarter'
        dot = True
    elif durations == '4':
        n_of_beats_im_takt = n_of_notes_per_system
        beat_type = 4
        divisions = 2
        xml_note_duration = 2
        xml_note_type = 'quarter'
        dot = False
    elif durations == 'p8':
        n_of_beats_im_takt = n_of_notes_per_system * 3
        beat_type = 16
        divisions = 4
        xml_note_duration = 3
        xml_note_type = 'eighth'
        dot = True
    elif durations == '8':
        n_of_beats_im_takt = n_of_notes_per_system
        beat_type = 8
        divisions = 2
        xml_note_duration = 1
        xml_note_type = 'eighth'
        dot = False
    elif durations == 'p16':
        n_of_beats_im_takt = n_of_notes_per_system * 3
        beat_type = 32
        divisions = 8
        xml_note_duration = 3
        xml_note_type = '16th'
        dot = True
    elif durations == '16':
        n_of_beats_im_takt = n_of_notes_per_system
        beat_type = 16
        divisions = 4
        xml_note_duration = 1
        xml_note_type = '16th'
        dot = False
    elif durations == '32':
        n_of_beats_im_takt = n_of_notes_per_system
        beat_type = 32
        divisions = 8
        xml_note_duration = 1
        xml_note_type = '32nd'
        dot = False
    return [n_of_beats_im_takt, beat_type, divisions, xml_note_duration, xml_note_type, dot]



# saves lists with midi pitches as a music-xml file
def midi_pitches_to_musicxml(output_filename, output_filename_playback, n_of_notes_per_system, durations, note_obj_lists, prec):

    global_xml_durations = get_xml_durations(n_of_notes_per_system, durations)

    gl_n_of_beats_im_takt = global_xml_durations[0]
    gl_beat_type = global_xml_durations[1]
    gl_divisions = global_xml_durations[2]
    gl_xml_note_duration = global_xml_durations[3]
    gl_xml_note_type = global_xml_durations[4]
    gl_dot = global_xml_durations[5]

    # finding the longest list
    all_numbers_of_notes = []
    for i in note_obj_lists:
        all_numbers_of_notes.append(len(i))

    # we take the largest
    number_of_notes = max(all_numbers_of_notes)

    # fill in the parts parts, so they have the same number of notes
    for i in range(len(note_obj_lists)):
        if len(note_obj_lists[i]) < number_of_notes:
            for k in range(number_of_notes - len(note_obj_lists[i])):
                note_obj_lists[i].append((Note(0)))

    output_file = open(output_filename, 'w')
    output_file_playback = open(output_filename_playback, 'w')
    header_file = open('musicxml_header_template.txt', 'r')
    header_lines = header_file.readlines()

    output_file.writelines(header_lines)
    output_file_playback.writelines(header_lines)

    n_of_parts = len(note_obj_lists)

    output_file.write('<part-list>\n')
    output_file.write('    <part-group number="1" type="start">\n')
    output_file.write('      <group-symbol default-x="-5">bracket</group-symbol>\n')
    output_file.write('      <group-barline>yes</group-barline>\n')
    output_file.write('    </part-group>\n')

    output_file_playback.write('<part-list>\n')
    output_file_playback.write('    <part-group number="1" type="start">\n')
    output_file_playback.write('      <group-symbol default-x="-5">bracket</group-symbol>\n')
    output_file_playback.write('      <group-barline>yes</group-barline>\n')
    output_file_playback.write('    </part-group>\n')

    for cur_part_indx in range(n_of_parts):
        output_file.write('    <score-part id="P{:d}">\n'.format(cur_part_indx + 1))
        output_file.write('      <part-name print-object="no">MusicXML Part</part-name>\n')
        output_file.write('      <score-instrument id="P{:d}-I{:d}">\n'.format(cur_part_indx + 1, cur_part_indx + 1))
        output_file.write('        <instrument-name>ARIA Player</instrument-name>\n')
        output_file.write('        <virtual-instrument>\n')
        output_file.write('          <virtual-library>Garritan Instruments for Finale</virtual-library>\n')
        output_file.write('          <virtual-name>005. Keyboards/Steinway Piano</virtual-name>\n')
        output_file.write('        </virtual-instrument>\n')
        output_file.write('      </score-instrument>\n')
        output_file.write('      <midi-device>Bank 1</midi-device>\n')
        output_file.write('      <midi-instrument id="P{:d}-I{:d}">\n'.format(cur_part_indx + 1, cur_part_indx + 1))
        output_file.write('        <midi-channel>1</midi-channel>\n')
        output_file.write('        <midi-program>1</midi-program>\n')
        output_file.write('        <volume>80</volume>\n')
        output_file.write('        <pan>-70</pan>\n')
        output_file.write('      </midi-instrument>\n')
        output_file.write('    </score-part>\n')

        output_file_playback.write('    <score-part id="P{:d}">\n'.format(cur_part_indx + 1))
        output_file_playback.write('      <part-name print-object="no">MusicXML Part</part-name>\n')
        output_file_playback.write('      <score-instrument id="P{:d}-I{:d}">\n'.format(cur_part_indx + 1, cur_part_indx + 1))
        output_file_playback.write('        <instrument-name>ARIA Player</instrument-name>\n')
        output_file_playback.write('        <virtual-instrument>\n')
        output_file_playback.write('          <virtual-library>Garritan Instruments for Finale</virtual-library>\n')
        output_file_playback.write('          <virtual-name>005. Keyboards/Steinway Piano</virtual-name>\n')
        output_file_playback.write('        </virtual-instrument>\n')
        output_file_playback.write('      </score-instrument>\n')
        output_file_playback.write('      <midi-device>Bank 1</midi-device>\n')
        output_file_playback.write('      <midi-instrument id="P{:d}-I{:d}">\n'.format(cur_part_indx + 1, cur_part_indx + 1))
        output_file_playback.write('        <midi-channel>1</midi-channel>\n')
        output_file_playback.write('        <midi-program>1</midi-program>\n')
        output_file_playback.write('        <volume>80</volume>\n')
        output_file_playback.write('        <pan>-70</pan>\n')
        output_file_playback.write('      </midi-instrument>\n')
        output_file_playback.write('    </score-part>\n')

    output_file.write('    <part-group number="1" type="stop"/>\n')
    output_file.write('  </part-list>\n')

    output_file_playback.write('    <part-group number="1" type="stop"/>\n')
    output_file_playback.write('  </part-list>\n')

    for cur_part_indx in range(n_of_parts):
        cur_line = '  <part id="P{:d}">\n'.format(cur_part_indx + 1)
        output_file.write(cur_line)
        output_file_playback.write(cur_line)

        number_of_full_bars = int(number_of_notes / n_of_notes_per_system)  # one bar per system
        number_of_notes_in_the_last_bar = number_of_notes % n_of_notes_per_system  # 0

        note_map = []  # how many note in each bar

        for i in range(number_of_full_bars):
            note_map.append(n_of_notes_per_system)

        if number_of_notes_in_the_last_bar != 0:
            note_map.append(number_of_notes_in_the_last_bar)

        number_of_bars = len(note_map)

        for cur_bar_num in range(number_of_bars):
            output_file.write('	<measure number="{:d}">\n'.format(cur_bar_num + 1))
            output_file.write('	  <print new-system="yes">\n')
            output_file.write('		<system-layout>\n')
            output_file.write('		  <system-distance>80</system-distance>\n')
            output_file.write('		</system-layout>\n')
            output_file.write('	  </print>\n')
            output_file.write('	  <attributes>\n')
            output_file.write('		<divisions>{:d}</divisions>\n'.format(gl_divisions))
            output_file.write('		<key>\n')
            output_file.write('		  <fifths>0</fifths>\n')
            output_file.write('		  <mode>major</mode>\n')
            output_file.write('		</key>\n')
            output_file.write('		<time>\n')
            output_file.write('		  <beats>{:d}</beats>\n'.format(gl_n_of_beats_im_takt))
            output_file.write('		  <beat-type>{:d}</beat-type>\n'.format(gl_beat_type))
            output_file.write('		</time>\n')
            output_file.write('	  </attributes>\n')

            output_file_playback.write('	<measure number="{:d}">\n'.format(cur_bar_num + 1))
            output_file_playback.write('	  <print new-system="yes">\n')
            output_file_playback.write('		<system-layout>\n')
            output_file_playback.write('		  <system-distance>80</system-distance>\n')
            output_file_playback.write('		</system-layout>\n')
            output_file_playback.write('	  </print>\n')
            output_file_playback.write('	  <attributes>\n')
            output_file_playback.write('		<divisions>{:d}</divisions>\n'.format(gl_divisions))
            output_file_playback.write('		<key>\n')
            output_file_playback.write('		  <fifths>0</fifths>\n')
            output_file_playback.write('		  <mode>major</mode>\n')
            output_file_playback.write('		</key>\n')
            output_file_playback.write('		<time>\n')
            output_file_playback.write('		  <beats>{:d}</beats>\n'.format(gl_n_of_beats_im_takt))
            output_file_playback.write('		  <beat-type>{:d}</beat-type>\n'.format(gl_beat_type))
            output_file_playback.write('		</time>\n')
            output_file_playback.write('	  </attributes>\n')

            for cur_pitch_no_in_the_bar in range(note_map[cur_bar_num]):
                # with pitch, duration and articulation
                cur_note_obj = note_obj_lists[cur_part_indx][
                    cur_bar_num * n_of_notes_per_system + cur_pitch_no_in_the_bar]
                cur_duration = cur_note_obj.duration
                cur_articulation = cur_note_obj.articulation
                cur_lyrics = cur_note_obj.comment

                # doubling the duration for this one note
                if cur_duration == 'x2':
                    if durations == '32':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, '16')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                    elif durations == '16':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, '8')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                    elif durations == '8':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, '4')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                    elif durations == '4':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, '2')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                    elif durations == 'p16':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, 'p8')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                    elif durations == 'p8':
                        cur_xml_durations = get_xml_durations(n_of_notes_per_system, 'p4')
                        cur_n_of_beats_im_takt = cur_xml_durations[0]
                        cur_beat_type = cur_xml_durations[1]
                        cur_divisions = cur_xml_durations[2]
                        cur_xml_note_duration = cur_xml_durations[3]
                        cur_xml_note_type = cur_xml_durations[4]
                        cur_dot = cur_xml_durations[5]
                else:
                    cur_n_of_beats_im_takt = gl_n_of_beats_im_takt
                    cur_beat_type = gl_beat_type
                    cur_divisions = gl_divisions
                    cur_xml_note_duration = gl_xml_note_duration
                    cur_xml_note_type = gl_xml_note_type
                    cur_dot = gl_dot

                cur_midi_pitch = cur_note_obj.midi

                # finding out which tuning 1/4-tone, 1/8-tone etc.
                if prec == '1/16':
                    micro_list = [(2 * i) / 16 for i in range(2 + (8 - 1))]  #
                elif prec == '1/8':
                    micro_list = [(2 * i) / 8 for i in range(2 + (4 - 1))]  #
                elif prec == '1/6':
                    micro_list = [(2 * i) / 6 for i in range(2 + (3 - 1))]  #
                elif prec == '1/4':
                    micro_list = [0, 0.5, 1]
                elif prec == '1/3':
                    micro_list = [0, 0.66666667, 1]
                elif prec == '1/2':
                    micro_list = [0, 1]

                difList = []
                for j in micro_list:
                    difList.append(abs(cur_midi_pitch - (int(cur_midi_pitch) + j)))
                _min = min(difList)
                for j in range(len(difList)):
                    if difList[j] == _min:
                        minInd = j

                cur_alteration = minInd
                cur_midi_pitch = int(cur_midi_pitch) + micro_list[minInd]
                cents = abs(int(cur_midi_pitch) - cur_midi_pitch) * 100

                if cents > 50:
                    cents = cents - 100
                    cur_midi_pitch = cur_midi_pitch + 1
                    cur_alteration = cur_alteration - (len(micro_list) - 1)

                cur_alteration_for_playback = 0
                cur_alter_for_playback_expr = '{:d}{:s}'.format(cur_alteration, prec[1:])
                cur_mikro_alteration_for_playback = cur_alteration

                cur_octave = int(cur_midi_pitch / 12) - 1
                note_integer = int(cur_midi_pitch) % 12

                prec_list = prec.split('/')
                prec_float = float(prec_list[0]) / float(prec_list[1])

                if note_integer == 0:
                    note_name = 'C'
                elif note_integer == 1:
                    note_name = 'C'
                    cur_alteration = cur_alteration + 1 * (1 / (prec_float * 2))
                    cur_alteration_for_playback = 1
                elif note_integer == 2:
                    note_name = 'D'
                elif note_integer == 3:
                    note_name = 'D'
                    cur_alteration = cur_alteration + 1 * (1 / (prec_float * 2))
                    cur_alteration_for_playback = 1
                elif note_integer == 4:
                    note_name = 'E'
                elif note_integer == 5:
                    note_name = 'F'
                elif note_integer == 6:
                    note_name = 'F'
                    cur_alteration = cur_alteration + 1 * (1 / (prec_float * 2))
                    cur_alteration_for_playback = 1
                elif note_integer == 7:
                    note_name = 'G'
                elif note_integer == 8:
                    note_name = 'G'
                    cur_alteration = cur_alteration + 1 * (1 / (prec_float * 2))
                    cur_alteration_for_playback = 1
                elif note_integer == 9:
                    note_name = 'A'
                elif note_integer == 10:
                    note_name = 'A'
                    cur_alteration = cur_alteration + 1 * (1 / (prec_float * 2))
                    cur_alteration_for_playback = 1
                elif note_integer == 11:
                    note_name = 'B'

                output_file_playback.write('      <direction placement="below">\n')
                output_file_playback.write('        <direction-type>\n')
                output_file_playback.write('      <words default-y="-115" relative-x="0">{:s}</words>\n'.format(cur_alter_for_playback_expr))
                output_file_playback.write('        </direction-type>\n')
                output_file_playback.write('      </direction>\n')

                if cur_midi_pitch != 0:
                    output_file.write('	  <note>\n')
                    output_file.write('		<pitch>\n')
                    output_file.write('		  <step>{:s}</step>\n'.format(note_name))

                    output_file_playback.write('	  <note>\n')
                    output_file_playback.write('		<pitch>\n')
                    output_file_playback.write('		  <step>{:s}</step>\n'.format(note_name))

                    if cur_alteration:
                        output_file.write('		  <alter>{:d}</alter>\n'.format(int(cur_alteration)))
                        output_file_playback.write(
                            '		  <alter>{:d}</alter>\n'.format(int(cur_alteration_for_playback)))

                    output_file.write('		  <octave>{:d}</octave>\n'.format(cur_octave))
                    output_file.write('		</pitch>\n')
                    output_file.write('		<duration>{:d}</duration>\n'.format(cur_xml_note_duration))
                    output_file.write('		<voice>1</voice>\n')
                    output_file.write('		<type>{:s}</type>\n'.format(cur_xml_note_type))

                    output_file_playback.write('		  <octave>{:d}</octave>\n'.format(cur_octave))
                    output_file_playback.write('		</pitch>\n')
                    output_file_playback.write('		<duration>{:d}</duration>\n'.format(cur_xml_note_duration))
                    output_file_playback.write('		<voice>1</voice>\n')
                    output_file_playback.write('		<type>{:s}</type>\n'.format(cur_xml_note_type))

                    if cur_dot:
                        output_file.write('        <dot/>\n')
                        output_file_playback.write('        <dot/>\n')

                    if cur_alteration > 0:
                        output_file.write('		<accidental>sharp</accidental>\n')
                        output_file_playback.write('		<accidental>sharp</accidental>\n')

                    elif cur_alteration < 0:
                        output_file.write('		<accidental>flat</accidental>\n')
                        output_file_playback.write('		<accidental>flat</accidental>\n')

                    else:
                        output_file.write('		<accidental>natural</accidental>\n')
                        output_file_playback.write('		<accidental>natural</accidental>\n')

                    output_file.write('		<stem>up</stem>\n')

                    if cur_articulation == '>':
                        output_file.write('		<notations>\n')
                        output_file.write('		    <articulations>\n')
                        output_file.write('		        <accent />\n')
                        output_file.write('		    </articulations>\n')
                        output_file.write('		</notations>\n')

                    output_file.write('		<lyric default-y="-90">\n')
                    output_file.write('		    <syllabic>single</syllabic>\n')
                    output_file.write('		    <text>{:s}</text>\n'.format(cur_lyrics))
                    output_file.write('		</lyric>\n')

                    output_file.write('	  </note>\n')

                    # playback file
                    output_file_playback.write('		<stem>up</stem>\n')

                    if cur_articulation == '>':
                        output_file_playback.write('		<notations>\n')
                        output_file_playback.write('		    <articulations>\n')
                        output_file_playback.write('		        <accent />\n')
                        output_file_playback.write('		    </articulations>\n')
                        output_file_playback.write('		</notations>\n')

                    output_file_playback.write('		<lyric default-y="-90">\n')
                    output_file_playback.write('		    <syllabic>single</syllabic>\n')
                    output_file_playback.write('		    <text>{:s}</text>\n'.format(cur_lyrics))
                    output_file_playback.write('		</lyric>\n')

                    output_file_playback.write('	  </note>\n')

                else:
                    output_file.write('	  <note>\n')
                    output_file.write('		<rest/>\n')
                    output_file.write('		<duration>{:d}</duration>\n'.format(cur_xml_note_duration))
                    output_file.write('		<voice>1</voice>\n')
                    output_file.write('		<type>{:s}</type>\n'.format(cur_xml_note_type))

                    output_file_playback.write('	  <note>\n')
                    output_file_playback.write('		<rest/>\n')
                    output_file_playback.write('		<duration>{:d}</duration>\n'.format(cur_xml_note_duration))
                    output_file_playback.write('		<voice>1</voice>\n')
                    output_file_playback.write('		<type>{:s}</type>\n'.format(cur_xml_note_type))

                    if cur_dot:
                        output_file.write('        <dot/>\n')
                        output_file_playback.write('        <dot/>\n')

                    output_file.write('	  </note>\n')
                    output_file_playback.write('	  </note>\n')

            output_file.write('	</measure>\n')
            output_file_playback.write('	</measure>\n')
        output_file.write('  </part>\n')
        output_file_playback.write('  </part>\n')
    output_file.write('</score-partwise>\n')
    output_file_playback.write('</score-partwise>\n')

    output_file.close()
    output_file_playback.close()
    header_file.close()


class Variable(object):
    def __init__(self, value):
        self.value = value

variables = {}

# main menu
def main_menu():
    while True:
        print('\n1:  Text → Notes')  # menu1
        print('2:  Convert a list with Note objects into a Music-XML-File')  # menu2
        print('3:  Print variables')  # menu3
        print('4:  Delete variables')  # menu4
        print('5:  Export variables')  # menu5
        print('6:  Import variables')  # menu6
        print('q:  Quit')
        choice = input(">> ")
        exec_menu(choice)
    return

# execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print('▶▶▶ Error: Invalid choice. Try again.')
    return


# exit program
def quit():
    print('\n')
    print('╔═══════════════════════════════════════════════════════════╗')
    print('║                             Bye!                          ║')
    print('╚═══════════════════════════════════════════════════════════╝')
    sys.exit()


def menu1():
    running1 = True
    running2 = True
    running3 = True

    while True:  # only für back!
        while running1:
            print('')
            print('┌──────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the name of the file with the text. │')
            print('└──────────────────────────────────────────────┘')
            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                return
            elif input_ == 'q':
                exec_menu('q')
            elif input_ == 'm':
                return
            else:
                running1 = True
                running2 = True
                running3 = True

                text_filename = input_
                if os.path.isfile(text_filename):
                    break
                else:
                    print('▶▶▶ Error: The file does not exist. Try again.')

        while running2:
            print('')
            print('┌──────────────────────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the name of the JSON-File with the convertion rule. │')
            print('└──────────────────────────────────────────────────────────────┘')
            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                running3 = False
                running1 = True
                break
            elif input_ == 'q':
                exec_menu('q')
            elif input_ == 'm':
                return
            else:
                running1 = True
                running2 = True
                running3 = True

                rule_filename = input_
                if os.path.isfile(rule_filename):
                    break
                else:
                    print('▶▶▶ Error: The file does not exist. Try again.')

        while running3:
            print('')
            print('┌────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the variable name for the result. │')
            print('└────────────────────────────────────────────┘')
            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                running1 = False
                running2 = True
                break
            elif input_ == 'm':
                return 'main_menu'
            elif input_ == 'q':
                exec_menu('q')
            else:

                running1 = True
                running2 = True
                running3 = True

                var_name = input_
                # checking if we have already var_name_part_NN
                is_there = False
                for i in variables:
                    if i == var_name:
                        is_there = True

                if is_there:
                    while True:
                        print('')
                        print('┌─────────────────────────────────────────────────┐')
                        print('│▶▶▶ The variable already exists. Overwrite? y/n? │')
                        print('└─────────────────────────────────────────────────┘')
                        print('b: Back ║ m: Main Menu ║ q: Quit')
                        input__ = input('>> ')
                        if input__ == 'b':
                            break
                            continue
                        elif input__ == 'm':
                            return 'main_menu'
                        elif input__ == 'q':
                            exec_menu('q')
                        elif input__ == 'y':  # overwrite
                            try:
                                log_filename = '{:s}_log.txt'.format(var_name)
                                result = logos(text_filename, rule_filename, log_filename)
                                variables[var_name] = Variable(result)
                                return 'main_menu'

                            except Exception as ex:
                                print('▶▶▶ Error: Something went wrong.')
                                PrintException()
                                return 'main_menu'

                        elif input__ == 'n':  # do not overwrite
                            break
                            continue

                        else:
                            print('▶▶▶ Error: Invalid choice. Try again.')
                            continue
                else:
                    try:
                        log_filename = '{:s}_log.txt'.format(var_name)
                        result = logos(text_filename, rule_filename, log_filename)
                        variables[var_name] = Variable(result)
                        return 'main_menu'
                    except Exception as ex:
                        print('▶▶▶ Error: Something went wrong.')
                        PrintException()
                        return 'main_menu'

# variables with lists of Note objects -> Music XML
def menu2():
    # 1. variable name for the list -> there / not there?
    # 2. filename for the music xml file -> there / not there -> overwrite?
    running1 = True
    running2 = True
    running3 = True
    while True:
        while running1:
            print('')
            print('┌──────────────────────────────────────────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the variable names for the lists with note objects separated by spaces. │')
            print('│▶▶▶ The lists will be rendered on separate staves in a Music-XML-File.            │')
            print('└──────────────────────────────────────────────────────────────────────────────────┘')
            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                return
            elif input_ == 'm':
                return
            elif input_ == 'q':
                exec_menu('q')
            else:
                running1 = True
                running2 = True
                running3 = True
                try:
                    cur_var_names = input_.split(' ')
                    cur_pitch_lists = []
                    for i in cur_var_names:
                        cur_pitch_lists.append(variables[i].value)
                    break
                except KeyError:
                    print('▶▶▶ Error: The variable does not exist. Try again.')
                    PrintException()

        while running2:
            print('')
            print('┌─────────────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the number of notes per a staff, durations │')
            print('│▶▶▶ and the pitch resolution, separated by spaces    │')
            print('└─────────────────────────────────────────────────────┘')
            print('░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ Syntax ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░')
            print('Duration: ')
            print('2:     for half notes')
            print('p4:    for dotted quarter notes')
            print('4:     for quarter notes')
            print('p8:    for dotted eigth notes')
            print('8:     for eigth notes')
            print('p16:   for dotted 16th')
            print('16:    for 16th')
            print('32:    for 32th\n')

            print('\nPossible pitch resolutions: ')
            print('1/16:  round to 16th tones')
            print('1/8:   round to 8th tones')
            print('1/6:   round to 6th tones')
            print('1/4:   round to quarter tones')
            print('1/3:   round to third tones')
            print('1/2:   round to half tones')

            print('\nFor example:')
            print('10 p4 1/8')
            print('means 10 dotted quarters per staff in the Music-XML-File.')
            print('The pitches will be rounded to 8th-tones.')
            print('░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ Syntax ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░')

            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                running3 = False
                running1 = True
                break
            elif input_ == 'm':
                return
            elif input_ == 'q':
                exec_menu('q')
            else:

                running1 = True
                running2 = True
                running3 = True

                try:
                    input_splitted = input_.split(' ')
                    n_of_notes_per_system = int(input_splitted[0])
                    durations_im_takt = input_splitted[1]
                    prec = input_splitted[2]
                    break
                except TypeError as ex:
                    print('▶▶▶ Error: Something went wrong. Try again.')
                    PrintException()

        while running3:
            print('')
            print('┌───────────────────────────────────────────────────────────────────────────┐')
            print('│▶▶▶ Enter the name for the Music-XML-Files without filename extension      │')
            print('│▶▶▶ The extension will be generated automatically for two Music-XML-Files: │')
            print('│▶▶▶ for playback and notatioin.                                            │')
            print('└───────────────────────────────────────────────────────────────────────────┘')
            print('b: Back ║ m: Main Menu ║ q: Quit')
            input_ = input('>> ')
            if input_ == 'b':
                running1 = False
                running2 = True
                break
            elif input_ == 'm':
                return
            elif input_ == 'q':
                exec_menu('q')
                break
            else:
                running1 = True
                running2 = True
                running3 = True
                notation_filename = input_ + '_notation.xml'
                playback_filename = input_ + '_playback.xml'
                if os.path.isfile(notation_filename) or os.path.isfile(playback_filename):
                    print('')
                    print('┌──────────────────────────────────────────────────┐')
                    print('│▶▶▶ The file(s) already exist(s). Overwrite? y/n? │')
                    print('└──────────────────────────────────────────────────┘')
                    print('b: Back ║ m: Main Menu ║ q: Quit')
                    input__ = input('>> ')
                    if input__ == 'b':
                        continue
                    elif input__ == 'm':
                        return
                    elif input__ == 'q':
                        exec_menu('q')
                    elif input__ == 'y':
                        try:
                            midi_pitches_to_musicxml(notation_filename, playback_filename, n_of_notes_per_system,
                                                     durations_im_takt, cur_pitch_lists, prec)
                            return
                        except Exception as ex:
                            print('▶▶▶ Error: Something went wrong. Try again.')
                            PrintException()
                            return
                    else:
                        continue

                else:
                    try:
                        midi_pitches_to_musicxml(notation_filename, playback_filename, n_of_notes_per_system,
                                                 durations_im_takt, cur_pitch_lists, prec)
                        return
                    except Exception as ex:
                        print('▶▶▶ Error: Something went wrong. Try again.')
                        PrintException()
                        return
    return


# printing out variables
def menu3():
    if variables:
        print('\n▶▶▶ Your variables:\n')
        variables_keys = []
        for i in variables:
            variables_keys.append(i)
        variables_keys.sort()
        for i in variables_keys:
            print('    {:s}'.format(str(i)))
        print('')
        print('┌──────────────────────────────────────────────────────────────────────────┐')
        print('│▶▶▶ Which variables do you want to print out? durch leerzeichen getrennt. │')
        print('│▶▶▶ Separate variables with spaces. Type print_all                        │')
        print('│▶▶▶ to print out all variables.                                           │')
        print('└──────────────────────────────────────────────────────────────────────────┘')
        print('b: Back ║ m: Main Menu ║ q: Quit')
        input_ = input('>> ')
        if input_ == 'b':
            return
        elif input_ == 'm':
            return
        elif input_ == 'q':
            exec_menu('q')
        elif input_ == 'print_all':
            for i in variables_keys:
                print('\nList stored in the variable {:s}:'.format(i))
                print('─────────────────────────────────────')
                for k in variables[i].value:
                    print(k)
        else:
            to_print = [str(i) for i in input_.split(' ')]
            for i in to_print:
                print('\nList stored in the variable {:s}:'.format(i))
                print('─────────────────────────────────────')
                for k in variables[i].value:
                    print(k)

    else:
        print('▶▶▶ Error: There are no variables out there.')
    return

# deleting variables
def menu4():
    print('\n▶▶▶ Your variables:\n')
    variables_keys = []
    for i in variables:
        variables_keys.append(i)
    variables_keys.sort()
    for i in variables_keys:
        print('    {:s}'.format(str(i)))
    print('')
    print('┌──────────────────────────────────────────────────┐')
    print('│▶▶▶ What do you want to delete?                   │')
    print('│▶▶▶ Separate variables with spaces. Print del_all │')
    print('│▶▶▶ to delete all variables.                      │')
    print('└──────────────────────────────────────────────────┘')
    print('b: Back ║ m: Main Menu ║ q: Quit')
    input_ = input('>> ')
    if input_ == 'b':
        return
    elif input_ == 'm':
        return
    elif input_ == 'del_all':
        variables.clear()
    else:
        to_del = [str(i) for i in input_.split(' ')]
        for i in to_del:
            del variables[i]
    return


# export variables as json
def menu5():
    while True:
        print('')
        print('┌──────────────────────────────────────┐')
        print('│▶▶▶ Enter the name for the JSON-File. │')
        print('└──────────────────────────────────────┘')
        print('b: Back ║ m: Main Menu ║ q: Quit')
        input_ = input('>> ')
        if input_ == 'b':
            return
        elif input_ == 'm':
            return
        elif input_ == 'q':
            exec_menu('q')
            break
        else:
            json_filename = input_
            if os.path.isfile(json_filename):
                while True:
                    print('')
                    print('┌─────────────────────────────────────────────┐')
                    print('│▶▶▶ The file already exists. Overwrite? y/n? │')
                    print('└─────────────────────────────────────────────┘')
                    print('b: Back ║ m: Main Menu ║ q: Quit')
                    input__ = input('>> ')
                    if input__ == 'b':
                        break
                        continue
                    elif input__ == 'm':
                        return
                    elif input__ == 'q':
                        exec_menu('q')
                    elif input__ == 'y':
                        try:
                            variables_ = {}
                            for cur_var_name in variables:
                                variables_[cur_var_name] = []  # list of dicts
                                for cur_note_obj in variables[cur_var_name].value:
                                    variables_[cur_var_name].append(note_obj_to_dict(cur_note_obj))
                            json_string = json.dumps(variables_, sort_keys=True, indent=4, separators=(',', ': '))
                            json_file = open(json_filename, 'w')
                            json_file.write(json_string)
                            json_file.close()
                            return
                        except Exception as ex:
                            print('▶▶▶ Error: Something went wrong. Try again.')
                            PrintException()
                            return
                    elif input__ == 'n':
                        break
                        continue
                    else:
                        print('▶▶▶ Error: Invalid choice. Try again.')
                        continue
            else:
                try:
                    # all variables in dict format we collect here
                    variables_ = {}
                    for cur_var_name in variables:
                        variables_[cur_var_name] = [] # list of dicts
                        for cur_note_obj in variables[cur_var_name].value:
                            variables_[cur_var_name].append(note_obj_to_dict(cur_note_obj))
                    json_string = json.dumps(variables_, sort_keys=True, indent=4, separators=(',', ': '))
                    json_file = open(json_filename, 'w')
                    json_file.write(json_string)
                    json_file.close()
                    return
                except Exception as ex:
                    print('variables', variables)
                    print('▶▶▶ Error: Something went wrong. Try again.')
                    PrintException()
                    return
    return

# importing variables from json
def menu6():
    while True:
        print('')
        print('┌──────────────────────────────────────┐')
        print('│▶▶▶ Enter the name for the JSON-File. │')
        print('└──────────────────────────────────────┘')
        print('b: Back ║ m: Main Menu ║ q: Quit')
        input_ = input('>> ')
        if input_ == 'b':
            return
        elif input_ == 'm':
            return
        elif input_ == 'q':
            exec_menu('q')
            break
        else:
            json_filename = input_
            if os.path.isfile(json_filename):
                try:
                    json_file = open(json_filename)
                    json_data = json.load(json_file)
                    for i in json_data:
                        running2 = True
                        running3 = True
                        if i in variables:
                            dash_string = ''
                            space_string = ''
                            for ii in range(len(i)):
                                dash_string = dash_string + '─'
                                space_string = space_string + ' '
                            while running2:
                                running3 = True
                                print('')
                                print('┌─────────────────{:s}─────────────────────────────────┐'.format(dash_string))
                                print('│▶▶▶ The variable {:s} already exists. Overwrite? y/n? │'.format(i))
                                print('│▶▶▶ or save with a new name: N{:s}?                   │'.format(space_string))
                                print('└─────────────────{:s}─────────────────────────────────┘'.format(dash_string))
                                print('m: Main Menu ║ q: Quit')
                                input__ = input('>> ')
                                if input__ == 'y':  # works#
                                    cur_list_of_note_obj = []
                                    for cur_dict in json_data[i]:
                                        cur_list_of_note_obj.append(dict_to_note_obj(cur_dict))
                                    variables[i] = Variable(cur_list_of_note_obj)
                                    break
                                elif input__ == 'n':
                                    break
                                elif input__ == 'N':  # save under a different name
                                    while running3:
                                        print('')
                                        print('┌─────────────────────────────────{:s}─┐'.format(dash_string))
                                        print('│▶▶▶ Enter the new variable name  {:s} │'.format(space_string))
                                        print('│▶▶▶ to import the variable {:s}       │'.format(i))
                                        print('└─────────────────────────────────{:s}─┘'.format(dash_string))
                                        print('b: Back ║ m: Main Menu ║ q: Quit')
                                        input___ = input('>> ')
                                        if input___ == 'b':
                                            running3 = False
                                        elif input___ == 'q':
                                            exec_menu('q')
                                        elif input___ == 'm':
                                            return
                                        else:
                                            var_name = input___
                                            if var_name in variables:
                                                while True:
                                                    print('')
                                                    print('┌────────────────────────────────────────────────┐')
                                                    print('│▶▶▶ The variable already exists. Overwrite? y/n?│')
                                                    print('└────────────────────────────────────────────────┘')
                                                    print('z: zurück ║ h: hauptmenü ║ q: quit')
                                                    input____ = input('>> ')
                                                    if input____ == 'b':
                                                        break
                                                        continue
                                                    elif input____ == 'q':
                                                        exec_menu('q')
                                                    elif input____ == 'm':
                                                        return
                                                    elif input____ == 'y':
                                                        cur_list_of_note_obj = []
                                                        for cur_dict in json_data[i]:
                                                            cur_list_of_note_obj.append(dict_to_note_obj(cur_dict))
                                                        variables[var_name] = Variable(cur_list_of_note_obj)
                                                        running2 = False
                                                        running3 = False
                                                        break
                                                    elif input____ == 'n':
                                                        break
                                                    else:
                                                        print('▶▶▶ Error: Invalid choice. Try again.')
                                                        continue
                                            else:
                                                cur_list_of_note_obj = []
                                                for cur_dict in json_data[i]:
                                                    cur_list_of_note_obj.append(dict_to_note_obj(cur_dict))
                                                variables[var_name] = Variable(cur_list_of_note_obj)
                                                break
                                    else:
                                        continue
                                    break
                                elif input__ == 'm':
                                    return
                                elif input__ == 'q':
                                    exec_menu('q')
                                else:
                                    print('▶▶▶ Error: Invalid choice. Try again.')
                        else:
                            cur_list_of_note_obj = []
                            for cur_dict in json_data[i]:
                                cur_list_of_note_obj.append(dict_to_note_obj(cur_dict))
                            variables[i] = Variable(cur_list_of_note_obj)
                    return
                except Exception as ex:
                    print('▶▶▶ Error: Something went wrong. Try again.')
                    PrintException()
                    return
            else:
                print('▶▶▶ Error: The file already exists. Try again.')


# menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '6': menu6,
    'q': quit
}

# translates a text into a list of Note objects
def logos(text_filename, rule_filename, log_filename):
    log_file = open(log_filename, 'w')
    output = []
    text_file = open(text_filename, 'r')
    text_file_words = text_file.read().split()

    rule_file = open(rule_filename)
    rule_data = json.load(rule_file)

    all_keys = [i for i in rule_data]

    all_keys_counters = {}
    for i in all_keys:
        all_keys_counters[i] = 0

    all_keys_current_pitches = {}
    for i in all_keys:
        all_keys_current_pitches[i] = 0

    for cur_word in text_file_words:
        cur_word_lower = cur_word.lower()
        log_file.write(cur_word_lower + ':\n')
        # finding all letters and also á, é, í, ó, ú ... ά, έ, ί, ύ, ή, ό, ώ, ού
        cur_letters = re.findall(r'(ου|ού|\w)', cur_word_lower)
        print('cur_letters', cur_letters)
        # iterating throughh the letters of a word
        for cur_letter in cur_letters:
            # check if we use alternative letter with accent or no
            alternative_flag = 0

            # substituting the accents with normal ones
            # latin
            if cur_letter == 'á':
                cur_letter_key = 'a'
                alternative_flag = 1
            elif cur_letter == 'é':
                cur_letter_key = 'e'
                alternative_flag = 1

            elif cur_letter == 'í':
                cur_letter_key = 'i'
                alternative_flag = 1

            elif cur_letter == 'ú':
                cur_letter_key = 'u'
                alternative_flag = 1


            # greek
            elif cur_letter == 'ά':
                cur_letter_key = 'α'
                alternative_flag = 1

            elif cur_letter == 'έ':
                cur_letter_key = 'ε'
                alternative_flag = 1

            elif cur_letter == 'ί':
                cur_letter_key = 'ι'
                alternative_flag = 1

            elif cur_letter == 'ύ':
                cur_letter_key = 'υ'
                alternative_flag = 1

            elif cur_letter == 'ή':
                cur_letter_key = 'η'
                alternative_flag = 1

            elif cur_letter == 'ό':
                cur_letter_key = 'ο'
                alternative_flag = 1

            elif cur_letter == 'ώ':
                cur_letter_key = 'ω'
                alternative_flag = 1

            elif cur_letter == 'ού':
                cur_letter_key = 'ου'
                alternative_flag = 1

            else:
                cur_letter_key = cur_letter
                # alternative_flag stays 0, we sonify the non-accent letter

            if cur_letter_key in all_keys:
                print('')
                cur_notenname = rule_data[cur_letter_key]['main_note']
                cur_note_obj_no_transp = Note(cur_notenname)

                cur_modifier = 0

                if ('modifier' in rule_data[cur_letter_key]) and (alternative_flag == 1):
                    cur_modifier = rule_data[cur_letter_key]['modifier']

                duration = 0
                articulation = 0

                if cur_modifier == 'dd': # double duration
                    duration = 'x2' # relative duration, doubling
                elif cur_modifier == 'a': # accent
                    articulation = '>'

                all_keys_counters[cur_letter_key] = all_keys_counters[cur_letter_key] + 1
                cur_key_counter = all_keys_counters[cur_letter_key]

                if cur_key_counter == 1:  # the first time
                    cur_note_obj_transp = cur_note_obj_no_transp
                    cur_muster_indx = -1
                else:
                    cur_muster_indx = (cur_key_counter - 2) % len(rule_data[cur_letter_key]['pattern'])
                    cur_transp = rule_data[cur_letter_key]['pattern'][cur_muster_indx]
                    cur_units_str = rule_data[cur_letter_key]['units']
                    cur_units_list = cur_units_str.split('/')
                    cur_units = float(cur_units_list[0]) / float(cur_units_list[1])
                    cur_note_obj_transp = Note(all_keys_current_pitches[cur_letter_key].midi + cur_transp * 2 * cur_units)

                # transpose cur_note_obj_transp to the 1st octave
                cur_midi_transp_1_okt = cur_note_obj_transp.midi % 12 + 60
                cur_comment = cur_letter # later for the lyrics
                cur_note_obj_output = Note(cur_midi_transp_1_okt, duration, articulation, cur_comment)
                output.append(cur_note_obj_output)

                # for printing out only
                cur_note_transp_1_okt = cur_note_obj_output.note

                print('Word:', cur_word_lower)
                print('Letter:', cur_letter)
                print('Pitch:', cur_notenname)
                print('Letter counter:', cur_key_counter)
                print('Number in the pattern:', cur_muster_indx + 1)
                print('MIDI:', cur_note_obj_transp.midi)
                print('MIDI transposed to 1st Octave:', cur_note_obj_transp.midi)
                print('Note name, 1st Octave: ', cur_note_transp_1_okt)

                log_file.write(str(cur_note_obj_output) + '\n')

                all_keys_current_pitches[cur_letter_key] = cur_note_obj_transp

        # nach jedem wort eine pause
        log_file.write('\n')
        output.append(Note(0))

    log_file.close()
    return output


print('\033c')
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=100))
main_menu()