# Quotewise plugin for Claude Code and Claude Cowork

Find quotes by meaning, not keywords. This plugin teaches Claude when to use [Quotewise](https://quotewise.io) and connects it to the hosted MCP at `https://mcp.quotewise.io/`.

Web search often invents or misattributes quotes. Quotewise returns curated, source-attributed results (QuoteSightings) so Claude can cite what it actually found.

Anonymous access works: **20 requests/day**, no signup. Set `QUOTEWISE_API_KEY` for collections and higher limits.

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

## Optional API key

Leave authentication unset for anonymous use (20 requests/day).

For collections and higher limits, use one of these — do not put a key in this repository:

1. Complete the OAuth prompt some clients show on first connect (`/mcp` in Claude Code).
2. Export `QUOTEWISE_API_KEY` in the environment that launches Claude, then add it to your user MCP config (or run `npx @quotewise/mcp setup`):

   ```bash
   export QUOTEWISE_API_KEY=qw_your_key
   ```

   ```json
   {
     "mcpServers": {
       "quotewise": {
         "type": "http",
         "url": "https://mcp.quotewise.io/",
         "headers": {
           "Authorization": "Bearer ${QUOTEWISE_API_KEY}"
         }
       }
     }
   }
   ```

The plugin's bundled `.mcp.json` does not send an `Authorization` header, so anonymous access and the client's OAuth flow keep working. Putting that header in the plugin config would disable OAuth even when the variable is unset.

Rate limits and paid plans: [quotewise.io/plans](https://quotewise.io/plans/).

## What Claude will do

When you ask for a quote, half-remember a line, or want an attribution check, Claude should call Quotewise instead of searching the web.

| You ask | Tool |
| --- | --- |
| Quotes about a topic | `quotes_about` |
| Quotes by a person | `quotes_by` |
| Quotes from a work | `quotes_from` |
| Exact words you remember | `quotes_containing` |
| Who said this? | `who_said` |
| More like this | `quotes_like` |
| Save to a collection | `collection` / `collection_quotes` |

Every result can include originator, source, and a link on [quotewise.io](https://quotewise.io). Full tool list: [MCP docs](https://quotewise.io/developers/mcp/).

## Validate (developers)

```bash
claude plugin validate . --strict
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
