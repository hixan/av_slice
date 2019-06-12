from moviepy import editor
import click
from av_slice.audio import quiet_sections
from av_slice.video import remove_sections


@click.command()
@click.option('--output_file', default='', help='filename of output')
@click.argument('file')
@click.option('--threshold', default=.01,
              help='threshold under which to make a cut')
def _video_silence(file, output_file, threshold):
    if output_file == '':
        n, *ext = file.split('.')
        output_file = f'{n}_modified.{".".join(ext)}'
    click.echo(f'saving result to {output_file}')
    click.echo('calculating removals...')
    inpt = editor.VideoFileClip(file)

    # chunk_length is the number of audio frames in 1 video frame as this is
    # the smallest resolution possible to split the video up into.
    cuts = quiet_sections(inpt.audio, int(inpt.audio.fps/inpt.fps),
                          threshold=threshold)
    click.echo(f'making {len(cuts)} cuts')
    final = remove_sections(inpt, cuts)
    final.write_videofile(output_file)


_video_silence()
