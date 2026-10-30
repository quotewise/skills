# Quotewise Agent Skill

Agent Skill for verified quotes via [Quotewise](https://quotewise.io) MCP (or CLI when MCP is not in the session).

Web search often invents or misattributes quotes. Quotewise returns curated, source-attributed results (QuoteSightings) so the agent can cite what it actually found.

Anonymous access works: **20 requests/day**, no signup. When the client offers it, **OAuth** is the preferred authenticated path. `QUOTEWISE_API_KEY` is the fallback for collections and higher limits.

## Use in any Agent Skills client

Point the client at `skills/quotewise/`. Any environment that understands Agent Skills (`SKILL.md` frontmatter + progressive disclosure) can load it. Other clients that load `SKILL.md` work the same way: connect the hosted MCP at `https://mcp.quotewise.io/`, or use the CLI when MCP is not in the session.

```
skills/quotewise/
  SKILL.md
  references/mcp.md
  references/cli.md
```

Optional MCP setup (any MCP client):

```bash
npx @quotewise/mcp setup
```

## Claude Code / Cowork (one packaged install)

`.claude-plugin/plugin.json` and `.mcp.json` are an install adapter. They are not the whole product.

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

You can also add the hosted server without the adapter:

```bash
claude mcp add --transport http quotewise https://mcp.quotewise.io/
```

### Claude Cowork

1. Open the **Cowork** tab, then **Customize** → **Plugins**.
2. Upload this repository (or a zip of the branch) as a custom plugin.

After Anthropic lists the adapter, Cowork users will install it from **Browse plugins** instead.

After install, ask for a quote (for example, "Find a short quote about starting over") or invoke `/quotewise:quotewise`.

Listing at [https://platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit) is a later step. This repository does not submit anything to Anthropic.

## Auth

1. **Anonymous** — 20 requests/day, no signup.
2. **OAuth** — preferred when the client offers it. Complete the client's login prompt (in Claude Code, `/mcp`).
3. **`QUOTEWISE_API_KEY`** — fallback. Export it in the environment that launches the agent; never commit it. You can add `Authorization: Bearer ${QUOTEWISE_API_KEY}` to *your* MCP config, or run `npx @quotewise/mcp setup`.

This repo's `.mcp.json` does not send an `Authorization` header, so anonymous access and OAuth keep working.

Rate limits and paid plans: [quotewise.io/plans](https://quotewise.io/plans/).

## What the agent will do

When the user asks for a quote, half-remembers a line, or wants an attribution check, the agent should call Quotewise instead of searching the web.

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

## Links

- [Quotewise](https://quotewise.io)
- [MCP setup](https://quotewise.io/developers/mcp/)
- [MCP tools](https://quotewise.io/developers/mcp/)
- [Plans](https://quotewise.io/plans/)
- [Hosted MCP](https://mcp.quotewise.io/)
- [Setup package](https://github.com/quotewise/mcp)

---

Built by [Quotewise](https://quotewise.io) / Christopher Q. Alexander.
