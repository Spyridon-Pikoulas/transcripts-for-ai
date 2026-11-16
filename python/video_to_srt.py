"""Any video or audio URL to an .srt subtitle file (Loom, TED, Twitch, SoundCloud, an .mp4 or .mp3
link and 1,000+ more sites).

    python video_to_srt.py https://www.ted.com/talks/candace_parker_how_to_break_down_barriers_and_not_accept_limits
"""
import os
import sys
import urllib.request

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/video-transcriber").call(logger=None, run_input={
    "urls": [sys.argv[1]],
    "subtitles": True,
    "translateToEnglish": False,  # True: English subtitles whatever the language spoken
})
for n, item in enumerate(client.dataset(run.default_dataset_id).iterate_items(), 1):
    if item.get("srtUrl"):
        name = f"transcript-{n}.srt"
        urllib.request.urlretrieve(item["srtUrl"], name)
        print("saved", name, "-", item.get("title"))
    else:
        print("no transcript:", item.get("noTranscriptReason"))
