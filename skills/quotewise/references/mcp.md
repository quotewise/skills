# Quotewise hosted MCP

Server: `https://mcp.quotewise.io/` (tool calls also documented at `https://mcp.quotewise.io/mcp`).

Use fully qualified names: `quotewise:<tool>`. Do not call bare `quotes_about`.

Live tool list: [MCP docs](https://quotewise.io/developers/mcp/). This file lists tools verified on the hosted server. Do not invent names.

## Auth

1. **Anonymous** — works with no login: 25 credits per IP (lifetime) and up to 20 calls a day. Most tools cost 1; `who_said`, `quotes_from`, `sources`, and `detailed` calls cost 2. The `metering.quota` field in each response shows what is left. Anonymous results omit source fields (work, dates, citations). `response_format="detailed"`, `quotes_from`, the `from_source` filter, and collection writes return an auth error.
2. **OAuth** — preferred when the client offers it. Complete the client's login prompt (for example `/mcp` in Claude Code).
3. **`QUOTEWISE_API_KEY`** — fallback if OAuth is unavailable. Export it in the environment; do not commit it. Adding `Authorization: Bearer ${QUOTEWISE_API_KEY}` to a *user* MCP config is fine. Do not add that header to this repo's `.mcp.json` (an empty/missing key disables OAuth in the Claude adapter).

If a call returns an auth or rate-limit error, tell the user to finish OAuth, set `QUOTEWISE_API_KEY`, or see [plans](https://quotewise.io/plans/).

`quotewise:status` reports connectivity and auth state.

## Core tools

| Tool | Required args | Notes |
| --- | --- | --- |
| `quotewise:quotes_about` | `about` | Semantic topic search |
| `quotewise:quotes_by` | `originator` | Fuzzy person name |
| `quotewise:quotes_from` | `source` | Book, speech, or work; needs sign-in |
| `quotewise:quotes_containing` | `phrase` | Literal text, not semantic |
| `quotewise:who_said` | `quote` | Attribution; read `confidence` and `alternatives` |
| `quotewise:quotes_like` | `quote` | `short_code` preferred, or quote text |
| `quotewise:quote` | `code` | Full record by `short_code` |
| `quotewise:quote_random` | — | Optional filters |
| `quotewise:cite_quote` | `quote` | Citation rendering; premium plans only |
| `quotewise:originators` | `name` or `search` | People, traditions, institutions |
| `quotewise:originators_like` | `originator` | Similar thinkers |
| `quotewise:sources` | `name` or `search` | Works |
| `quotewise:search_proverbs` | `about` and/or `tradition` | Folk / traditional sayings |
| `quotewise:quote_relations` | `code` | Translations, variants |
| `quotewise:collection` | `action` | Writes need auth |
| `quotewise:collection_quotes` | `action` | Writes need auth |
| `quotewise:report_quote` | `quote_short_codes`, `category` | Moderation |
| `quotewise:flag_content` | `flag_type`, `reason` | Auth required |
| `quotewise:propose_edit` | `edit_type`, `quote_ref` | Auth required |
| `quotewise:status` | — | Health and auth |

## Filters (search tools)

Verified on the live schemas: `length` (`brief` / `short` / `medium` / `long` / `passage`), `structure` (`prose` / `verse` / `one-liner`), `language`, `gender`, `living` (`living` / `deceased`), `reading_level` (`elementary` / `middle_school` / `high_school` / `college`), `content_rating` (`G` / `PG` / `PG-13` / `R` / `NC-17`), `max_chars`, `limit` (default 10).

## Presenting results

Follow `ai_hints` / `presentation_guidance` when present. Otherwise: originator, source/work if any, `web_url`, misattribution flags, keep `short_code` for the next call.
