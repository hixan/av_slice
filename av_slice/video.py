# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.VideoClip import VideoClip
from moviepy.audio.AudioClip import AudioClip
from typing import Tuple, Iterable, Union


def join_sections(
        video_clip: Union[VideoClip, AudioClip],
        sections: Iterable[Tuple[float, float]]
) -> VideoClip:
    '''join sections from video_clip endoded as a list of (start, end) timestamp pairs.

    :param video_clip: clip to extract sections from
    :param sections: list of (start_time, end_time) pairs that encode section timestamp values.
    :return: edited video_clip
    '''
    return concatenate_videoclips(
        [video_clip.subclip(start, end) for start, end in sections]
    )
# }}}
