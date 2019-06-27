# -*- coding: utf-8 -*-

"""Console script for av_slice."""
import sys
import click
from moviepy import editor
from av_slice.audio import loud_sections, remove_sections as a_remove_sections
from av_slice.video import remove_sections as v_remove_sections


@click.command()
@click.option('--output_file', default='', help='filename of output')
@click.argument('file')
@click.option('--threshold', default=.01,
              help='threshold under which to make a cut')
def video(file, output_file, threshold):
    if output_file == '':
        n, *ext = file.split('.')
        output_file = f'{n}_modified.{".".join(ext)}'
    click.echo(f'saving result to {output_file}')
    click.echo('calculating removals...')
    inpt = editor.VideoFileClip(file)

    # chunk_length is the number of audio frames in 1 video frame as this is
    # the smallest resolution possible to split the video up into.
    cuts = loud_sections(inpt.audio, int(inpt.audio.fps/inpt.fps),
                          threshold=threshold)
    click.echo(f'making {len(cuts)} cuts')
    final = v_remove_sections(inpt, cuts)
    final.write_videofile(output_file)


@click.command()
@click.option('--output_file', default='', help='filename of output')
@click.argument('file')
@click.option('--threshold', default=.01,
              help='threshold under which to make a cut')
@click.option('-a', 'audio_input', help='input file is an audio file',
              is_flag=True, flag_value=True)
@click.option('-v', 'audio_input', help='input file is a video file',
              is_flag=True, flag_value=False)
@click.option('--resolution', default=1/30,
              help='resolution of search in seconds')
def audio(file, output_file, threshold, audio_input, resolution):
    click.echo(f'extracting audio from {file} and removing silent/quiet' +
               ' portions')
    if output_file == '':
        n, *ext = file.split('.')
        output_file = f'{n}_modified.{".".join(ext)}'
    click.echo(f'saving result to {output_file}')
    click.echo(f'calculating removals...')
    if audio_input:
        audio = editor.AudioFileClip(file)
    else:
        infile = editor.VideoFileClip(file)
        audio = infile.audio
    cuts = loud_sections(audio, resolution, threshold=threshold)
    final = a_remove_sections(audio, cuts)
    final.write_audiofile(output_file, fps=audio.fps)


if __name__ == "__main__":
    sys.exit(video())  # pragma: no cover
