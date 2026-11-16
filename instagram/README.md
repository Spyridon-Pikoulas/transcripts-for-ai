# How to transcribe Instagram Reels

Turn Instagram Reels into text: the whole script, the opening hook and timestamped lines, by reel
URL or a creator's whole profile, from Python, JavaScript or curl, through
[Instagram Video Transcript](https://apify.com/pikoulas/instagram-transcripts) on Apify. No
Instagram account, no browser.

Instagram has no captions to download, so the speech is transcribed by OpenAI's Whisper, run
inside the Actor: nothing is sent to an outside AI service. It costs $0.003 a started minute of
audio, so about $3 per 1,000 reels under a minute, and reels with nothing said are free.

## Step by step

1. Sign up at [apify.com](https://apify.com) (the free plan covers a first run) and copy your API
   token from **Settings → API & Integrations**.
2. `pip install apify-client`
3. Run:

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/instagram-transcripts").call(logger=None, run_input={
    "reels": ["https://www.instagram.com/reel/DfIfj7vS3qt/"],  # reel, post or tv URLs, or shortcodes
    "profiles": ["nasa"],                                       # a creator's latest reels
    "maxReelsPerProfile": 10,
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item["url"], item.get("hook"))
    print(item.get("text"))
```

[`python/instagram_hooks.py`](../python/instagram_hooks.py) lines up a creator's opening hooks by
likes: what works in a niche, side by side.

## Options that matter

| Input | What it does |
|---|---|
| `model` | `base`, fast, or `small`, more accurate on accents, names and languages other than English ($0.008 a minute). |
| `language` | The language spoken, when you know it; otherwise detected per reel. |
| `translateToEnglish` | The text in English whatever the language spoken, at the same price. |
| `includeTimestamps`, `subtitles` | Timestamped segments, and .srt/.vtt subtitle files. |
| `skipReelsWithoutSpeech` | Leaves out reels with music only. |

## Output

```json
{
  "code": "Dfc1mYxFevS",
  "url": "https://www.instagram.com/reel/Dfc1mYxFevS/",
  "authorUsername": "nasa",
  "createdAt": "2026-11-07T18:35:41Z",
  "durationSeconds": 63.5,
  "likes": 97005,
  "caption": "Apply to become an astronaut! ...",
  "language": "en",
  "hook": "The universe is calling. Will you answer?",
  "text": "The universe is calling. Will you answer? Training pushes you beyond your limits. Every day you learn something new. ...",
  "billedMinutes": 2
}
```

## FAQ

**Is the caption the transcript?** No: the caption is what the creator typed under the reel;
`text` is what is said in it.

**Can an AI agent use it?** Yes, through Apify's MCP server: see the
[main README](../README.md#use-them-from-ai-agents-mcp).

**Other platforms?** [YouTube](../youtube/README.md), [TikTok](../tiktok/README.md),
[podcasts](../podcasts/README.md) and [any other video or audio URL](../video-to-text/README.md).
