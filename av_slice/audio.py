import numpy as np

def quiet_sections(audio_clip, chunk_duration, threshold=.01):  # {{{

    # store sectional data
    silent_sections = []
    current_loud = False
    for i, chunk in enumerate(audio_clip.iter_chunks(
        chunk_duration=chunk_duration,
        progress_bar=True
    )):
        a = np.max(chunk)  # use numpy as chunk is a 2d array
        if not current_loud:
            if a >= threshold:
                start_loud = i * chunk_duration
                current_loud = True
        else:
            if a < threshold:
                silent_sections.append(
                    (start_loud, i * chunk_duration)
                )
                current_loud = False
    return silent_sections  # }}}

