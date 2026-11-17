# Quotewise skill evals

These cases check that the skill **changes behavior**: with the skill, the agent must use Quotewise and cite a real result. Without the skill, it is expected to web-search or invent, and to fail the “sourced from Quotewise” graders.

Prompts are human-written and outcome-focused. They do **not** name the skill or tell the agent which tool to call.

| Case | Prompt intent | With-skill must |
| --- | --- | --- |
| `attribution-trap` | Commonly misattributed “be the change…” line | `quotewise:who_said`; report confidence/alternatives; no memory-Gandhi-as-fact |
| `semantic-find` | Short quote about starting over after failure | `quotewise:quotes_about`; cite a Quotewise page |
| `half-remembered` | Half-remembered “fear itself” phrase | `quotewise:quotes_containing` or `quotewise:who_said`; exact wording + originator from Quotewise |
| `fdr-one-speech-or-two` | FDR passage that looks stitched from two speeches | Quotewise lookup; say both lines are in the May 27, 1941 address, with the date for a footnote |
| `ford-false-debunk` | Ford “failure is simply the opportunity…”, also credited to Seelig | Quotewise lookup; credit Ford, *My Life and Work* (1922), with the original wording |

Each case is isolated (`evals/<case>/prompt.md` + `graders/`). Shared rubric: [expected_behavior.md](expected_behavior.md).

## With-skill vs no-skill

### Claude models (native harness)

`claude plugin eval` runs a fresh session per case and adds a no-plugin baseline arm for path targets. Two flags are required for this suite: `--mocks off` (the default `record` mode never starts the real Quotewise server) and the server-level allow rule (`mcp__*` is refused).

```bash
# From the plugin root; repeat per model (haiku, sonnet, opus, fable).
claude plugin eval . --runs 1 --model haiku --mocks off \
  --allow-tools mcp__plugin_quotewise_quotewise WebSearch WebFetch --judge-model sonnet --no-publish
```

The adapter's `.mcp.json` sends no `Authorization` header, so this arm uses the anonymous tier (or the user's OAuth token) and draws on that IP's credits. Anonymous results omit sources and dates, so cases that grade a source or date (`ford-false-debunk`, `fdr-one-speech-or-two`, `attribution-trap`) can pass only with a signed-in MCP. A full run also needs more than one IP's 25 anonymous credits.

### Codex and Grok

`evals/scripts/run_agents.py` runs the same case files through `codex exec` and `grok -p`. Each run gets a throwaway `CODEX_HOME` / `HOME` holding only copied auth, so your own skills, MCP servers and instructions never reach either arm. A sandbox profile also denies reads of your real home and `/private/tmp`, so neither arm can read earlier results or kept traces. `with` installs the skill and configures the Quotewise MCP (Bearer `QUOTEWISE_API_KEY` when set); `without` has neither. `llm` graders are judged the way plugin eval judges them: `claude -p --model sonnet`, majority of 3 votes, with tool calls shown only to `focus: trace` graders.

```bash
python3 evals/scripts/run_agents.py --agent codex:gpt-5.6-luna --agent grok:grok-4.7 --runs 3 [--case <glob>] [--no-web]
```

Results (per-run grader verdicts, tool calls, raw transcripts) land in `evals/results/agents-<timestamp>/`.

Grade outcomes, not implementation:

- **with-skill must** call Quotewise MCP (`quotewise:who_said` / `quotes_about` / `quotes_containing`, or CLI via `$QW_CLI` only if MCP is absent), return a real `short_code` / `quotewise.io/q/…` QuoteSighting, and must not invent a quote or originator.
- **no-skill** is expected to web-search or fabricate, and to **fail** the sourced-from-Quotewise graders (`quotewise.io/q/` in the reply; with-skill also needs the matching `quotewise:<tool>` call).

## Smoke test (this repo, no agent)

Proves the three skill-path MCP calls succeed against the hosted server (anonymous), and that canned no-skill replies fail the sourced-from-Quotewise check:

```bash
python3 evals/scripts/check_skill_path_mcp.py
```

Does not require `QUOTEWISE_API_KEY`. Uses 4 of the IP's 25 anonymous credits (`who_said` costs 2).

Do not upload this suite to Skillsbench (needs network + live MCP; their default tasks are no-network).
