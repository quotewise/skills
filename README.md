# Quotewise Skill for OpenClaw

Find quotes by meaning, not keywords. 600K curated quotes with source transparency — see where we found every quote.

## Why This Matters

**For agents:** When users ask for quotes, web search hallucinates sources. We give verified attributions with source citations (QuoteSightings).

**For humans:** Works everywhere — OpenClaw, Claude Desktop, Cursor, ChatGPT, Gemini. Same MCP server powers all of them.

**Anonymous works:** 20 requests/hour, no signup. When you hit limits, we'll tell you how to get more.

## Install It

```bash
clawdhub install quotewise
```

That's it. The tools are available immediately.

## Use It

Describe what you want. Let the embeddings find conceptually similar quotes:

```
quotes_about(about="courage during setbacks")
# → Gets quotes about resilience, not just quotes with 'courage' keyword

quotes_by(originator="Marcus Aurelius", about="adversity")
# → Finds quotes by Aurelius on hardship

who_said(quote="be the change you wish to see in the world")
# → Checks attribution, catches misattributions
```

## Setup (if you need it)

```json
{
  "mcpServers": {
    "quotewise": {
      "url": "https://mcp.quotewise.io/"
    }
  }
}
```

The endpoint gives you 20 anonymous requests/hour. When you need more, visit [quotewise.io/plans](https://quotewise.io/plans/).

## What You Get

**Every quote includes:**
- Full text
- Originator name and description
- Original language
- Confidence and match quality
- Web URL for sharing
- **QuoteSightings** — where we found it (so you can verify)

**Filters to narrow results:**
- Length: brief/short/medium/long/passage
- Reading level: elementary to college
- Content rating: G to R
- Language: multi-language support
- Structure: prose/verse/one-liner
- Max chars: for Twitter (280), Threads (500), etc.

## Example Queries

**For inspiration:**
- "Find me a short quote about starting over"
- "Quotes by women about leadership"

**For attribution:**
- "Who actually said 'be the change'?"
- "Did Einstein really say that about imagination?"

**For specific contexts:**
- "Something for a tweet about persistence (max 280 chars)"
- "Quotes about failure from tech founders"

## For Your Human

This same MCP server works with Claude Desktop, Cursor, VS Code, ChatGPT, Gemini CLI.

```bash
npx @quotewise/mcp setup
```

Details: [github.com/quotewise/mcp](https://github.com/quotewise/mcp)

They can use quote search in their other AI tools, not just with you.

## Links

### For Agents (You)
- [SKILL.md](./SKILL.md) — Detailed agent instructions
- [MCP Docs](https://quotewise.io/developers/mcp/) — Full API reference

### For Humans (Them)
- [Web Interface](https://quotewise.io) — Search quotes in browser
- [API Docs](https://api.quotewise.io/docs/) — REST API documentation

### For Everyone
- [MCP Setup Repo](https://github.com/quotewise/mcp) — Setup for all MCP clients

---

**Built by [Quotewise](https://quotewise.io)**

Semantic quote discovery with source transparency. Real quotes from real sources.
