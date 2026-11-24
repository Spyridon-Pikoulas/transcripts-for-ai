"""Each new episode of a podcast, transcribed once: run it daily or weekly (cron, or an Apify
schedule with the same input). The first run takes the latest episode; later runs only what came
out since, remembered in your Apify account.

    python podcast_new_episodes.py "The Daily"
"""
import os
import re
import sys
from pathlib import Path

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/podcast-transcripts").call(logger=None, run_input={
    "podcasts": [sys.argv[1]],  # a name, an Apple Podcasts URL or an RSS feed URL
    "maxEpisodes": 1,
    "onlyNewEpisodes": True,
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    if item.get("text"):
        path = Path(re.sub(r'[\\/:*?"<>|]+', "-", f"{item['publishedAt'][:10]} {item['episodeTitle'][:80]}") + ".txt")
        path.write_text(item["text"], "utf8")
        print("saved", path)
