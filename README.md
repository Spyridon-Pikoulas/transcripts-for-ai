# Transcripts for AI

Get transcripts from YouTube, TikTok, Instagram Reels, podcasts and any video or audio URL as
clean text, timestamped segments or SRT/VTT subtitles, ready for LLMs, RAG and AI agents. Each
source has its own [Apify](https://apify.com) Actor, called from Python, JavaScript, curl or an
MCP client, and they all return the same core fields: `text`, `language`, `durationSeconds` and,
with timestamps on, `segments`, each line with its start and end in seconds.

| Source | Actor | Input | Price |
|---|---|---|---|
| YouTube | [YouTube Transcript Scraper & API](https://apify.com/pikoulas/youtube-transcripts) | videos, channels, playlists, searches | $1 per 1,000 transcripts |
| TikTok | [TikTok Transcript Scraper](https://apify.com/pikoulas/tiktok-transcripts) | videos, profiles, hashtags, searches | $1 per 1,000 transcripts |
| Instagram | [Instagram Video Transcript](https://apify.com/pikoulas/instagram-transcripts) | reels, profiles | $0.003 per audio minute |
| Podcasts | [Podcast Transcription](https://apify.com/pikoulas/podcast-transcripts) | Apple Podcasts, RSS feeds, audio files | $0.003 per audio minute |
| Anything else | [Video to Text & Audio to Text](https://apify.com/pikoulas/video-transcriber) | any video or audio URL (1,000+ sites) or file | $0.003 per audio minute |

YouTube and TikTok transcripts come from the captions the platform has. Instagram, podcasts and
other videos are transcribed by OpenAI's Whisper, run inside the Actor (nothing is sent to an
outside AI service), with optional translation to English, and speaker labels for podcasts and
videos. Apify's free plan covers a first run of each.

## How-to guides

- [How to get YouTube transcripts with Python](youtube/README.md): a video, a channel, a
  playlist or a search, from a hosted API.
- [How to get TikTok transcripts](tiktok/README.md): a video, a creator's profile, a hashtag.
- [How to transcribe Instagram Reels](instagram/README.md): the script and the opening hook.
- [How to transcribe a podcast](podcasts/README.md): an episode, a whole show, or each new
  episode on a schedule.
- [How to convert a video or audio URL to text](video-to-text/README.md): Loom, TED, Twitch,
  SoundCloud, audio files and 1,000+ more, with SRT subtitles.

## Quick start

1. Sign up at [apify.com](https://apify.com) (free) and copy your API token from
   **Settings → API & Integrations**.
2. `pip install apify-client` and `export APIFY_TOKEN=...`
3. Run any script in [`python/`](python/), e.g.
   `python python/youtube_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("pikoulas/youtube-transcripts").call(logger=None, run_input={
    "videos": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item["title"], item["text"][:200])
```

The same in [JavaScript](javascript/youtube-transcript.mjs), or with curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/pikoulas~youtube-transcripts/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"videos": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]}'
```

## Use them from AI agents (MCP)

Claude, ChatGPT, Cursor and other MCP clients can call all five as tools through
[Apify's MCP server](https://mcp.apify.com):

```json
{
  "mcpServers": {
    "transcripts": {
      "url": "https://mcp.apify.com?tools=pikoulas/youtube-transcripts,pikoulas/tiktok-transcripts,pikoulas/instagram-transcripts,pikoulas/podcast-transcripts,pikoulas/video-transcriber",
      "headers": {"Authorization": "Bearer YOUR_APIFY_TOKEN"}
    }
  }
}
```

Then ask in plain words: "Get the transcripts of the last 5 videos on @lexfridman and list the
guests' main claims."

## Examples

| Script | What it does |
|---|---|
| [`python/youtube_transcript.py`](python/youtube_transcript.py) | Transcripts of YouTube videos as plain text |
| [`python/youtube_channel_to_markdown.py`](python/youtube_channel_to_markdown.py) | A channel's latest videos, one Markdown file each, for RAG |
| [`python/tiktok_profile.py`](python/tiktok_profile.py) | A TikTok creator's latest videos: views, hook, transcript |
| [`python/instagram_hooks.py`](python/instagram_hooks.py) | The opening hooks of a creator's reels |
| [`python/podcast_new_episodes.py`](python/podcast_new_episodes.py) | Each new episode of a podcast, once, for a scheduled job |
| [`python/video_to_srt.py`](python/video_to_srt.py) | Any video URL to an .srt subtitle file |
| [`python/langchain_documents.py`](python/langchain_documents.py) | Transcripts as LangChain `Document`s with their source metadata |
| [`javascript/youtube-transcript.mjs`](javascript/youtube-transcript.mjs) | YouTube transcripts from Node.js |

## License

The examples are MIT licensed. The Actors are paid per result on Apify; see each one's page for
its pricing.
