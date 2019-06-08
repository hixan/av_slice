# -*- coding: utf-8 -*-

from moviepy import editor
import numpy as np

threshold = .01
fps = 30
frames_per_chunk = 2  # duration of chunks in seconds. smaller means more
# accurate representation (to a point) but slower computation. pointless to go
# more than video framerate / 2 as the final video cant be cut into pieces
# smaller then the length of 1 frame, and you cannot cut one frame in to
# smaller pieces to change the start/end of your window.


def chunk_to_timestamp(chunknumber, chunk_duration):
    return chunknumber * chunk_duration


with editor.AudioFileClip('test.mp4') as sound:
    # initialise and calculate required variables

    # duration of chunk in seconds
    chunk_duration = frames_per_chunk / fps

    # number of frames per chunk
    chunk_length = int(chunk_duration * sound.fps)

    # number of seconds per chunk (altered)
    chunk_duration = chunk_length / sound.fps

    # store sectional data here
    silent_sections = []
    current_loud = False
    for i, chunk in enumerate(sound.iter_chunks(chunksize=chunk_length)):
        a = np.max(chunk)
        if not current_loud:
            if a >= threshold:
                start_loud = chunk_to_timestamp(i, chunk_duration)
                current_loud = True
        else:
            if a < threshold:
                silent_sections.append(
                    (start_loud, chunk_to_timestamp(i, chunk_duration))
                )
                current_loud = False
start, end = np.array(silent_sections).T

print('making', len(silent_sections), 'cuts.')

inpt = editor.VideoFileClip('test.mp4')
clips = []
for start, end in silent_sections:
    clips.append(inpt.subclip(start, end))
print('rendering...')
final = editor.concatenate_videoclips(clips)
final.write_videofile('output.mp4')
