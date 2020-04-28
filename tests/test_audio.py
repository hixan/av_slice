#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `av_slice.audio`."""

import pytest

# from click.testing import CliRunner

import numpy as np
from moviepy.audio.AudioClip import AudioClip
from av_slice.audio import loud_sections
from av_slice.video import join_sections

'''

from av_slice.cli import video as cmd_video, audio as cmd_audio

def test_cmd_setup_video():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cmd_video, ['--help'])
    assert help_result.exit_code == 0, 'help call failed, check config'
    assert '--help' in help_result.output, 'help call failed, check config'


def test_cmd_setup_audio():
    runner = CliRunner()
    help_result = runner.invoke(cmd_audio, ['--help'])
    assert help_result.exit_code == 0, 'help call failed, check config'
    assert '--help' in help_result.output, 'help call failed, check config'

'''

# {{{ loud sections tests

@pytest.fixture
def loud_sections_audio():
    '''returns audioclip of different frequency, amplitude sine waves
    as follows:
       0| silent
        | silent
       1| normal tone
        | normal tone
       2| silent
        | silent
       3| high tone
        | high tone
       4| silent
        | silent
       5| low tone
        | low tone
       6| quiet
        | quiet
       7| normal tone
        | normal tone
       8| silent
        | silent
       9| silent
        | silent
        ...
        '''

    def make_audio_frame(ts):
        @np.vectorize
        def f(t):
            if t < 1:
                rv = 0  # silent
            elif t < 2:
                rv = np.sin(800 * np.pi * t)  # normal tone
            elif t < 3:
                rv = 0  # silent
            elif t < 4:
                rv = np.sin(1600 * np.pi * t)  # high tone
            elif t < 5:
                rv = 0  # silent
            elif t < 6:
                rv = np.sin(200 * np.pi * t)  # low tone
            elif t < 7:
                rv = np.sin(800 * np.pi * t) * .4  # quiet (40% volume)
            elif t < 8:
                rv = np.sin(800 * np.pi * t)  # normal tone
            else:
                rv = 0
            return rv
        # for some reason np.sin returns np.float64 here so that is emulated
        rv = f(ts)
        if rv.shape == ():  # rv is a 0d array
            return np.float64(rv)
        return rv
    return AudioClip(make_audio_frame, duration=100, fps=4200)


def test_loud_sections_1_start_nend(loud_sections_audio):
    # test when a section includes the very beginning but not the very end
    resolution = .05
    clip = loud_sections_audio.subclip(1.5, 2.5)
    expected = np.array([[1.5, 2]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.01))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_1_nstart_nend(loud_sections_audio):
    # test when a section includes neither the very beginning nor the very end
    resolution = .05
    clip = loud_sections_audio.subclip(0.5, 2.5)
    expected = np.array([[1, 2]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.01))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_1_nstart_end(loud_sections_audio):
    # test when a section includes the end but not beginning
    resolution = .05
    clip = loud_sections_audio.subclip(0.5, 1.5)
    expected = np.array([[1, 1.5]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.01))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_1_start_end(loud_sections_audio):
    # test when section includes beginning and end
    resolution = .05
    clip = loud_sections_audio.subclip(1.2, 1.7)
    expected = np.array([[1.2, 1.7]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.01))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_3_nstart_nend(loud_sections_audio):
    # test when section includes neither beginning nor end with 3 sections
    resolution = .05
    clip = loud_sections_audio.subclip(0.5, 6.5)
    expected = np.array([[1, 2], [3, 4], [5, 6]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.01))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_threshold(loud_sections_audio):
    # test when section includes neither beginning nor end with 3 sections
    resolution = .05
    clip = loud_sections_audio.subclip(4.5, 6.5)
    expected = np.array([[5, 6]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.5))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


def test_loud_sections_threshold_under(loud_sections_audio):
    # test when section includes neither beginning nor end with 3 sections
    resolution = .05
    clip = loud_sections_audio.subclip(4.5, 6.5)
    expected = np.array([[5, 6.5]])
    expected_len = len(expected)

    sections = np.array(loud_sections(clip, resolution, threshold=0.3))

    assert len(sections) == expected_len, 'returned wrong number of sections'
    assert max(np.sum(sections - expected, axis=1)) <= resolution * 2.01, \
        'sections were not accurate enough / had incorrect start/end times'


# remove sections tests
def test_remove_sections():
    pass
