# Collections: candidates, used quotes, limits

Collections are the writer's memory across pieces and sessions. Collection calls cost no search
credits. All writes need sign-in.

## Contents
- Which mode: several collections, or one
- Naming convention (several collections)
- One-collection mode
- Note format
- Has this been used?
- When the writer picks
- Plan limits

## Which mode

Plans differ in how many collections an account may hold, and the limits change, so do not state
numbers from memory. `can_create_collections` in `quotewise:status` only reports sign-in; it does
not say whether there is room for another collection.

1. List the writer's collections. If they already keep a used-quotes or per-piece collection under
   any name, use theirs and skip the convention below.
2. Otherwise ask once whether to set up tracking, then try to create `Quotes I've used`.
3. Created → several-collections mode. Refused for a plan limit → one-collection mode, and follow
   "Plan limits" below.

## Naming convention (several collections)

| Name | Holds | Lifetime |
|---|---|---|
| `Quotes I've used` | Every quote the writer has published, one entry each | Permanent, one per writer |
| `Draft: <piece title>` | Candidates for one piece | Until the piece ships; then offer to delete it |
| `Shelf: <subject>` | Standing stock for a subject the writer returns to | Permanent, optional |
| The default collection (`is_default: true`) | Favorites saved while browsing | Never rename or reorganise it |

Create collections private. Use the slug the create call returns for later calls.

```text
quotewise:collection(action="create", name="Draft: The Authority Paradox",
                     description="Candidates for the essay, Dec 2026")
```

## One-collection mode

Everything lives in the writer's one collection (usually the default), and the note carries the
state. The first word of the note is the status:

| Status word | Meaning |
|---|---|
| `candidate` | Shortlisted for a piece, not yet published |
| `used` | Published |
| (no note) | A favorite saved while browsing; leave it alone |

Updating a note through MCP means `remove` then `add` with the new note. Do that only for quotes
this skill added; never rewrite a note the writer wrote.

## Note format

`notes` is private to the writer. One line, fields separated by ` · `. In one-collection mode put
the status word first.

| Where | Note | Example |
|---|---|---|
| `Draft: …` / `candidate` | `<piece title> · <job> · <slot> · <why>` | `The Authority Paradox · epigraph · top · raises the trust question` |
| `Quotes I've used` / `used` | `<YYYY-MM-DD> · <piece title> · <job> · <published URL if known>` | `2026-12-08 · The Authority Paradox · epigraph · https://…` |
| `Shelf: …` | `supports: <the claim>` | `supports: checklists beat expertise under stress` |

```text
quotewise:collection_quotes(action="add", collection="<slug>", quote="<short_code>",
                            notes="The Authority Paradox · epigraph · top · raises the trust question")
```

`framing` and `circumstance` are shown to readers when a collection is shared. Leave them empty
unless the writer is building a collection to publish.

## Has this been used?

Run before showing a shortlist (SKILL.md, writing step 4).

1. Once per session, load the ledger: `quotewise:collection_quotes(action="list",
   collection="<slug>", limit=100, response_format="detailed")`; page while `has_next`. Keep the
   short codes and notes. In one-collection mode the ledger is the entries whose note starts
   `used`.
2. Drop any candidate whose `short_code` is in the ledger.
3. The same line can exist in another wording under another code. For each finalist, also run
   `quotewise:collection_quotes(action="list", collection="<slug>", by="<originator>")` and read
   the results. Tell the writer when they have quoted this person before, and how often.

For a single quote, `quotewise:quote(code=..., include=["collections"])` lists the collections
that hold it. In detailed search results, `is_collected: true` means it is already in one of the
writer's collections; say so when it helps ("from your favorites").

No ledger yet: offer to seed it with quotes from pieces already published. The writer pastes them;
resolve each with `quotewise:who_said` or `quotewise:quotes_containing` and add the matches.

"What have I used?": list the ledger with `response_format="detailed"`; the notes hold the piece
and the date.

## When the writer picks

1. Record the pick as used, with the dated note.
2. Leave the other candidates saved; they are stock for the next piece on the subject.
3. Several-collections mode: when the piece ships, offer to move the keepers to a `Shelf: …` and
   delete the draft collection. Never delete a collection without being asked.

## Plan limits

When a write is refused for a limit (collection count, or saved-quote count):

1. Report the error text as returned, and what was not saved.
2. Give the options in this order:
   - Work within the plan: one-collection mode; or delete a `Draft: …` collection whose piece has
     shipped; or remove `candidate` entries for shipped pieces.
   - Raise the limit: https://quotewise.io/plans/ (separate collections per piece, project or
     subject are a paid feature).
3. Carry on with the shortlist in the conversation either way. Never withhold candidates because
   they could not be saved.

Mention the plans page once per session, and only at the point a limit is hit.
