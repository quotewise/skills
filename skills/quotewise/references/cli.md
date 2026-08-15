# Quotewise CLI (when MCP is absent)

Use the CLI only when Quotewise MCP tools are **not** in this session — scripts, CI, or non-Claude agents. If `quotewise:…` tools are available, use MCP instead. → READ [mcp.md](mcp.md)

## Resolve the binary

1. If `$QW_CLI` is set, run that command.
2. Else if `quotewise` is on `PATH`, use it.
3. Else say the CLI is not installed. Do **not** invent an install package or download URL.

```bash
QW="${QW_CLI:-quotewise}"
command -v "${QW%% *}" >/dev/null || { echo "Quotewise CLI not found"; exit 1; }
```

## Auth

Same policy as MCP: anonymous (20 requests/day) works; **OAuth** is preferred when the CLI offers a login; `QUOTEWISE_API_KEY` is the fallback. Never write a key into the repo or a committed config.

## Commands

A public `quotewise` / `$QW_CLI` command surface was **not verified** from published docs or npm at the time this file was written (no `@quotewise/cli` package; [developers/cli](https://quotewise.io/developers/cli/) is not a live page). Do not guess flags.

When the binary exists:

1. Run `"$QW" --help` (or the equivalent the binary prints) and follow that output.
2. Prefer the same tool names as MCP (`quotes_about`, `who_said`, `quotes_containing`, …) if the CLI exposes them.
3. Ask for JSON when the CLI supports it, so `short_code` / `web_url` / QuoteSightings can be cited.

If help does not document a quote-search command, stop. Point the user at [MCP setup](https://quotewise.io/developers/mcp/) or the [REST API](https://api.quotewise.io/docs/) rather than inventing a CLI invocation.

## Still never invent

CLI or MCP: never invent a quote, originator, or source. Cite what the tool returned (`web_url` / `https://quotewise.io/q/{short_code}`).
