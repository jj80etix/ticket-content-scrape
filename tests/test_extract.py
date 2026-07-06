from harvest.extract import clean_vtt, needs_chunking

VTT = """WEBVTT

00:00:00.000 --> 00:00:02.000
hello world

00:00:02.000 --> 00:00:04.000
hello world
next line
"""


def test_clean_vtt_strips_cues_and_dedups():
    assert clean_vtt(VTT) == "hello world\nnext line"


def test_needs_chunking_threshold():
    assert not needs_chunking(24 * 1024 * 1024)
    assert needs_chunking(24 * 1024 * 1024 + 1)
