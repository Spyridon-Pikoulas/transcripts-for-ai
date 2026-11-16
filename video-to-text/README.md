# How to convert a video or audio URL to text

Turn any video or audio into text from its URL: Loom, TED, Twitch, Dailymotion, SoundCloud,
Bilibili, YouTube and 1,000+ other sites, or a direct link to an .mp4, .mp3 or other file. Plain
text, timestamped segments or SRT/VTT subtitles, from Python, JavaScript or curl, through
[Video to Text & Audio to Text](https://apify.com/pikoulas/video-transcriber) on Apify.

The speech is transcribed by OpenAI's Whisper, run inside the Actor: nothing is sent to an outside
AI service. It costs $0.003 a started minute of audio, so $0.03 for a 10-minute video, and videos
with nothing said are free.

## Step by step

1. Sign up at [apify.com](https://apify.com) (the free plan covers a first run) and copy your API
   token from **Settings → API & Integrations**.
2. `pip install apify-client`
3. Run:

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/video-transcriber").call(logger=None, run_input={
    "urls": ["https://www.ted.com/talks/candace_parker_how_to_break_down_barriers_and_not_accept_limits"],
    "subtitles": True,  # also .srt and .vtt files, linked from each row
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item.get("title"), item.get("srtUrl"))
    print(item.get("text"))
```

[`python/video_to_srt.py`](../python/video_to_srt.py) downloads the .srt file.

## Options that matter

| Input | What it does |
|---|---|
| `maxVideosPerUrl` | For a playlist, channel or profile URL: how many of its latest videos. |
| `maxMinutesPerVideo` | Transcribe (and pay for) only each video's first minutes. |
| `model` | `base`, fast, or `small`, more accurate on accents, crosstalk and names ($0.008 a minute). |
| `translateToEnglish` | The text in English whatever the language spoken, at the same price. |
| `speakerLabels` | Who speaks when (`SPEAKER_1`, `SPEAKER_2`...), anonymous. |

## Output

```json
{
  "url": "https://www.ted.com/talks/candace_parker_how_to_break_down_barriers_and_not_accept_limits",
  "platform": "TedTalk",
  "title": "How to break down barriers and not accept limits",
  "uploader": "Candace Parker",
  "publishedAt": "2022-01-14",
  "durationSeconds": 679,
  "language": "en",
  "text": "You know everywhere in the world the question ...",
  "transcribedSeconds": 680,
  "isComplete": true,
  "billedMinutes": 12,
  "srtUrl": "https://api.apify.com/v2/key-value-stores/STORE_ID/records/transcript-0001.srt"
}
```

## FAQ

**A YouTube video has captions.** Then [YouTube Transcript Scraper](../youtube/README.md) is
faster and cheaper ($1 per 1,000 videos); this one is for videos without captions.

**Can an AI agent use it?** Yes, through Apify's MCP server: see the
[main README](../README.md#use-them-from-ai-agents-mcp).

**Other sources?** [TikTok](../tiktok/README.md), [Instagram Reels](../instagram/README.md) and
[podcasts](../podcasts/README.md) have Actors of their own, with each platform's details.
