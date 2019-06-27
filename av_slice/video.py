# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips


def remove_sections(video_clip, sections):  # {{{
    return concatenate_videoclips(
        [video_clip.subclip(start, end) for start, end in sections]
    )
# }}}
