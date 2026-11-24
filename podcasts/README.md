# How to transcribe a podcast

Turn podcast episodes into text: one episode, a whole show, or each new episode as it comes out,
by Apple Podcasts URL, RSS feed, audio file or just the podcast's name, from Python, JavaScript or
curl, through [Podcast Transcription](https://apify.com/pikoulas/podcast-transcripts) on Apify.

The speech is transcribed by OpenAI's Whisper, run inside the Actor: nothing is sent to an outside
AI service. It costs $0.003 a started minute of audio, so $0.18 for an hour-long episode. Speaker
labels (who speaks when) are $0.01 a minute more.

## Step by step

1. Sign up at [apify.com](https://apify.com) (the free plan covers a first run) and copy your API
   token from **Settings → API & Integrations**.
2. `pip install apify-client`
3. Run:

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/podcast-transcripts").call(logger=None, run_input={
    "podcasts": ["Lex Fridman Podcast"],  # a name, an Apple Podcasts show or episode URL, an RSS feed or an .mp3 link
    "maxEpisodes": 1,                      # the latest episodes of each show
    "maxMinutesPerEpisode": 10,            # optional: transcribe (and pay for) only the start
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item["episodeTitle"])
    print(item.get("text"))
```

## Each new episode, automatically

Turn on `onlyNewEpisodes` and run it on a schedule (cron, or Apify's **Schedules**): each run
transcribes only the episodes published since the last one, remembered in your Apify account, and
a run with nothing new costs nothing.
[`python/podcast_new_episodes.py`](../python/podcast_new_episodes.py) does that and saves each
transcript as a text file.

## Options that matter

| Input | What it does |
|---|---|
| `searchTerms` | Episodes across all of Apple Podcasts that mention a topic, a company or a person. |
| `model` | `base`, fast, or `small`, more accurate on accents, crosstalk and names ($0.008 a minute). |
| `translateToEnglish` | The text in English whatever the language spoken, at the same price. |
| `speakerLabels` | Who speaks when (`SPEAKER_1`, `SPEAKER_2`...), anonymous. |
| `includeTimestamps`, `subtitles` | Timestamped segments, and .srt/.vtt subtitle files. |

## Output

```json
{
  "podcastTitle": "Lex Fridman Podcast",
  "episodeTitle": "#504 – Russia-Ukraine War: Putin, Zelenskyy, Drones and the Future of Warfare",
  "publishedAt": "2026-11-10T23:52:44Z",
  "durationSeconds": 10875,
  "audioUrl": "https://media.blubrry.com/takeituneasy/ins.blubrry.com/takeituneasy/lex_ai_preston_stewart_michael_kofman.mp3",
  "language": "en",
  "text": "The following is a conversation with ... about the war in Ukraine. ...",
  "transcribedSeconds": 596.8,
  "isComplete": false,
  "billedMinutes": 10
}
```

`isComplete` is false here because `maxMinutesPerEpisode` stopped it at 10 minutes.

## FAQ

**Spotify-only shows?** Spotify's exclusives have no public audio; any show with an RSS feed
(nearly all) works, by its name, Apple Podcasts URL or feed.

**Can an AI agent use it?** Yes, through Apify's MCP server: see the
[main README](../README.md#use-them-from-ai-agents-mcp).

**Other sources?** [YouTube](../youtube/README.md), [TikTok](../tiktok/README.md),
[Instagram Reels](../instagram/README.md) and [any other video or audio URL](../video-to-text/README.md).
