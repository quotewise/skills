# Expected behavior rubric

Grade **outcomes**, not which file the agent opened.

## All tasks (with-skill)

Must:

1. Call Quotewise MCP (`quotewise:<tool>`). CLI via `$QW_CLI` only if MCP tools are absent.
2. Return a real Quotewise record: `short_code` and/or `https://quotewise.io/q/…` (QuoteSighting / quote page).
3. Not invent a quote, originator, or source.

Must not: web-search for the quote while Quotewise is available; assert a famous attribution from memory.

## All tasks (no-skill)

Expected to web-search or fabricate. Should **fail** “called Quotewise MCP” and usually fail “sourced from Quotewise.”

## Per task

| Case | With-skill call | Extra outcome |
| --- | --- | --- |
| `attribution-trap` | `quotewise:who_said` | Report confidence and alternatives. Do not treat Gandhi (or any memory name) as settled fact. |
| `semantic-find` | `quotewise:quotes_about` | Short, sourced line about starting over after failure. |
| `half-remembered` | `quotewise:quotes_containing` (or `who_said`) | Exact wording + originator from Quotewise, not recitation from memory. |
