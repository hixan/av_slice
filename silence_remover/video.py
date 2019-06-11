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
