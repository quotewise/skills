# Quotewise plugin for Claude Code and Claude Cowork

Find quotes by meaning, not keywords. This plugin teaches Claude when to use [Quotewise](https://quotewise.io) and connects it to the hosted MCP at `https://mcp.quotewise.io/`.

Web search often invents or misattributes quotes. Quotewise returns curated, source-attributed results (QuoteSightings) so Claude can cite what it actually found.

Anonymous access works: **20 requests/day**, no signup. When the client offers it, **OAuth** (`/mcp`) is the preferred authenticated path. `QUOTEWISE_API_KEY` is the fallback for collections and higher limits.

## Install

This repository **is** the plugin (not a marketplace). Until it is listed in Anthropic's plugin directory, load it from a clone or a zip of this branch.

### Claude Code

From a clone of this repo (or this PR branch):

```bash
claude --plugin-dir .
```

From a hosted zip of a branch:

```bash
claude --plugin-url https://github.com/quotewise/skills/archive/refs/heads/<branch>.zip
```

Reload with `/reload-plugins` if the install summary asks you to. Confirm the server with `/mcp`.

Guided client setup (optional, any MCP client):

```bash
npx @quotewise/mcp setup
```

Claude Code can also add the hosted server without this plugin:

```bash
claude mcp add --transport http quotewise https://mcp.quotewise.io/
```

### Claude Cowork

1. Open the **Cowork** tab, then **Customize** → **Plugins**.
2. Upload this repository (or a zip of the branch) as a custom plugin.

After Anthropic lists the plugin, Cowork users will install it from **Browse plugins** instead.

After install, ask for a quote (for example, "Find a short quote about starting over") or invoke `/quotewise:quotewise`.

## Auth

1. **Anonymous** — 20 requests/day, no signup.
2. **OAuth** — preferred when the client offers it. In Claude Code, open `/mcp` and complete login.
3. **`QUOTEWISE_API_KEY`** — fallback. Export it in the environment that launches Claude; never commit it. You can add `Authorization: Bearer ${QUOTEWISE_API_KEY}` to *your* MCP config, or run `npx @quotewise/mcp setup`.

This plugin's `.mcp.json` does not send an `Authorization` header, so anonymous access and OAuth keep working.

Rate limits and paid plans: [quotewise.io/plans](https://quotewise.io/plans/).

## What Claude will do

When you ask for a quote, half-remember a line, or want an attribution check, Claude should call Quotewise instead of searching the web.

| You ask | Tool |
| --- | --- |
| Quotes about a topic | `quotewise:quotes_about` |
| Quotes by a person | `quotewise:quotes_by` |
| Quotes from a work | `quotewise:quotes_from` |
| Exact words you remember | `quotewise:quotes_containing` |
| Who said this? | `quotewise:who_said` |
| More like this | `quotewise:quotes_like` |
| Save to a collection | `quotewise:collection` / `quotewise:collection_quotes` |

Every result can include originator, source, and a link on [quotewise.io](https://quotewise.io). Full tool list: [MCP docs](https://quotewise.io/developers/mcp/).

## Validate and evals

```bash
claude plugin validate . --strict
python3 evals/scripts/check_skill_path_mcp.py
```

Agent A/B (with-skill vs no-skill) lives in [`evals/`](evals/README.md). On a machine with Claude Code plugin eval enabled:

```bash
claude plugin eval . --ablation with-without --runs 1 --allow-tools 'mcp__*' WebSearch WebFetch --no-publish
```

## Plugin directory

Listing this plugin at [https://platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit) is a later step. This repository does not submit anything to Anthropic.

## Links

- [Quotewise](https://quotewise.io)
- [MCP setup](https://quotewise.io/developers/mcp/)
- [MCP tools](https://quotewise.io/developers/mcp/)
- [Plans](https://quotewise.io/plans/)
- [Hosted MCP](https://mcp.quotewise.io/)
- [Setup package](https://github.com/quotewise/mcp)

## History

This repo previously shipped as an OpenClaw skill. That install path is no longer the default; Claude Code and Claude Cowork are.

---

Built by [Quotewise](https://quotewise.io) / Christopher Q. Alexander.
