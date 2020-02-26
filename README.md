# Revese Engineer a Synthesia Video

### To use:
1. Get a synthesia video as a `.mp4` file.
2. Run: `mkdir images && ffmpeg -i video.mp4 images/out-%01d.jpg`
3. Create a `note_mapping.txt` file and update it according to the video frames. The first number is the midi note, the second is the `x` coordinate of the note in the frame, the third is the `y` coordinate in the frame.
3. Run: `pip install -r requirements.txt`
4. Update the `bpm` variable in `main.py` if necessary.
4. Run: `python main.py`
5. Use any tool to convert a midi to sheet music.

See example output in `examples`.