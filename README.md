# Quotewise Agent Skill

One Agent Skill for finding, checking and tracking quotations with [Quotewise](https://quotewise.io) MCP (or CLI when MCP is not in the session). It works with a person in the conversation and as an unattended bot.

Web search often invents or misattributes quotes. Quotewise returns curated, source-attributed results (QuoteSightings) so the agent can cite what it actually found.

Anonymous access works: **25 free credits per IP**, no signup (most calls cost 1, `who_said` costs 2). Anonymous results omit sources, dates, and citations; sign in to get them. When the client offers it, **OAuth** is the preferred authenticated path. `QUOTEWISE_API_KEY` is the fallback for collections and higher limits.

## Use in any Agent Skills client

Point the client at `skills/quotewise/`. Any environment that understands Agent Skills (`SKILL.md` frontmatter + progressive disclosure) can load it. Other clients that load `SKILL.md` work the same way: connect the hosted MCP at `https://mcp.quotewise.io/`, or use the CLI when MCP is not in the session.

```
skills/quotewise/
  SKILL.md                    rules, who is driving, lookup, writing workflow
  references/mcp.md           tools, filters, auth
  references/cli.md           CLI equivalents
  references/jobs.md          what a quote does in a piece, and how to search for it
  references/collections.md   candidates, used-quotes ledger, plan limits
  references/pull-quote.md    the writer's own quotable line
  references/unattended.md    scheduled jobs, pipelines, platform bots
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

1. **Anonymous** — 25 free credits per IP (lifetime) and up to 20 calls a day, no signup. Results carry the quote, originator, year, and link, but no sources, dates, or citations.
2. **OAuth** — preferred when the client offers it. Complete the client's login prompt (in Claude Code, `/mcp`).
3. **`QUOTEWISE_API_KEY`** — fallback. Export it in the environment that launches the agent; never commit it. You can add `Authorization: Bearer ${QUOTEWISE_API_KEY}` to *your* MCP config, or run `npx @quotewise/mcp setup`.

This repo's `.mcp.json` does not send an `Authorization` header, so anonymous access and OAuth keep working.

Rate limits and paid plans: [quotewise.io/plans](https://quotewise.io/plans/).

## What the agent will do

When the user asks for a quote, half-remembers a line, or wants an attribution check, the agent should call Quotewise instead of searching the web.

Beyond lookup, the skill covers three jobs:

- **Quotes for a piece of writing.** It settles what the quote has to do (epigraph, borrowed authority, evidence, counterpoint, closer, a quote to post), searches your saved collections first, then the corpus, and returns a shortlist of three to five with source, link and flags. "No quote" is a valid answer.
- **Not repeating yourself.** Signed in, it keeps candidates per piece and a `Quotes I've used` ledger in your Quotewise collections. On a plan with one collection it keeps the same record in notes.
- **Your own quotable line.** It finds the one sentence of your draft worth quoting, tests it, checks whether someone already said it, and says where to state it. It asks questions; it does not write the line for you.

### People and bots

The skill asks one question of itself: can it ask a person and get a reply in this session?

| | A person is in the conversation | Unattended (scheduled job, pipeline, platform bot) |
| --- | --- | --- |
| Something is missing | Asks | Infers it and states the assumption |
| Result | A shortlist; you choose | One pick, plus runners-up |
| Collection writes | Offers once | Only when its instructions say so |
| Sign-in or plan limit | Says it once | Reports it as a fact; no upgrade pitch in public posts |

A bot that posts on a schedule needs `QUOTEWISE_API_KEY`: anonymous access has no sources and no collections, so it cannot keep a ledger.

| You ask | Tool |
| --- | --- |
| Quotes about a topic | `quotewise:quotes_about` |
| Quotes by a person | `quotewise:quotes_by` |
| Quotes from a work | `quotewise:quotes_from` |
| Exact words you remember | `quotewise:quotes_containing` |
| Who said this? | `quotewise:who_said` |
| More like this | `quotewise:quotes_like` |
| Save to a collection | `quotewise:collection` / `quotewise:collection_quotes` |

Every result names the originator, with the source when you are signed in, and links to its page on [quotewise.io](https://quotewise.io). Full tool list: [MCP docs](https://quotewise.io/developers/mcp/).

## Contributing

Install the skill, use it, and open a pull request against `skills/quotewise/` when it gets something wrong. Keep `SKILL.md` under 200 lines; detail goes in `references/`, one level deep.

## Validate and evals

```bash
claude plugin validate . --strict
python3 evals/scripts/check_skill_path_mcp.py
```

Agent A/B (with-skill vs no-skill) lives in [`evals/`](evals/README.md). On a machine with Claude Code plugin eval enabled:

```bash
claude plugin eval . --runs 1 --mocks off --allow-tools mcp__plugin_quotewise_quotewise WebSearch WebFetch --no-publish
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
