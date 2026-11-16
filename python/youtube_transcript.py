"""Transcripts of YouTube videos as plain text.

    python youtube_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ [more URLs or IDs]
"""
import os
import sys

from apify_client import ApifyClient

sys.stdout.reconfigure(encoding="utf-8")  # transcripts come in any script; a Windows console's code page fails on most
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/youtube-transcripts").call(logger=None, run_input={
    "videos": sys.argv[1:],
    "languages": ["en"],  # the caption languages to prefer, in order
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"# {item.get('title')}\n{item['url']}\n")
    print(item.get("text") or item.get("error"), end="\n\n")
