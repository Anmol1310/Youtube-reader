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

## Step 5 — x402 agent-payment discovery (after payments go live)

IMPORTANT (verified Oct 2026): you CANNOT submit or "list" an endpoint on the
Coinbase CDP x402 Bazaar — there is no form and no listing API. A resource gets
indexed only after a real payment settles through the CDP facilitator, and each
facilitator's index is independent (CDP, thirdweb, PayAI each list only what
settled through them). So the real sequence is:

1. Declare discovery metadata in your 402 response (route, method, input
   example, output schema) — this is what lets an index catalogue you.
2. Make the first real payment happen through the CDP facilitator
   (a buyer call, or your own test payment) — that single settled payment is
   what puts you in the Bazaar index.
3. Verify by querying that facilitator's discovery index for your URL —
   per index, not once globally.
4. Agents also browse these public catalogues directly, so get visible there:
   Coinbase Agentic.Market (public catalog of x402 services), x402scan.

Honest note: an Oct 13, 2026 crawl of all 31,620 Bazaar listings found 77% had
two payers or fewer in 30 days, and 45.8% had exactly one (usually the seller's
own test payment). Being listed is not demand — the buyers still come from the
directories in Step 4, your GitHub README, and the human web page.

## What makes a listing win (the 3 rules)

1. **Clear title + one-line promise.** Robots (and humans) decide in 3 seconds.
2. **Show input → output.** Our README shows a real example. Most listings don't. Ours will stand out.
3. **Be in 10 places on day one.** Discovery is a numbers game — every listing is another door.
