# Payments — YouTube Reader

Robots pay per use, automatically. No sales calls, no invoicing, no chasing.

## The choice (and why)

**We use MCPize pay-per-call (x402) — NOT self-hosted x402, NOT Stripe.**

| Option | Verdict |
|---|---|
| **MCPize x402** (chosen) | Dashboard config only. They run the facilitator (verification + settlement), handle the 402 challenge, and settle USDC straight to your wallet. No code, no keys to manage, no crypto knowledge needed. 80% revenue share. |
| Self-hosted x402 | Rejected for now. Real but tricky: the production facilitator (Coinbase CDP) needs API-key auth with JWT signing — real backend work, and anything that breaks, only a developer can fix. Worth revisiting when volume justifies it (protocol is open, same wallet works). |
| MCPize subscriptions | Rejected for agents. Human checkout flow — a robot can't complete Stripe Checkout. Fine as a *human* phase-2, not for agents. |
| Plain Stripe per-call | Rejected. 2.9% + $0.30 per transaction makes a $0.02 payment impossible. Also needs full KYC before you can receive anything. |

Why x402 at all: it's the only rail where a $0.02 machine payment makes economic sense,
and the only one where the buyer needs no account — the agent just pays and goes.
That's exactly our "zero human sales" requirement.

**Honest caveat:** x402 is young. Across all non-crypto utility sellers, roughly
~$3,900 total changed hands in 30 days (Oct 2026 data) — real, but tiny. We are
positioning early, not harvesting existing demand. The fee (20%) only matters
once there's revenue; 80% of something beats 100% of nothing that never ships.

## How it works (5 lines)

1. Agent calls the `youtube_reader` tool **without** payment.
2. MCPize answers HTTP 402: "this costs $0.02 in USDC on Base, pay here."
3. Agent signs the payment from its own wallet and retries with the payment attached.
4. MCPize verifies with a facilitator, settles USDC **directly to your wallet**.
5. The tool runs, the agent gets the transcript. Nobody signed up for anything.

## Anmol's checklist (phone, ~20 minutes total)

**Step 1 — Get a wallet (5 min, free)**
1. Install **Coinbase Wallet** from your app store.
2. Create a new wallet. **Write down the recovery phrase on paper and keep it
   safe. Never share it with anyone, ever.** Lose it = lose the money.
3. In the app, make sure **Base** network is enabled. Tap Receive → copy your
   address (starts with `0x`).

**Step 2 — Tell us the address (1 min)**
- Send the `0x...` address to the chat. We'll put it in `mcpize.yaml`
  (`recipient:`) — or edit that one line on GitHub yourself.

**Step 3 — MCPize account + connect your server (~10 min)**
1. Go to **mcpize.com** → sign up.
2. **New server** → look for **Advanced Options** → **Your Server endpoint** →
   paste: `https://web-production-0cbb7.up.railway.app/mcp`
   - Skip the GitHub App connection (keeps your Railway deployment as-is).
   - *If there's no bring-your-own-endpoint option anymore:* use their
     "deploy from repo" instead and point it at your GitHub repo —
     same result, they host it.
3. Publish the listing.

**Step 4 — Turn on payments (3 min)**
1. Open the **Payments** tab in your server dashboard.
2. Paste your wallet address, set network to **base-sepolia** (testnet first),
   set `youtube_reader` price to **0.02**. Save.

**Step 5 — Test for free (5 min)**
1. Get free testnet USDC: **faucet.circle.com** (choose Base Sepolia).
2. Call your tool through an x402-aware client — you should get the 402,
   pay with testnet USDC, and get the transcript back.
3. When it works end-to-end: flip `network` to **base** in the dashboard
   (and in `mcpize.yaml`). You're live with real money.

That's it. No Stripe account, no KYC to receive, no code changes.

## Money facts

- **Price:** $0.02 per transcript call, paid in USDC on Base (≈ $1 = 1 USDC).
- **Your cut:** 80% ($0.016 per call). Platform fee 20% covers facilitator,
  hosting, support, fraud prevention.
- **Settlement:** instant, onchain, straight to YOUR wallet. No intermediary
  holds funds. No chargebacks (crypto payments can't be reversed).
- **Payouts:** there's no "payout" step — the USDC is already yours. To turn
  it into bank money later: Coinbase app → receive → sell USDC → withdraw.
  *That* step needs ID verification (KYC) — but only when you cash out,
  not to start earning.
- **Fees per call:** fractions of a cent (Base gas). No $0.30 Stripe minimum.

## What about the plain HTTP API (`/read`)?

MCPize's x402 covers the **MCP endpoint** (`/mcp`) — that's what agents use
and what's in the registries. The plain `/read` API stays free for now
(humans, testing, demos). Gating it is a later step, not needed to start.

## Discovery (so agents actually find the paid tool)

Being payable isn't enough — agents must discover it:
- MCPize marketplace listing (done in Step 3 above).
- x402 directories: **x402scan**, **Agent402**, **402 Index** — submit the
  payable endpoint once live.
- The official MCP Registry entry (already published) — update its
  description to mention pay-per-call pricing.

## Phase 2 — $19/mo human tier (later, when humans show up)

When real human demand appears (the SEO web page), add Stripe:
- Stripe Payment Links → human pays $19/mo → webhook issues an API key →
  key unlocks unlimited `/read`. Needs a small subscriber database —
  build only when the free tier shows traction.

## Caveats (read once)

1. **Young market.** Tiny buyer base today; you're early, not late. Don't
   expect day-one revenue.
2. **MCPize dependency.** If their gateway has issues, paid calls pause.
   Mitigation: the protocol is open — you can self-host x402 later with
   the same wallet and prices.
3. **BYO endpoint.** The bring-your-own-Railway-URL flow was documented by a
   builder ~6 months ago; dashboards change — the fallback (their hosted
   deploy from your repo) always works.
4. **Wallet safety.** Seed phrase on paper, never in chat, email, or screenshots.
5. **Taxes.** Crypto income is income. Keep records of what lands in the wallet.
6. **Testnet first.** Never test with real money. Base Sepolia + faucet USDC
   is free.
