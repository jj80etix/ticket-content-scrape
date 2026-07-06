import subprocess
from pathlib import Path

import requests

WHISPER_CHUNK_BYTES = 24 * 1024 * 1024


def clean_vtt(vtt_text):
    out = []
    for ln in vtt_text.splitlines():
        ln = ln.strip()
        if not ln or ln == "WEBVTT" or "-->" in ln or ln.isdigit():
            continue
        if not out or out[-1] != ln:
            out.append(ln)
    return "\n".join(out)


def youtube_captions(video_url, workdir):
    subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
         "--sub-langs", "en.*", "--sub-format", "vtt",
         "-o", f"{workdir}/%(id)s", video_url],
        check=True, capture_output=True, text=True, timeout=600)
    vtts = sorted(Path(workdir).glob("*.vtt"))
    if not vtts:
        raise RuntimeError(f"no captions for {video_url}")
    return clean_vtt(vtts[0].read_text())


def article_markdown(url):
    r = subprocess.run(["npx", "--yes", "defuddle-cli", "parse", url, "--markdown"],
                       check=True, capture_output=True, text=True, timeout=120)
    return r.stdout.strip()


def needs_chunking(size_bytes):
    return size_bytes > WHISPER_CHUNK_BYTES


# TODO before adding podcast sources: derive -segment_time from size/duration
# (fixed 1200s can exceed 25MB at >=192kbps) and handle non-mp3 enclosures
# (-c copy assumes mp3).
def podcast_transcript(enclosure_url, workdir):
    from openai import OpenAI  # deferred so tests don't need the key
    audio = Path(workdir) / "episode.mp3"
    with requests.get(enclosure_url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(audio, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    if needs_chunking(audio.stat().st_size):
        subprocess.run(
            ["ffmpeg", "-i", str(audio), "-f", "segment", "-segment_time",
             "1200", "-c", "copy", f"{workdir}/part%03d.mp3"],
            check=True, capture_output=True)
        parts = sorted(Path(workdir).glob("part*.mp3"))
    else:
        parts = [audio]
    client = OpenAI()
    texts = []
    for p in parts:
        with open(p, "rb") as f:
            texts.append(client.audio.transcriptions.create(
                model="whisper-1", file=f).text)
    return "\n".join(texts)
