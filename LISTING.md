# Listing Pack — YouTube Reader

Everything copy-paste ready. Do these in order.

## The copy (use everywhere)

- **Name:** YouTube Reader
- **Tagline:** Turn any YouTube video into text — transcript, title, channel, timestamps.
- **Short description (for directories):** AI agents can't watch video. Give this tool a YouTube link and get back the full spoken transcript with timestamps, plus title, channel and thumbnail. One call, clean JSON, no API key.
- **Tags:** youtube, transcript, captions, video, transcription, metadata, subtitles

## Step 1 — GitHub repo (everything links here)

1. Create a new public repo named `youtube-reader`
2. Upload this folder (README.md is already written to sell it)
3. Done — this URL goes into every listing below

## Step 2 — Railway deploy (free, your API goes live)

1. https://railway.app → sign up (GitHub login, 2 minutes)
2. New Project → Deploy from repo → pick `youtube-reader`
3. Railway reads `requirements.txt` + `Procfile` automatically
4. You get a URL like `https://youtube-reader.up.railway.app`
5. Test: `POST https://youtube-reader.up.railway.app/read` with `{"url": "<youtube link>"}`

For the MCP remote endpoint (needed for the official registry), add a
second Railway service in the same project with start command:
`.venv/bin/python mcp_server.py --http` — or simply `python mcp_server.py --http`
with `fastmcp` added to requirements.

## Step 3 — Official MCP Registry (free, the big one)

On your computer:

```
brew install mcp-publisher        # or download the binary for your OS
cd youtube-reader
```

1. Open `.mcp/server.json` and replace the 3 placeholders:
   - `YOUR-GITHUB-USERNAME` → your GitHub name (2 places)
   - `YOUR-APP.up.railway.app` → your Railway URL (1 place)
2. `mcp-publisher login github` → approve in browser
3. `mcp-publisher publish`
4. Done — you're in the official registry that other directories read from.

## Step 4 — Community directories (free listings)

Submit to ALL of these — each is a backlink and a discovery channel.
Use the copy from the top of this file.

| Directory | How | Cost |
|---|---|---|
| mcpservers.org | submit form on site | free (review up to 2 weeks) or $39 for 24h |
| Smithery.ai | sign up → submit | free |
| PulseMCP | submit listing | free |
| Glama.ai | submit | free (curated) |
| mcp.so | submit | $39 web form, or free via GitHub issue |
| Cline Marketplace | submit | free |

## Step 5 — Agent payment directories (after payments go live)

- x402scan, Agent402, 402 Index — list every payable endpoint the hour you ship payments
- Coinbase CDP Bazaar — also use it to spy on what actually sells before building tool #2

## What makes a listing win (the 3 rules)

1. **Clear title + one-line promise.** Robots (and humans) decide in 3 seconds.
2. **Show input → output.** Our README shows a real example. Most listings don't. Ours will stand out.
3. **Be in 10 places on day one.** Discovery is a numbers game — every listing is another door.
