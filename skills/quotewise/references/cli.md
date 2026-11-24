# Quotewise CLI equivalents (no MCP in the session)

Use only when `quotewise:` tools are absent. Output is JSON.

## Find the binary

```bash
QW="${QW_CLI:-quotewise}"
command -v "${QW%% *}" >/dev/null || echo "Quotewise CLI not found"
```

Not installed: say so and point to https://github.com/quotewise/cli (releases) or the MCP setup at
https://quotewise.io/developers/mcp/. Do not fall back to memory or web search for quotes.

Auth: `"$QW" auth-status`. Not signed in: `"$QW" login` (browser) or `QUOTEWISE_API_KEY` in the
environment. Never write a key to a file.

Flags change between releases. Run `"$QW" <command> --help` before the first use of a command, and
`"$QW" schema --operation <operationId>` for a request body.

## Commands by workflow step

| Step | MCP | CLI |
|---|---|---|
| Access | `status` | `auth-status` |
| List collections | `collection(list)` | `collections-list --fields name,slug,is_default,quote_count` |
| Semantic search in one collection | `collection_quotes(list, about=)` | `quotes-similar-by-text --text "<claim>" --collection <slug>` |
| Substring search in one collection | n/a | `collections-quotes-list <slug> --q "<words>"` |
| Semantic search, corpus | `quotes_about` | `quotes-similar-by-text --text "<claim>"` |
| By a person | `quotes_by` | `originators-search`, then `originators-quotes <slug>` |
| Similar people | `originators_like` | `originators-similar <slug>` |
| More like a quote | `quotes_like` | `quotes-similar <short_code>` |
| Exact words | `quotes_containing` | `quotes-list --q "<words>"` (substring) |
| Random | `quote_random` | `quotes-random` |
| Variants and translations | `quote_relations` | `quotes-relations <short_code>` |
| Filtered listing | search filters | `quotes-list --length short --max-chars 280 --originator-slug <slug>` |
| Full record | `quote` | `quotes-get <short_code>` |
| Collections holding a quote | `quote(include=["collections"])` | `quotes-collections <short_code>` |
| Create a collection | `collection(create)` | `collections-create --body-file -` |
| Save a quote with a note | `collection_quotes(add, notes=)` | `collections-quotes-add <slug> --body-file -` |
| Change a note | remove, then add | `collections-quote-patch` (see its `--help`) |

`quotes-list --q` is substring match, not semantic. Use `quotes-similar-by-text` for meaning.

## Bodies

```bash
echo '{"name": "Draft: The Authority Paradox", "description": "Candidates, Dec 2026"}' \
  | "$QW" collections-create --body-file -

echo '{"short_code": "abc123", "notes": "The Authority Paradox · epigraph · top · raises the trust question"}' \
  | "$QW" collections-quotes-add <slug> --body-file -
```

Trim list output with `--fields text,short_code,originator_name --first 10`.

There is no CLI command for an attribution check (`who_said`). Find the record by its words and
report what it shows. CLI or MCP, the rules in SKILL.md hold: never invent a quote, originator or
source.
