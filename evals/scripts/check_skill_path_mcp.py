#!/usr/bin/env python3
"""Smoke-test skill-path MCP calls and grade a no-skill baseline.

Anonymous. No secrets.

With-skill: each hosted MCP call must return a short_code and web_url.
No-skill: canned replies (memory / invented attribution) must fail the
sourced-from-Quotewise check (no quotewise.io/q/ link).
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://mcp.quotewise.io/mcp"

CASES = [
    {
        "name": "attribution-trap",
        "tool": "who_said",
        "arguments": {"quote": "be the change you wish to see", "response_format": "concise"},
    },
    {
        "name": "semantic-find",
        "tool": "quotes_about",
        "arguments": {
            "about": "starting over after failure",
            "length": "short",
            "limit": 2,
            "response_format": "concise",
        },
    },
    {
        "name": "half-remembered",
        "tool": "quotes_containing",
        "arguments": {
            "phrase": "the only thing we have to fear",
            "limit": 2,
            "response_format": "concise",
        },
    },
]


def _sse_or_json(raw: str) -> dict:
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    data_lines = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].strip())
    if not data_lines:
        raise ValueError(f"no JSON in response: {raw[:200]!r}")
    return json.loads("\n".join(data_lines))


def mcp_request(payload: dict, session: str | None = None) -> tuple[dict, str | None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "quotewise-skills-evals/1.0",
    }
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        new_session = resp.headers.get("Mcp-Session-Id") or session
        body = resp.read().decode()
    if not body.strip():
        return {}, new_session
    return _sse_or_json(body), new_session


def first_result(content: object) -> dict:
    if isinstance(content, dict):
        if content.get("short_code") and content.get("web_url"):
            return content
        results = content.get("results")
        if isinstance(results, list) and results:
            return results[0]
        # MCP tool results are often {content:[{type:text,text:"...json..."}]}
        inner = content.get("content")
        if isinstance(inner, list):
            for part in inner:
                if isinstance(part, dict) and part.get("type") == "text":
                    try:
                        return first_result(json.loads(part["text"]))
                    except json.JSONDecodeError:
                        continue
        if "result" in content:
            return first_result(content["result"])
    raise ValueError(f"no quote result in {str(content)[:300]}")


def main() -> int:
    init, session = mcp_request(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "quotewise-skill-evals", "version": "1.0.0"},
            },
        }
    )
    if "error" in init:
        print("initialize failed:", init["error"], file=sys.stderr)
        return 1
    try:
        mcp_request({"jsonrpc": "2.0", "method": "notifications/initialized"}, session)
    except urllib.error.HTTPError:
        pass

    # Memory / web-search style replies. Not sourced from Quotewise.
    no_skill_replies = {
        "attribution-trap": 'Gandhi said "Be the change you wish to see in the world."',
        "semantic-find": 'Try "Fall seven times, stand up eight" — Japanese proverb.',
        "half-remembered": (
            "Franklin D. Roosevelt said the only thing we have to fear is fear itself "
            "(first inaugural, 1933)."
        ),
    }

    failed = 0
    print("== with-skill (hosted MCP) ==")
    for i, case in enumerate(CASES, start=2):
        raw, session = mcp_request(
            {
                "jsonrpc": "2.0",
                "id": i,
                "method": "tools/call",
                "params": {"name": case["tool"], "arguments": case["arguments"]},
            },
            session,
        )
        try:
            if "error" in raw:
                raise ValueError(raw["error"])
            hit = first_result(raw)
            code = hit.get("short_code")
            url = hit.get("web_url", "")
            if not code or "quotewise.io/q/" not in str(url):
                raise ValueError(f"missing short_code/web_url: {hit!r}")
            print(f"PASS {case['name']} {case['tool']} short_code={code} url={url}")
        except Exception as exc:  # noqa: BLE001 — report and continue
            failed += 1
            print(f"FAIL {case['name']} {case['tool']}: {exc}", file=sys.stderr)

    print("== no-skill (expected fail: no Quotewise citation) ==")
    for name, reply in no_skill_replies.items():
        sourced = "quotewise.io/q/" in reply
        if sourced:
            failed += 1
            print(f"FAIL {name}: no-skill reply unexpectedly cited Quotewise")
        else:
            print(f"PASS {name}: no quotewise.io/q/ (fails sourced-from-Quotewise)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
