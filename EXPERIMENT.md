# The Agent-as-Customer Experiment

*Notes on building services for AI agents, not just humans.*

## The Hypothesis

AI agents are becoming first-class API consumers. A SKILL.md is documentation optimized for agents — concise, example-heavy, action-oriented.

**The funnel:**
- Agents discover Quotewise via ClawdHub / MCP directories / other agents
- They use it to serve their humans better
- Some hit rate limits
- Agent guides human to sign up
- Human upgrades to $5/mo AI Access

## Target Personas (via agents)

From `docs/vision/03-user-personas.md`:

| Persona | Why They'd Use Via Agent | Upgrade Trigger |
|---------|-------------------------|-----------------|
| **Sarah Chen** (Content Creator) | "Find me a quote about courage for my newsletter" | Hits 10/hr limit mid-deadline |
| **Robert Kim** (Startup Founder) | "Quote for my investor deck about persistence" | Needs reliability for pitch prep |
| **Alex Rivera** (AI Developer) | Testing MCP integration, building quote features | API access for production |
| **Dr. Marcus Williams** (Academic) | Verifying student submissions | Source transparency for lectures |

**Key insight:** The agent is the distribution channel. The human is the paying customer.

## Honesty Guardrails (from copywriter agent)

What we CAN say:
- ✅ "Semantic search finds quotes by meaning"
- ✅ "QuoteSightings shows sources for every quote"
- ✅ "608K+ quotes with source transparency"
- ✅ "Wikiquote-matched quotes hide known fakes"

What we CANNOT say:
- ❌ "Verified quotes" (no systematic verification yet)
- ❌ "Never misquote again" (overpromise)
- ❌ "Attribution confidence scoring" (launching 2026, not now)

**The principle:** Lead with PROCESS (QuoteSightings, transparency) not OUTCOME (verified, never wrong).

## Distribution Channels

### Now
- [x] ClawdHub skill package (AgentSkills format)
- [ ] MCP awesome-list PR
- [ ] quotewise.io/developers/mcp docs update

### Soon
- [ ] ChatGPT Actions directory
- [ ] Claude Desktop featured MCPs (if that becomes a thing)
- [ ] Agent-focused Discord communities

### The Meta-Play
Document this experiment publicly. "Building services for AI agents" is novel enough to attract early adopters.

## Economics

**Current model:**
- Anonymous: 10/hr (discovery)
- Free tier: 100/month (email verification)
- AI Access: $5/mo unlimited

**The math:**
- Agent makes 10 requests → hits limit
- Human sees value, signs up
- $5/mo is 1/4 the cost of ChatGPT ($20/mo)
- "Grand Slam ratio" per Hormozi

**Open question:** Should there be agent-specific tiers? Bulk licensing for agent developers?

## Future: Two-Way Value

Agents could contribute, not just consume:
- Flag misattributions ("This quote seems wrong because...")
- Suggest corrections with sources
- Submit new quotes with provenance
- Rate quote quality

This turns agents into collaborators, not just clients.

## Success Metrics

1. **Discovery:** Anonymous requests/day
2. **Conversion:** Anonymous → free tier rate
3. **Revenue:** Free → AI Access conversion
4. **Quality:** Agent-reported issues (future)
5. **Virality:** Skill installs, mentions in other agents' contexts

## Risks

1. **Token burn:** Both sides pay for inference. Keep skill file lean (~3KB).
2. **Abuse:** Agents could scrape corpus. Rate limits + monitoring.
3. **Attribution:** If agents use quotes without linking back, we lose discovery.
4. **Quality exposure:** Agents surface our data issues (typos, wrong dates).

## ClawdHub Publishing

```bash
# Login
clawdhub login

# Publish
clawdhub publish ./quotewise-skill \
  --slug quotewise \
  --name "Quotewise" \
  --version 1.0.0 \
  --changelog "Initial release: semantic quote search with source transparency" \
  --tags latest,quotes,mcp
```

Or let Chris publish from his account for proper ownership.

---

*This is an experiment. We're lighting the way, not paving the road.*

*Last updated: 2026-01-30*
