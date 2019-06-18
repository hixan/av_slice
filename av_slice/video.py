# -*- coding: utf-8 -*-

from moviepy import editor


def remove_sections(video_clip, sections):  # {{{
    return editor.concatenate_videoclips(
        [video_clip.subclip(start, end) for start, end in sections]
    )
# }}}
