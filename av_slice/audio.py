import numpy as np
from moviepy.audio.AudioClip import AudioClip
from typing import List, Tuple


def loud_sections(
        audio_clip: AudioClip,
        chunk_duration: float,
        threshold: float = .01
) -> List[Tuple[float, float]]:
    '''Finds loud sections in audio_clip.

    :param audio_clip: the audio_clip to search
    :param chunk_duration: resolution of search
    :param threshold: volume cutoff threshold
    :return: list of sections that contain audio above the threshold.
    '''

    # store sectional data
    loud_sections = []
    current_loud = False

    for i, chunk in enumerate(audio_clip.iter_chunks(
        chunk_duration=chunk_duration
    )):
        a = np.max(chunk)  # use numpy as chunk is an nd array
        if not current_loud:
            if a >= threshold:
                start_loud = i * chunk_duration
                current_loud = True
        else:
            if a < threshold:
                loud_sections.append(
                    (start_loud, i * chunk_duration)
                )
                current_loud = False
    if current_loud:  # add last loud section if necessary.
        loud_sections.append((start_loud, audio_clip.duration))
    return loud_sections
