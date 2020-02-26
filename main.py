import os
from PIL import Image
import mido

bpm = 80

def get_color_diff(color1, color2):
  return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2])

# Get note mapping
with open('./note_mapping.txt') as file:
  lines = [x.strip().split(' ') for x in file.readlines()]

note_map = {}
for line in lines:
  note = line[0]
  x = line[1]
  y = line[2]
  if note.isdigit() and x.isdigit and y.isdigit():
    note_map[int(note)] = (int(x), int(y))

first_frame_note_to_color_map = {}
note_on_map = { x: False for x in note_map.keys() }
events = []

# Loop over frames
for i in range(len(os.listdir('./images'))):
  img = Image.open(f'./images/out-{i+1}.jpg')

  for note, coords in note_map.items():
    color = img.getpixel(coords)
    if i == 0:
      first_frame_note_to_color_map[note] = color
    else:
      first_color = first_frame_note_to_color_map[note]
      colorDiff = get_color_diff(first_color, color)
      if (colorDiff > 50):
        if not note_on_map[note]:
          note_on_map[note] = True
          events.append({ 'note': note, 'on': True, 'time': i })
      else:
        if note_on_map[note]:
          note_on_map[note] = False
          events.append({ 'note': note, 'on': False, 'time': i })

mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

# Meta
track.append(mido.MetaMessage('set_tempo', tempo=int(mido.bpm2tempo(bpm))))
mid.ticks_per_beat = int((bpm / 60) / (1 / 29.97))

last_time = 0
for event in events:
  delta_time = event['time'] - last_time
  message_type = 'note_on' if event['on'] else 'note_off'
  track.append(mido.Message(message_type, note=event['note'], velocity=64, time=delta_time))
  last_time = event['time']

mid.save('output.mid')