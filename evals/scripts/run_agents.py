#!/usr/bin/env python3
"""Run the eval cases against non-Claude agent CLIs (Codex, Grok) with and without the skill.

Claude models use the native harness (`claude plugin eval`, see evals/README.md). This runner
reads the same case files (evals/<case>/prompt.md + graders/*.md), so one suite grades every
vendor, and judges `llm` graders the way plugin eval does: majority of 3 votes. Sonnet is the
default judge here because haiku misread nuanced answer keys; pass plugin eval --judge-model sonnet to match.

Each run gets a throwaway home (CODEX_HOME / HOME) holding only copied auth, so the user's own
skills, MCP servers and instructions never leak into either arm:

  with     skill installed + Quotewise MCP configured
  without  neither (web search still on unless --no-web)

    python3 evals/scripts/run_agents.py --agent codex:gpt-5.6-luna --agent grok:grok-4.7 --case semantic-find

QUOTEWISE_API_KEY, when set, is sent as a Bearer header to the MCP server (with arm only).
The configs reference it by name; the key itself is never written to disk.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals"
SKILL = ROOT / "skills" / "quotewise"
MCP_URL = "https://mcp.quotewise.io/"
def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text.strip()
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":  # YAML-quoted scalar
                v = json.loads(v) if v[0] == '"' else v[1:-1]
            meta[k.strip()] = v
    return meta, m.group(2).strip()


def load_cases(pattern: str) -> list[dict]:
    cases = []
    for prompt in sorted(EVALS.glob("*/prompt.md")):
        meta, body = frontmatter(prompt)
        name = meta.get("name", prompt.parent.name)
        if not fnmatch.fnmatch(name, pattern):
            continue
        graders = []
        for g in sorted((prompt.parent / "graders").glob("*.md")):
            gmeta, gbody = frontmatter(g)
            graders.append({"name": g.stem, **gmeta, "rubric": gbody})
        cases.append(
            {
                "name": name,
                "prompt": body,
                "graders": graders,
                "timeout": int(meta.get("timeout_seconds", 180)),
                "max_turns": meta.get("max_turns", "8"),
            }
        )
    return cases


def setup_codex(home: Path, ws: Path, arm: str, model: str, case: dict, web: bool) -> tuple[list[str], dict]:
    cx = home / ".codex"
    cx.mkdir(parents=True)
    shutil.copy(Path.home() / ".codex" / "auth.json", cx / "auth.json")
    # Shell reads stay off the real home and /tmp (prior eval results, kept traces, global skills),
    # except this run's own temp dir; sandboxed commands get no network.
    config = (
        'default_permissions = "eval"\n\n[permissions.eval.filesystem]\n":root" = "read"\n'
        f'{json.dumps(str(Path.home()))} = "deny"\n"/private/tmp" = "deny"\n'
        f'{json.dumps(str(home.parent.resolve()))} = "read"\n\n[permissions.eval.network]\nenabled = false\n\n'
    )
    if arm == "with":
        config += f'[mcp_servers.quotewise]\nurl = "{MCP_URL}"\n'
        if os.environ.get("QUOTEWISE_API_KEY"):
            config += 'bearer_token_env_var = "QUOTEWISE_API_KEY"\n'
        shutil.copytree(SKILL, cx / "skills" / "quotewise")
    (cx / "config.toml").write_text(config)
    cmd = (
        ["codex"]
        + (["--search"] if web else ["-c", 'web_search="disabled"'])
        + [
            "exec",
            "--disable",
            "apps",  # ChatGPT account connectors (incl. a web-search app) bypass config isolation
            "--json",
            "--skip-git-repo-check",
            "--ephemeral",
            "-m",
            model,
            "-C",
            str(ws),
            case["prompt"],
        ]
    )
    return cmd, {"CODEX_HOME": str(cx), "HOME": str(home)}  # HOME: no ~/.agents/skills discovery


def setup_grok(home: Path, ws: Path, arm: str, model: str, case: dict, web: bool) -> tuple[list[str], dict]:
    gx = home / ".grok"
    gx.mkdir(parents=True)
    shutil.copy(Path.home() / ".grok" / "auth.json", gx / "auth.json")
    # Same isolation as Codex: reads stay off the real home and /tmp (kernel-enforced).
    deny = json.dumps([str(Path.home()), "/private/tmp"])
    (gx / "sandbox.toml").write_text(f'[profiles.eval]\nextends = "strict"\ndeny = {deny}\n')
    # read_file reads the skill; the allowlist also keeps out XSearch. The MCP meta-tools stay on unless
    # removed. Without tools to research with, Grok often stalls to the timeout instead of answering.
    tools, allow = "read_file", ["--disallowed-tools", "search_tool,use_tool"]
    if arm == "with":
        lines = ["[mcp_servers.quotewise]", f'url = "{MCP_URL}"']
        if os.environ.get("QUOTEWISE_API_KEY"):
            lines.append('headers = { "Authorization" = "Bearer ${QUOTEWISE_API_KEY}" }')
        (gx / "config.toml").write_text("\n".join(lines) + "\n")
        shutil.copytree(SKILL, gx / "skills" / "quotewise")
        tools += ",search_tool,use_tool"  # Grok reaches MCP tools only through these
        allow = ["--allow", "MCPTool(quotewise__*)"]  # dontAsk refuses unapproved MCP calls
    cmd = [
        "grok",
        "-p",
        case["prompt"],
        "--output-format",
        "streaming-messages-json",
        "-m",
        model,
        "--cwd",
        str(ws),
        "--max-turns",
        str(case["max_turns"]),
        "--permission-mode",
        "dontAsk",
        "--no-subagents",
        "--sandbox",
        "eval",
        "--tools",
        tools + (",web_search,web_fetch" if web else ""),
    ] + allow + ([] if web else ["--disable-web-search"])
    env = {"HOME": str(home), "GROK_CLAUDE_SKILLS_ENABLED": "false", "GROK_CURSOR_SKILLS_ENABLED": "false"}
    return cmd, env


def parse_codex(stdout: str) -> tuple[str, list[dict]]:
    final, calls = "", []
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = ev.get("item") or {}
        if ev.get("type") != "item.completed":
            continue
        kind = item.get("type")
        if kind == "agent_message":
            final = item.get("text", final)
        elif kind == "mcp_tool_call":
            calls.append(
                {
                    "name": f"mcp__{item.get('server')}__{item.get('tool')}",
                    "input": item.get("arguments"),
                    "output": clip(item.get("result") or item.get("error")),
                }
            )
        elif kind == "web_search":
            calls.append({"name": "WebSearch", "input": item.get("query")})
        elif kind == "command_execution":
            calls.append({"name": "Bash", "input": item.get("command"), "output": clip(item.get("aggregated_output"))})
    return final, calls


def parse_stream_json(stdout: str) -> tuple[str, list[dict]]:
    """Claude stream-json / Grok streaming-messages-json (same wire format)."""
    final, calls, by_id = "", [], {}
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        blocks = (ev.get("message") or {}).get("content", []) if ev.get("type") in ("assistant", "user") else []
        for block in blocks if isinstance(blocks, list) else []:
            kind = block.get("type")
            if kind in ("tool_use", "server_tool_use"):
                call = {"name": block.get("name"), "input": block.get("input")}
                if call["name"] == "use_tool":  # Grok's MCP meta-tool: {"tool_name": "server__tool", "tool_input": …}
                    inp = call["input"] or {}
                    call = {"name": f"mcp__{inp.get('tool_name', '')}", "input": inp.get("tool_input")}
                by_id[block.get("id")] = call
                calls.append(call)
            elif kind in ("tool_result", "web_search_tool_result") and block.get("tool_use_id") in by_id:
                by_id[block["tool_use_id"]]["output"] = clip(block.get("content"))
            elif kind == "text" and ev["type"] == "assistant":
                final = block.get("text", final)
        if ev.get("type") == "result" and ev.get("result"):
            final = ev["result"]
    return final, calls


def clip(value: object, limit: int = 8000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text[:limit]


VENDORS = {"codex": (setup_codex, parse_codex), "grok": (setup_grok, parse_stream_json)}


def tool_matches(called: str, wanted: str) -> bool:
    """`mcp__plugin_quotewise_quotewise__who_said` matches any quotewise server's who_said."""
    suffix = wanted.rsplit("__", 1)[-1]
    if "quotewise" in wanted:
        return "quotewise" in called and called.rsplit("__", 1)[-1] == suffix
    return called == wanted or called.rsplit("__", 1)[-1] == suffix


def judge(rubric: str, prompt: str, final: str, calls: list[dict], model: str) -> tuple[bool, str]:
    order = (
        "You grade one AI assistant transcript against a rubric. Grade only what the rubric asks; "
        "tool outputs may be incomplete (web search results are not captured), so do not fail a reply "
        "for facts you cannot see in them unless the rubric requires it. Reply with ONLY a JSON object "
        '{"pass": true|false, "reason": "<one sentence>"}.\n\n'
        f"RUBRIC:\n{rubric}\n\nUSER PROMPT:\n{prompt}\n\n"
        f"TOOL CALLS (name, input, output; in order):\n{json.dumps(calls, ensure_ascii=False)[:48000]}\n\n"
        f"FINAL REPLY:\n{final[:8000]}\n"
    )
    with tempfile.TemporaryDirectory() as cwd:
        out = subprocess.run(  # prompt on stdin: --mcp-config is variadic and would swallow it
            [
                "claude",
                "-p",
                "--model",
                model,
                "--output-format",
                "json",
                "--setting-sources",
                "project",
                "--strict-mcp-config",
                "--mcp-config",
                '{"mcpServers":{}}',
            ],
            input=order,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=180,
        )
    try:
        reply = json.loads(out.stdout).get("result", "")
        verdict, _ = json.JSONDecoder().raw_decode(reply[reply.index("{") :])  # judges may add text after it
        return bool(verdict["pass"]), verdict.get("reason", "")
    except (ValueError, KeyError) as exc:
        return False, f"judge error: {exc}: {out.stdout[:200]} {out.stderr[:200]}"


def grade(case: dict, final: str, calls: list[dict], judge_model: str) -> list[dict]:
    results = []
    names = [c["name"] or "" for c in calls]
    for g in case["graders"]:
        kind = g.get("type")
        if kind == "regex":
            ok, why = bool(re.search(g["pattern"], final)), f"/{g['pattern']}/ in last message"
        elif kind == "tool_used":
            n = sum(tool_matches(x, g["tool"]) for x in names)
            ok, why = n >= int(g.get("min", 1)), f"{g['tool']} called {n}x"
        elif kind == "llm":
            seen = calls if g.get("focus") == "trace" else []  # plugin eval's default focus is last_message
            votes = [judge(g["rubric"], case["prompt"], final, seen, judge_model) for _ in range(3)]
            ok = sum(v for v, _ in votes) >= 2
            why = " | ".join(f"{'PASS' if v else 'FAIL'}: {r}" for v, r in votes)
        else:
            ok, why = False, f"unsupported grader type {kind!r}"
        results.append({"grader": g["name"], "type": kind, "pass": ok, "detail": why})
    return results


def run_one(vendor: str, model: str, arm: str, case: dict, web: bool, raw_dir: Path, n: int = 0) -> dict:
    setup, parse = VENDORS[vendor]
    with tempfile.TemporaryDirectory(prefix="qw-eval-") as tmp:
        home, ws = Path(tmp) / "home", Path(tmp) / "ws"
        ws.mkdir()
        cmd, env = setup(home, ws, arm, model, case, web)
        start = time.monotonic()
        try:
            proc = subprocess.run(
                cmd,
                cwd=ws,
                env={**os.environ, **env},
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=case["timeout"],
            )
            stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, code = (
                (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                "timeout",
                -1,
            )
    raw = raw_dir / f"{case['name']}.{vendor}-{model}.{arm}.{n}.jsonl"
    raw.write_text(stdout + ("\n# STDERR\n" + stderr if stderr else ""))
    final, calls = parse(stdout)
    return {
        "case": case["name"],
        "agent": f"{vendor}:{model}",
        "arm": arm,
        "exit": code,
        "seconds": round(time.monotonic() - start, 1),
        "tools": [c["name"] for c in calls],
        "calls": calls,
        "final": final,
        "raw": str(raw),
    }


def main() -> int:
    global SKILL
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--agent", action="append", required=True, help="vendor:model, e.g. codex:gpt-5.6-luna")
    ap.add_argument("--arm", action="append", choices=["with", "without"], help="default: both")
    ap.add_argument("--case", default="*", help="case name glob")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--no-web", dest="web", action="store_false", help="disable web search in both arms")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--skill", type=Path, default=SKILL, help="skill dir the with arm installs (A/B variants)")
    ap.add_argument("--out", type=Path, default=EVALS / "results" / f"agents-{time.strftime('%Y%m%d-%H%M%S')}")
    args = ap.parse_args()
    SKILL = args.skill.resolve()

    cases = load_cases(args.case)
    if not cases:
        print(f"no cases match {args.case!r}", file=sys.stderr)
        return 1
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in args.agent:
        vendor, _, model = spec.partition(":")
        if vendor not in VENDORS or not model:
            print(f"bad --agent {spec!r}; vendors: {', '.join(VENDORS)}", file=sys.stderr)
            return 1
        for case in cases:
            for arm in args.arm or ["with", "without"]:
                for n in range(args.runs):
                    row = run_one(vendor, model, arm, case, args.web, args.out, n)
                    row["graders"] = grade(case, row["final"], row["calls"], args.judge_model)
                    row["score"] = sum(g["pass"] for g in row["graders"]) / max(len(row["graders"]), 1)
                    rows.append(row)
                    print(
                        f"{row['agent']:<28} {arm:<8} {case['name']:<22} score={row['score']:.2f} "
                        f"exit={row['exit']} tools={','.join(row['tools']) or '-'}"
                    )
    (args.out / "results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"\n{args.out / 'results.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
