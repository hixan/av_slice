# -*- coding: utf-8 -*-

from moviepy import editor
import numpy as np
import argparse


frames_per_chunk = 1  # duration of chunks in seconds. smaller means more
# accurate representation (to a point) but slower computation. pointless to go
# more than video framerate / 2 as the final video cant be cut into pieces
# smaller then the length of 1 frame, and you cannot cut one frame in to
# smaller pieces to change the start/end of your window.


def find_quiet(audio_clip, chunk_width, threshold=.01):

    assert type(chunk_width) is int
    # store sectional data
    silent_sections = []
    current_loud = False
    for i, chunk in enumerate(audio_clip.iter_chunks(chunksize=chunk_width)):
        a = np.max(chunk)
        if not current_loud:
            if a >= threshold:
                start_loud = i * chunk_width / audio_clip.fps
                current_loud = True
        else:
            if a < threshold:
                silent_sections.append(
                    (start_loud, i * chunk_width / audio_clip.fps)
                )
                current_loud = False
    return silent_sections


def remove_sections(video_clip, sections):  # {{{
    clips = []
    for start, end in sections:
        clips.append(inpt.subclip(start, end))
    return editor.concatenate_videoclips(clips)
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

    if args.output_file is None:
        n, *ext = args.file.split('.')
        output_file = f'{n}_modified.{".".join(ext)}'
    else:
        output_file = args.output_file
    print(f'saving result to {output_file}')
    print('calculating removals...')
    inpt = editor.VideoFileClip(args.file)

    # chunk_length is the number of audio frames in 1 video frame as this is
    # the smallest resolution possible to split the video up into.
    cuts = find_quiet(inpt.audio, int(inpt.audio.fps/inpt.fps))
    print(f'making {len(cuts)} cuts')
    final = remove_sections(inpt, cuts)
    final.write_videofile(output_file)
