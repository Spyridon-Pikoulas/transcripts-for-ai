"""A YouTube channel's latest videos, one Markdown file each with its details: a folder ready to
load into a RAG pipeline or a notes app.

    python youtube_channel_to_markdown.py @lexfridman 10
"""
import os
import re
import sys
from pathlib import Path

from apify_client import ApifyClient

channel, count = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/youtube-transcripts").call(logger=None, run_input={
    "channels": [channel],
    "maxVideosPerSource": count,
})
out = Path(channel.strip("@"))
out.mkdir(exist_ok=True)
for item in client.dataset(run.default_dataset_id).iterate_items():
    if not item.get("text"):
        continue  # no captions: video-transcriber transcribes the speech
    name = re.sub(r"[^\w-]+", "-", item["title"]).strip("-")[:80]
    (out / f"{item['publishedAt'][:10]}-{name}.md").write_text(
        f"---\ntitle: {item['title']!r}\nurl: {item['url']}\nchannel: {item['channel']!r}\n"
        f"published: {item['publishedAt']}\n---\n\n{item['text']}\n", "utf8")
    print("saved", item["title"])
