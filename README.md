# YouTube Reader

Turn any YouTube video into text. For AI agents that can't watch video.

Give it a video link. Get back the title, channel, and the full spoken
transcript with timestamps. One call, clean JSON. No API key needed.

## Quick example

**You send:**
```json
POST /read
{ "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" }
```

**You get:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
  "channel": "Rick Astley",
  "channel_url": "https://www.youtube.com/@RickAstleyYT",
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
  "transcript_available": true,
  "language": "English",
  "segment_count": 61,
  "duration_seconds": 213,
  "full_text": "We're no strangers to love...",
  "segments": [
    { "start": 18.5, "text": "We're no strangers to love" },
    { "start": 22.1, "text": "You know the rules and so do I" }
  ]
}
```

## Run it

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python server.py        # http://127.0.0.1:8081
```

- `POST /read` with `{"url": "<youtube link>"}` → full report (JSON)
- `GET /health` → `{"ok": true}`

Accepts `watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, `/live/` links and bare video IDs.

## Use as an MCP server (Claude Desktop, Cursor, Windsurf...)

```
.venv/bin/pip install fastmcp
.venv/bin/python mcp_server.py
```

One tool: `youtube_reader(url)` — same report as the HTTP API.

## How transcripts are fetched (in order)

1. `youtube-transcript-api` — direct, free
2. Invidious instances — fallback, free

Known limitation: YouTube rate-limits automated requests from datacenter
IPs, so transcript fetches can intermittently fail from cloud servers.
Metadata (title/channel via official oEmbed) is unaffected. Professional
fix: add a residential proxy (~$3 per 1,000 transcripts) as step 3.

## Deploy (Railway, free tier)

1. Push this folder to GitHub
2. https://railway.app → New Project → Deploy from repo
3. It reads `requirements.txt` + `Procfile` automatically. Done.
4. Your API is live at the Railway URL: `POST https://<your-app>.up.railway.app/read`

## Pricing

- Metadata (title/channel): free
- Transcript via MCP (`youtube_reader` tool): **$0.02 per call**, paid in USDC on Base via x402 — no signup, no API key. See [PAYMENTS.md](PAYMENTS.md).
- Plain HTTP API (`POST /read`): free while in beta
- Heavy users: $19/month tier planned (Stripe, phase 2)

## Monetization (MCPize)

Per-call pricing is configured in [mcpize.yaml](mcpize.yaml) and the MCPize
dashboard (Payments tab). Full setup guide, wallet instructions, testnet
flow, and caveats: [PAYMENTS.md](PAYMENTS.md).
