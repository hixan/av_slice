# -*- coding: utf-8 -*-

from moviepy import editor
from audio import quiet_sections
import argparse


def remove_sections(video_clip, sections):  # {{{
    return editor.concatenate_videoclips(
        [video_clip.subclip(start, end) for start, end in sections]
    )
    clips = []
    for start, end in sections:
        clips.append(video_clip.subclip(start, end))
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
    cuts = quiet_sections(inpt.audio, int(inpt.audio.fps/inpt.fps))
    print(f'making {len(cuts)} cuts')
    final = remove_sections(inpt, cuts)
    final.write_videofile(output_file)
