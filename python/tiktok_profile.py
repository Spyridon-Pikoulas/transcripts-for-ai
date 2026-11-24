"""A TikTok creator's latest videos: views, the opening hook and the transcript.

    python tiktok_profile.py nasa 10
"""
import os
import sys

from apify_client import ApifyClient

profile, count = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10
sys.stdout.reconfigure(encoding="utf-8")  # transcripts come in any script; a Windows console's code page fails on most
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/tiktok-transcripts").call(logger=None, run_input={
    "profiles": [profile],
    "maxVideosPerProfile": count,
    "speechToText": False,  # True transcribes videos without captions too, with Whisper
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['views']:>10,} views  {item['url']}")
    print(f"  hook: {item.get('hook')}")
    print(f"  {(item.get('text') or item.get('noTranscriptReason') or '')[:300]}\n")
