# Unattended: scheduled jobs, pipelines and platform bots

Use when nobody can answer a question during the run: a scheduled post, a batch pipeline, a bot
replying on a platform, or instructions that say not to ask. If a person replies mid-run, go back
to the attended behaviour in SKILL.md.

The rules in SKILL.md apply unchanged. Only quotes a Quotewise tool returned in this run.

## Contents
- Decide without asking
- Access and credits
- What to return
- Posting a quote
- Not repeating
- Answering "who said this?" in public
- Lines from someone's own text
- Limits

## Decide without asking

| Missing | Do |
|---|---|
| The claim | Take it from the brief or the text you were given, as one sentence |
| The job | Use the one your instructions name; otherwise `Shared quote` for a post, `Borrowed authority` for a draft |
| The reader | The audience your instructions name; otherwise a general reader |
| Language, length, content rating | Use the platform's limits and your instructions; otherwise `length="short"` |

State every assumption you made in the output. Do not stop to ask.

## Access and credits

- No browser, so no OAuth. Use `QUOTEWISE_API_KEY` from the environment when it is set; otherwise
  run anonymous. Never write a key to a file, a log or a post.
- Anonymous runs have no sources, dates or collections, and a small lifetime allowance per IP. A
  bot that posts on a schedule needs a key.
- Call `quotewise:status` once. Each response carries `metering.quota`; read it.
- Spend little: search with `response_format="concise"`, then fetch `detailed` (via
  `quotewise:quote`) only for the one or two finalists. Three searches at most per pick.
- On an auth or rate-limit error, stop and report it. Do not retry in a loop, and do not fall back
  to memory or web search.

## What to return

One pick, and up to two runners-up. Use the shortlist format in SKILL.md, or these fields as JSON
when the caller reads the result by machine:

```json
{
  "text": "<exactly as returned>",
  "originator": "", "work": "", "year": null,
  "short_code": "", "url": "https://quotewise.io/q/<short_code>",
  "job": "", "flags": [], "assumptions": []
}
```

No candidate passes the screen: return no pick, the test that failed, and the searches you ran.
An empty result is better than a weak or unsourced quote.

## Posting a quote

- Exact wording, the originator's name, and the work when there is room. Include the link when the
  platform allows links.
- Fit the platform with `max_chars` (280 for X, 500 for Threads) instead of trimming a longer
  quote.
- Skip anything with an `attribution_status` set. Signed in, skip anything without a `source_name`:
  a post is screenshotted and the attribution has to hold on its own.
- For a public audience, pass `content_rating` unless your instructions say otherwise.
- Do not add commentary that the record does not support (dates, occasions, "famously said").

## Not repeating

A posting bot's first failure is repeating itself. Keep a ledger when your instructions allow
collection writes; → READ `collections.md` for the names and note format.

- Before choosing: drop candidates already in the ledger (`is_collected` on a detailed result, or
  the ledger's `short_code`s loaded once).
- After posting: add the quote to the ledger with a note `<YYYY-MM-DD> · <where posted> · <post URL>`.
- Create only the collections your instructions name. Remove only quotes this bot added.
- No write permission: keep the posted `short_code`s wherever your instructions say state lives,
  and say in the output that no ledger was kept.

## Answering "who said this?" in public

- Call `quotewise:who_said`. Lead with the finding and the link.
- Misattributed: give `correct_attribution` first, then who it is usually credited to.
- No match: say Quotewise has no record of it. That is not proof the quote is fake; do not say so.
- `confidence` is text match, not certainty about the attribution. Do not present it as a verdict.

## Lines from someone's own text

Asked for the quotable line in a text (→ READ `pull-quote.md` for the tests):

- Return up to three sentences verbatim, each with where it sits and which tests it passes.
- Do not write a new line and do not coach. "No sentence stands alone" is a result.
- When the text is the bot's own output, the same tests apply; choose the line, do not decorate it.

## Limits

A plan limit or quota message is a fact for the operator, not a pitch for the audience. Put the
tool's message in the output or the log, finish with what you have, and never mention plans or
pricing in a public post.
