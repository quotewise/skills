# Quotewise skill evals

These cases check that the skill **changes behavior**: with the skill, Claude must use Quotewise and cite a real result. Without the skill, it is expected to web-search or invent, and to fail the “sourced from Quotewise” graders.

Prompts are human-written and outcome-focused. They do **not** name the skill or tell the agent which tool to call.

| Case | Prompt intent | With-skill must |
| --- | --- | --- |
| `attribution-trap` | Commonly misattributed “be the change…” line | `quotewise:who_said`; report confidence/alternatives; no memory-Gandhi-as-fact |
| `semantic-find` | Short quote about starting over after failure | `quotewise:quotes_about`; cite a Quotewise page |
| `half-remembered` | Half-remembered “fear itself” phrase | `quotewise:quotes_containing` or `quotewise:who_said`; exact wording + originator from Quotewise |

Each case is isolated (`evals/<case>/prompt.md` + `graders/`). Shared rubric: [expected_behavior.md](expected_behavior.md).

## With-skill vs no-skill

Claude Code’s harness (`claude plugin eval`) runs a fresh session per case. `--ablation with-without` adds a no-plugin baseline arm. Path targets default to no ablation — pass the flag.

On a logged-in Claude Code machine (≥ 2.1.198):

```bash
# From the plugin root.
claude plugin eval . \
  --ablation with-without \
  --runs 1 \
  --allow-tools 'mcp__*' WebSearch WebFetch \
  --no-publish
```

Equivalent intent if you drive `claude -p` yourself:

| Arm | How |
| --- | --- |
| with-skill | `claude --plugin-dir . -p "<prompt>"` (Quotewise MCP connected) |
| no-skill | Same prompt, **no** `--plugin-dir` / plugin, no Quotewise MCP |

Grade outcomes, not implementation:

- **with-skill must** call Quotewise MCP (`quotewise:who_said` / `quotes_about` / `quotes_containing`, or CLI via `$QW_CLI` only if MCP is absent), return a real `short_code` / `quotewise.io/q/…` QuoteSighting, and must not invent a quote or originator.
- **no-skill** is expected to web-search or fabricate, and to **fail** the sourced-from-Quotewise graders (`quotewise.io/q/` in the reply; with-skill also needs the matching `quotewise:<tool>` call).

This cloud VM has Claude Code 2.1.233, but `claude auth status` is `loggedIn: false` and no `ANTHROPIC_API_KEY` is set, so a full agent A/B cannot run here. Run the command above locally and paste WITH vs WITHOUT scores on the PR.

## Smoke test (this repo, no agent)

Proves the three skill-path MCP calls succeed against the hosted server (anonymous), and that canned no-skill replies fail the sourced-from-Quotewise check:

```bash
python3 evals/scripts/check_skill_path_mcp.py
```

Does not require `QUOTEWISE_API_KEY`. Uses 3 of the anonymous 20/day.

Do not upload this suite to Skillsbench (needs network + live MCP; their default tasks are no-network).
