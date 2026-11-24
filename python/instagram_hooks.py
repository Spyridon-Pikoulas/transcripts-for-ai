"""The opening hooks of a creator's reels (what's said in the first 3 seconds), with likes:
what works in a niche, side by side.

    python instagram_hooks.py hubermanlab 10
"""
import os
import sys

from apify_client import ApifyClient

profile, count = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10
sys.stdout.reconfigure(encoding="utf-8")  # transcripts come in any script; a Windows console's code page fails on most
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/instagram-transcripts").call(logger=None, run_input={
    "profiles": [profile],
    "maxReelsPerProfile": count,
    "skipReelsWithoutSpeech": True,
})
for item in sorted(client.dataset(run.default_dataset_id).iterate_items(), key=lambda i: -(i.get("likes") or 0)):
    print(f"{item.get('likes') or 0:>9,} likes  {item['url']}\n  {item.get('hook')}\n")
