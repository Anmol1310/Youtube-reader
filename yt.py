"""YouTube Reader - turn any YouTube video into text for AI agents.

Give it a video link, get back:
  - title, channel, thumbnail
  - full spoken text (transcript), with timestamps

No API key needed.
"""
import json
import re
import urllib.parse
import urllib.request

USER_AGENT = "YouTubeReader/1.0 (+agent-tool)"

# ---------------------------------------------------------------- helpers

def _get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _get_text(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def video_id_from_url(url):
    """Handles watch?v=, youtu.be/, /shorts/, /embed/, /live/ and bare IDs."""
    u = (url or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", u):
        return u
    if "://" not in u:
        u = "https://" + u
    p = urllib.parse.urlparse(u)
    q = urllib.parse.parse_qs(p.query)
    if q.get("v"):
        vid = q["v"][0]
    else:
        parts = [s for s in p.path.split("/") if s]
        vid = parts[-1] if parts else ""
    vid = re.sub(r"[^A-Za-z0-9_-]", "", vid)
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        raise ValueError("not_a_youtube_url")
    return vid

# ---------------------------------------------------------------- metadata (YouTube oEmbed - official, no key)

def get_metadata(video_id):
    try:
        data = _get_json(
            "https://www.youtube.com/oembed?url="
            + urllib.parse.quote("https://www.youtube.com/watch?v=" + video_id, safe="")
            + "&format=json"
        )
        return {
            "title": data.get("title", ""),
            "channel": data.get("author_name", ""),
            "channel_url": data.get("author_url", ""),
            "thumbnail": data.get("thumbnail_url", ""),
        }
    except Exception:
        return {"title": "", "channel": "", "channel_url": "", "thumbnail": ""}

# ---------------------------------------------------------------- transcript, method 1: library

def _transcript_via_library(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi

    # new API (v1.x)
    try:
        api = YouTubeTranscriptApi()
        for langs in (["en"], ["en-US", "en-GB"], None):
            try:
                ft = api.fetch(video_id) if langs is None else api.fetch(video_id, languages=langs)
                segs = [
                    {"start": round(s.start, 1), "text": s.text.replace("\n", " ")}
                    for s in ft.snippets
                ]
                if segs:
                    return segs, getattr(ft, "language", "en"), "library"
            except Exception:
                continue
    except Exception:
        pass
    # old API (pre-1.0)
    try:
        for langs in (["en"], ["en-US", "en-GB"]):
            try:
                raw = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
                segs = [
                    {"start": round(float(x["start"]), 1), "text": x["text"].replace("\n", " ")}
                    for x in raw
                ]
                if segs:
                    return segs, langs[0], "library"
            except Exception:
                continue
    except Exception:
        pass
    return None

# ---------------------------------------------------------------- transcript, method 2: Invidious fallback

INVIDIOUS_HOSTS = [
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://iv.melmac.space",
]


def _transcript_via_invidious(video_id):
    for host in INVIDIOUS_HOSTS:
        try:
            data = _get_json("%s/api/v1/captions/%s" % (host, video_id))
            caps = data.get("captions") if isinstance(data, dict) else data
            if not caps:
                continue
            # prefer english, else first
            pick = next((c for c in caps if c.get("languageCode", "").startswith("en")), caps[0])
            vtt = _get_text(host + pick["url"])
            segs = []
            for block in re.split(r"\n\n+", vtt):
                lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
                if not lines or lines[0].startswith("WEBVTT"):
                    continue
                m = re.match(r"(\d+):(\d+):(\d+)\.(\d+)\s*-->", lines[0])
                if m and len(lines) > 1:
                    h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    text = " ".join(re.sub(r"<[^>]+>", "", ln) for ln in lines[1:])
                    if text.strip():
                        segs.append({"start": h * 3600 + mi * 60 + s, "text": text.strip()})
            if segs:
                return segs, pick.get("languageCode", "en"), "invidious"
        except Exception:
            continue
    return None

# ---------------------------------------------------------------- main entry point

def read_video(url):
    video_id = video_id_from_url(url)
    meta = get_metadata(video_id)

    result = _transcript_via_library(video_id)
    if result is None:
        result = _transcript_via_invidious(video_id)

    if result is None:
        return {
            "video_id": video_id,
            "url": "https://www.youtube.com/watch?v=" + video_id,
            **meta,
            "transcript_available": False,
            "error": "no_captions_found",
        }

    segs, lang, source = result
    full_text = " ".join(s["text"] for s in segs)
    # keep segments but cap size for agent-friendly output
    return {
        "video_id": video_id,
        "url": "https://www.youtube.com/watch?v=" + video_id,
        **meta,
        "transcript_available": True,
        "language": lang,
        "segment_count": len(segs),
        "duration_seconds": segs[-1]["start"] if segs else 0,
        "full_text": full_text[:60000],
        "segments": segs[:200],
        "source": source,
    }


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    out = read_video(target)
    out["full_text"] = out.get("full_text", "")[:500] + "..."
    out["segments"] = out.get("segments", [])[:3]
    print(json.dumps(out, indent=2, ensure_ascii=False))
