import numpy as np
from moviepy.audio import AudioClip


def loud_sections(audio_clip, chunk_duration, threshold=.01):  # {{{

    # store sectional data
    loud_sections = []
    current_loud = False
    for i, chunk in enumerate(audio_clip.iter_chunks(
        chunk_duration=chunk_duration
    )):
        a = np.max(chunk)  # use numpy as chunk is a 2d array
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
    return loud_sections  # }}}


def remove_sections(audio_clip, sections):  # {{{
    return AudioClip.CompositeAudioClip(
        [audio_clip.subclip(start, end) for start, end in sections]
    )  # }}}
