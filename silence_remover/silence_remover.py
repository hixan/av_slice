# -*- coding: utf-8 -*-

from moviepy import editor
import numpy as np
import argparse


frames_per_chunk = 1  # duration of chunks in seconds. smaller means more
# accurate representation (to a point) but slower computation. pointless to go
# more than video framerate / 2 as the final video cant be cut into pieces
# smaller then the length of 1 frame, and you cannot cut one frame in to
# smaller pieces to change the start/end of your window.


def _chunk_to_timestamp(chunknumber, chunk_duration):
    return chunknumber * chunk_duration


def remove_silence(filename, output_filename=None, threshold=.01):  # {{{

    inpt = editor.VideoFileClip(filename)
    try:
        fps = inpt.fps
    except AttributeError:
        print(
            'remove_silence:',
            f'unable to extract framerate from {filename}; assuming 30.'
        )
        fps = 30
    if output_filename is None:
        n, *ext = filename.split('.')
        output_filename = f'{n}_modified.{".".join(ext)}'
    print(f'saving result to {output_filename}')

    print('calculating removals...')

    with editor.AudioFileClip(filename) as sound:
        # initialise and calculate required variables

        # duration of chunk in seconds
        chunk_duration = frames_per_chunk / fps

        # number of frames per chunk
        chunk_length = int(chunk_duration * sound.fps)

        # number of seconds per chunk (altered)
        chunk_duration = chunk_length / sound.fps

        # store sectional data
        silent_sections = []
        current_loud = False
        for i, chunk in enumerate(sound.iter_chunks(chunksize=chunk_length)):
            a = np.max(chunk)
            if not current_loud:
                if a >= threshold:
                    start_loud = _chunk_to_timestamp(i, chunk_duration)
                    current_loud = True
            else:
                if a < threshold:
                    silent_sections.append(
                        (start_loud, _chunk_to_timestamp(i, chunk_duration))
                    )
                    current_loud = False

    start, end = np.array(silent_sections).T

    print('making', len(silent_sections), 'cuts.')

    clips = []
    for start, end in silent_sections:
        clips.append(inpt.subclip(start, end))
    print('rendering...')
    final = editor.concatenate_videoclips(clips)
    final.write_videofile(output_filename)
# }}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='automatically remove silent portions from a video'
    )
    parser.add_argument(
        'file',
        help='path to video file that is to be edited.'
    )
    parser.add_argument(
        '--output_file', '-o', default=None,
        help='destination for modified video. Default modifies original' +
        ' filename.'
    )
    parser.add_argument(
        '--threshold', '-t', type=float, default=.01,
        help='threshold volume under which frames are removed. Default .01.'
    )
    args = parser.parse_args()

    remove_silence(
        args.file, output_filename=args.output_file, threshold=args.threshold
    )
