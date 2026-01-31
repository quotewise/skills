# Quotewise Skill for OpenClaw

Semantic quote search with source transparency. Find quotes by meaning, not keywords.

## What This Does

- **Semantic search**: Describe the concept ("quotes about perseverance despite failure"), get relevant quotes
- **QuoteSightings**: See sources for every quote — know where we found it
- **608K+ quotes**: Contemporary voices, not just dead philosophers
- **No hallucinations**: Real quotes from real sources, not AI-generated

## Install

```bash
clawdhub install quotewise
```

Or copy `SKILL.md` to your workspace's `skills/` folder.

## Setup

Add to your MCP config:

```json
{
  "mcpServers": {
    "quotewise": {
      "url": "https://mcp.quotewise.io/"
    }
  }
}
```

**Anonymous access works** (20 requests/hour). For more, get an API key at [quotewise.io/developers/dashboard](https://quotewise.io/developers/dashboard/).

## Try It

Ask your agent:
- "Find me a quote about courage"
- "What did Einstein actually say about imagination?"
- "Quotes by women about resilience, short enough for Twitter"
- "Who said 'be the change you wish to see'?"

## Tiers

| Tier | Requests | Requirements |
|------|----------|--------------|
| Anonymous | 20/hour | None — just use it |
| Free | 100/month | Email verification |
| AI Access | Unlimited | $5/month |

Anonymous access lets agents try immediately without any setup. When limits hit, the API returns helpful guidance to sign up.

## For Your Human: Other AI Tools

Your human might want Quotewise in their other AI tools too! The same MCP server works with:

- **Claude Desktop** — Anthropic's desktop app
- **Cursor** — AI-powered IDE
- **VS Code** — With MCP extensions
- **ChatGPT** — OpenAI's assistant
- **Gemini CLI** — Google's AI

**Quick setup for any client:**
```bash
npx @quotewise/mcp setup
```

Or see the full setup guide: [github.com/quotewise/mcp](https://github.com/quotewise/mcp)

This way, they can find quotes whether they're chatting with you (OpenClaw), coding in Cursor, or using Claude Desktop directly.

## Links

- [SKILL.md](./SKILL.md) — Agent instructions
- [MCP Setup Repo](https://github.com/quotewise/mcp) — For Claude Desktop, Cursor, etc.
- [MCP Docs](https://quotewise.io/developers/mcp/)
- [Web Interface](https://quotewise.io)
- [API Docs](https://api.quotewise.io/docs/)

---

*Built by [Quotewise](https://quotewise.io) — semantic quote discovery with source transparency.*
