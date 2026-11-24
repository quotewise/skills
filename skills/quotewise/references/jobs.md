# Jobs a quote can do: search recipe and fit test

A quote concentrates an idea; it does not decorate one. Each job has its own way of searching and
its own test. If no candidate passes the test, say so and propose no quote.

## Contents
- Epigraph
- Borrowed authority
- Evidence
- Feeling
- Counterpoint
- Closer
- Shared quote
- Where a quote goes
- When to use none
- Getting past the familiar lines

## Epigraph

Sits above the piece and sets its question. The reader should understand it better after reading
the piece than before.

Search:
- `quotewise:quotes_about` with the piece's tension as a sentence ("trusting a source you cannot
  check"), not its topic ("trust").
- Add `length="brief"` or `"short"`. Try one pass with `structure="verse"` and one with
  `quotewise:search_proverbs`.
- If the piece discusses a book, speech or person, try `quotewise:quotes_from` or
  `quotewise:quotes_by` with `about`: a line from inside the subject often beats a line about it.

Fit test:
- Two lines or fewer.
- Raises the question; does not state the thesis or summarise the piece.
- From a different register than the piece (a poet above a technical essay, an engineer above a
  personal one) more often than from the same one.
- The writer can say in one sentence why this line and not another. If they cannot, it is
  decoration.

## Borrowed authority

A person the reader already trusts makes the claim, so the writer does not have to argue it from
zero. Choose the person before the line.

Search:
1. Ask who this reader trusts on this exact subject. If the writer does not name anyone,
   `quotewise:tags_like(concept="<field>", kind="originator_category")` then
   `quotewise:originators(tags=[...])` lists people in the field.
2. `quotewise:quotes_by(originator=..., about="<claim>")`.
3. `quotewise:originators_like(originator=...)` for people near the obvious name who are quoted
   less. Run `quotes_by` on two of them.

Fit test, three questions:
- Is this their subject? Authority does not transfer between fields: a physicist on marketing
  borrows fame, not authority.
- Does the reader know who they are, or can the writer say it in eight words?
- Is there a source on record? A famous name on an unsourced line is the riskiest quote in a
  piece. Prefer a sourced line from a less famous person.

## Evidence

Someone who was there, or who did the thing, says what happened.

Search: `quotewise:quotes_by(originator=..., about=...)`, or `quotewise:quotes_from` a named work.
Signed in, `from_source="any"` on `quotes_by` or `quotes_about` keeps only quotes with a source.

Fit test: source and year on record; the wording is specific (a number, a decision, a moment), not
a general maxim.

## Feeling

Says what the reader feels more exactly than the writer can.

Search: `quotewise:quotes_about` with the feeling described as an experience ("the dread of
sending work you know is unfinished"). Try `structure="verse"`.

Fit test: concrete image over abstraction; the writer has not already said the same thing in the
sentence before it.

## Counterpoint

The strongest fair version of the view the piece argues against.

Search: `quotewise:quotes_about` with the opposing claim as a sentence its holder would agree
with.

Fit test: a real person who held the view, quoted on the view itself; someone the reader
respects. A weak opponent makes the piece look weak.

## Closer

Leaves the piece's idea in a cadence that stays.

Search: `length="brief"`, `structure="one-liner"`; `quotewise:quotes_like` on the piece's own
last sentence.

Fit test: adds no new idea; does not hand the last word to someone else when the writer's own
last line is good. Test by reading the ending without it.

## Shared quote

Someone else's line posted on its own, with credit: the quote is the whole post. (The writer's own
line posted on its own is a pull quote; see `pull-quote.md`.)

Search: `max_chars=280` for X, `500` for Threads; `length="short"` elsewhere.

Fit test: stands alone with no setup; has a source, because a post gets screenshotted and the
attribution must survive on its own. Give the link so the reader can check it.

## Where a quote goes

| Slot | Works for | Fails when |
|---|---|---|
| Above the piece | Epigraph | It states the thesis |
| Opening line | Feeling, counterpoint | The reader has seen the line before |
| Under a claim | Borrowed authority, evidence | It repeats the claim instead of backing it |
| Before the turn | Counterpoint | The piece never answers it |
| Last line | Closer | It introduces a new idea |

Introduce the speaker before the quote, in the writer's words, when the reader may not know them.
One sentence of the writer's own after the quote, saying what it shows; a quote left alone to make
the point usually has not made it.

## When to use none

- The writer's own sentence says it as well.
- The quote would be the third in the piece.
- The only candidates that fit are lines the reader has seen this month.
- The claim needs data or an example, and a quote would stand in for evidence the piece lacks.

Say this plainly as the recommendation; do not pad a shortlist to avoid it.

## Getting past the familiar lines

Assistants hand every writer the same handful of quotes. A line you could have recited without
the tool is one the reader has probably seen.

- Start in the writer's own collections (SKILL.md, writing step 2).
- Keep the authority, change the line: `quotewise:quotes_by(originator=..., about="<claim>")`
  returns their lesser-known lines on the same point.
- Keep the idea, change the voice: `quotewise:quotes_like(quote="<short_code of the familiar one>")`,
  then filter with `living`, `gender` or `language`.
- Go to the work: `quotewise:quotes_from` a specific book or speech.
- Go to a tradition: `quotewise:search_proverbs`.
- Describe the idea in a full sentence. One-word topics return the most-quoted lines.

A familiar line can still be right, when the piece is about that line or its recognition is the
point. Flag it `familiar` and let the writer decide.
